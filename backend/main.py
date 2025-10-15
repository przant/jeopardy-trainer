from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Literal
import random
import sqlite3
import base64
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent

app = FastAPI(title="Jeopardy Trainer")

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DB_PATH = "tracker.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS question_exposure (
            question_id TEXT PRIMARY KEY,
            domain TEXT,
            seen_count INTEGER DEFAULT 0,
            last_seen TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Question loading
def load_questions(domain: str) -> List[dict]:
    """Load and parse question bank for given domain"""
    file_map = {
        "go": "gopardy-questions.md",
        "k8s": "kuberpardy-questions.md", 
        "linux": "jeolinux-questions.md"
    }
    
    file_path = Path(__file__).parent / "data" / file_map[domain]
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Parse markdown questions
    questions = []
    blocks = content.split('\n## Q')[1:]  # Split by question marker
    
    for block in blocks:
        lines = block.strip().split('\n')
        
        # Parse header: Q001 [basic] [multiple-choice]
        header = lines[0]
        q_id = header.split()[0]
        tags = [t.strip('[]') for t in header.split('[')[1:]]
        difficulty = tags[0] if len(tags) > 0 else 'basic'
        q_type = tags[1] if len(tags) > 1 else 'multiple-choice'
        
        # Extract question text
        question_text = ""
        options = []
        answer = ""
        explanation = ""
        
        section = None
        for line in lines[1:]:
            if line.startswith("**Question:**"):
                section = "question"
                question_text = line.replace("**Question:**", "").strip()
            elif line.startswith("**Options:**"):
                section = "options"
            elif line.startswith("**Answer:**"):
                section = "answer"
                answer = line.replace("**Answer:**", "").strip()
            elif line.startswith("**Explanation:**"):
                section = "explanation"
                explanation = line.replace("**Explanation:**", "").strip()
            elif line.startswith("---"):
                break
            elif section == "question" and line.strip():
                question_text += "\n" + line
            elif section == "options" and line.strip():
                options.append(line.strip())
            elif section == "explanation" and line.strip():
                explanation += " " + line.strip()
        
        questions.append({
            "id": f"{domain}-{q_id}",
            "domain": domain,
            "difficulty": difficulty,
            "type": q_type,
            "question": question_text.strip(),
            "options": options if options else None,
            "answer": answer,
            "explanation": explanation
        })
    
    return questions

# Models
class SessionRequest(BaseModel):
    domain: Literal["go", "k8s", "linux"]
    count: int = 10

class AnswerSubmission(BaseModel):
    question_id: str
    user_answer: str

class SessionSubmission(BaseModel):
    domain: str
    answers: List[AnswerSubmission]

# Endpoints
@app.get("/")
def root():
    return {"message": "Jeopardy Trainer API", "version": "1.0"}

@app.post("/session/start")
def start_session(request: SessionRequest):
    """Start new quiz session with smart question selection"""
    
    # Load all questions for domain
    all_questions = load_questions(request.domain)
    
    # Get exposure data
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Prioritize unseen questions, then less-seen
    selected = []
    
    # Try to get unseen first
    for q in all_questions:
        c.execute("SELECT seen_count FROM question_exposure WHERE question_id = ?", (q["id"],))
        row = c.fetchone()
        seen_count = row[0] if row else 0
        
        if seen_count == 0:
            selected.append(q)
        
        if len(selected) >= request.count:
            break
    
    # If need more, get seen_count = 1
    if len(selected) < request.count:
        for q in all_questions:
            if q in selected:
                continue
            c.execute("SELECT seen_count FROM question_exposure WHERE question_id = ?", (q["id"],))
            row = c.fetchone()
            seen_count = row[0] if row else 0
            
            if seen_count == 1:
                selected.append(q)
            
            if len(selected) >= request.count:
                break
    
    # If still need more, get seen_count = 2
    if len(selected) < request.count:
        for q in all_questions:
            if q in selected:
                continue
            c.execute("SELECT seen_count FROM question_exposure WHERE question_id = ?", (q["id"],))
            row = c.fetchone()
            seen_count = row[0] if row else 0
            
            if seen_count == 2:
                selected.append(q)
            
            if len(selected) >= request.count:
                break
    
    # Shuffle for variety
    random.shuffle(selected)
    selected = selected[:request.count]
    
    conn.close()
    
    # Return questions without answers
    questions_for_client = []
    for q in selected:
        questions_for_client.append({
            "id": q["id"],
            "type": q["type"],
            "difficulty": q["difficulty"],
            "question": q["question"],
            "options": q["options"]
        })
    
    return {
        "domain": request.domain,
        "questions": questions_for_client,
        "count": len(questions_for_client)
    }

@app.post("/session/submit")
def submit_session(submission: SessionSubmission):
    """Submit answers and get results"""
    
    # Load questions to check answers
    all_questions = load_questions(submission.domain)
    question_map = {q["id"]: q for q in all_questions}
    
    results = []
    score = 0
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    for answer_sub in submission.answers:
        q_id = answer_sub.question_id
        user_answer = answer_sub.user_answer.strip()
        
        if q_id not in question_map:
            continue
        
        question = question_map[q_id]
        correct_answer = question["answer"].strip()
        
        # Check answer (case-insensitive for fill-blank)
        is_correct = user_answer.lower() == correct_answer.lower()
        
        if is_correct:
            score += 1
        
        results.append({
            "question_id": q_id,
            "question": question["question"],
            "type": question["type"],
            "options": question["options"],
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "explanation": question["explanation"]
        })
        
        # Update exposure count
        c.execute("""
            INSERT INTO question_exposure (question_id, domain, seen_count, last_seen)
            VALUES (?, ?, 1, ?)
            ON CONFLICT(question_id) DO UPDATE SET
                seen_count = seen_count + 1,
                last_seen = ?
        """, (q_id, submission.domain, datetime.now().isoformat(), datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    
    return {
        "score": score,
        "total": len(results),
        "percentage": round((score / len(results)) * 100, 1) if results else 0,
        "results": results
    }

@app.get("/stats/{domain}")
def get_stats(domain: str):
    """Get question exposure stats for domain"""
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN seen_count = 0 THEN 1 ELSE 0 END) as unseen,
            SUM(CASE WHEN seen_count = 1 THEN 1 ELSE 0 END) as seen_once,
            SUM(CASE WHEN seen_count = 2 THEN 1 ELSE 0 END) as seen_twice,
            SUM(CASE WHEN seen_count >= 3 THEN 1 ELSE 0 END) as exhausted
        FROM question_exposure
        WHERE domain = ?
    """, (domain,))
    
    row = c.fetchone()
    conn.close()
    
    # Get total questions available
    all_questions = load_questions(domain)
    total_available = len(all_questions)
    
    if row and row[0]:
        return {
            "domain": domain,
            "total_questions": total_available,
            "tracked": row[0],
            "unseen": total_available - row[0] if row[0] else total_available,
            "seen_once": row[2] or 0,
            "seen_twice": row[3] or 0,
            "exhausted": row[4] or 0
        }
    else:
        return {
            "domain": domain,
            "total_questions": total_available,
            "tracked": 0,
            "unseen": total_available,
            "seen_once": 0,
            "seen_twice": 0,
            "exhausted": 0
        }

# Serve static files (frontend)
# app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
# app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "frontend" / "static")), name="static")
app.mount("/", StaticFiles(directory=str(BASE_DIR / "frontend"), html=True), name="frontend")