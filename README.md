# Jeopardy Trainer - Knowledge Muscle Memory Exerciser

Interview prep tool for Go, Kubernetes, and Linux. Uses smart question rotation to exercise memory retrieval pathways without overexposure.

## Features

- **Three domains:** Gopardy (Go), Kuberpardy (K8s), Jeolinux (Linux)
- **Smart rotation:** Questions shown 2-3 times max before cycling
- **Mixed question types:** Multiple choice, fill-in-the-blank, scenarios
- **Exam mode:** Answer all 10, then see results with explanations
- **Minimal UI:** Color-coded domains, clean design for focus
- **Session tracking:** SQLite tracks exposure, prioritizes unseen questions

## Quick Start

### 1. Project Structure

```
jeopardy-trainer/
├── backend/
│   ├── main.py              # FastAPI app
│   └── data/
│       ├── gopardy-questions.md
│       ├── kuberpardy-questions.md
│       └── jeolinux-questions.md
├── frontend/
│   ├── index.html
│   └── static/
│       ├── style.css
│       └── app.js
├── tracker.db               # Created automatically
├── requirements.txt
└── README.md
```

### 2. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install FastAPI + uvicorn
pip install fastapi uvicorn[standard]

# Save for future
pip freeze > requirements.txt
```

### 3. Setup Files

Create the directory structure:

```bash
mkdir -p jeopardy-trainer/backend/data
mkdir -p jeopardy-trainer/frontend/static
cd jeopardy-trainer
```

Copy the artifacts into these locations:
- `main.py` → `backend/main.py`
- Question banks → `backend/data/` (3 markdown files)
- `index.html` → `frontend/index.html`
- `style.css` → `frontend/static/style.css`
- `app.js` → `frontend/static/app.js`

### 4. Run the App

```bash
# From jeopardy-trainer directory
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Access at: **http://localhost:8000/index.html**

## Usage

1. **Select domain** - Click Gopardy, Kuberpardy, or Jeolinux
2. **Answer 10 questions** - Navigate with Previous/Next
3. **Submit** - See score + detailed explanations
4. **Repeat** - Questions rotate smartly (unseen first, then seen 1x, then 2x)

## Question Bank Stats

**MVP (v1.0):**
- Gopardy: 30 questions (15 basic, 10 intermediate, 5 gotcha)
- Kuberpardy: 30 questions (15 basic, 10 intermediate, 5 gotcha)
- Jeolinux: 30 questions (15 basic, 10 intermediate, 5 gotcha)
- **Total: 90 questions**

**Roadmap:**
- Target 80+ per domain (240+ total)
- Community contributions welcome

## API Endpoints

### POST `/session/start`
Start new quiz session.

**Request:**
```json
{
  "domain": "go",
  "count": 10
}
```

**Response:**
```json
{
  "domain": "go",
  "questions": [
    {
      "id": "go-Q001",
      "type": "multiple-choice",
      "difficulty": "basic",
      "question": "What's the zero value of a string?",
      "options": ["A) null", "B) \"\"", "C) nil", "D) undefined"]
    }
  ],
  "count": 10
}
```

### POST `/session/submit`
Submit answers and get results.

**Request:**
```json
{
  "domain": "go",
  "answers": [
    {
      "question_id": "go-Q001",
      "user_answer": "B"
    }
  ]
}
```

**Response:**
```json
{
  "score": 7,
  "total": 10,
  "percentage": 70.0,
  "results": [
    {
      "question_id": "go-Q001",
      "is_correct": true,
      "user_answer": "B",
      "correct_answer": "B",
      "explanation": "Go initializes strings to empty string..."
    }
  ]
}
```

### GET `/stats/{domain}`
Get question exposure statistics.

**Response:**
```json
{
  "domain": "go",
  "total_questions": 30,
  "unseen": 25,
  "seen_once": 3,
  "seen_twice": 2,
  "exhausted": 0
}
```

## Adding Questions

Questions use simple markdown format:

```markdown
## Q031 [intermediate] [fill-blank]
**Question:** Complete the command to build Go binary:

```bash
go ___ -o app .
```

**Answer:** build
**Explanation:** `go build` compiles Go code into executable binary.

---
```

**Tags:**
- Difficulty: `[basic]` `[intermediate]` `[gotcha]`
- Type: `[multiple-choice]` `[fill-blank]` `[scenario]`

## Question Rotation Logic

1. **First pass:** Prioritize unseen questions
2. **Second pass:** Include questions seen once
3. **Third pass:** Include questions seen twice
4. **After 3 exposures:** Question rests (no longer selected)

This prevents memorization while ensuring coverage.

## Docker Deployment (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY frontend/ ./frontend/

WORKDIR /app/backend

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t jeopardy-trainer .
docker run -p 8000:8000 -v $(pwd)/tracker.db:/app/backend/tracker.db jeopardy-trainer
```

## Kubernetes Deployment (Optional)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jeopardy-trainer
spec:
  replicas: 1
  selector:
    matchLabels:
      app: jeopardy-trainer
  template:
    metadata:
      labels:
        app: jeopardy-trainer
    spec:
      containers:
      - name: app
        image: jeopardy-trainer:latest
        ports:
        - containerPort: 8000
        volumeMounts:
        - name: data
          mountPath: /app/backend/tracker.db
          subPath: tracker.db
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: jeopardy-data
---
apiVersion: v1
kind: Service
metadata:
  name: jeopardy-trainer
spec:
  type: NodePort
  ports:
  - port: 8000
    targetPort: 8000
    nodePort: 30080
  selector:
    app: jeopardy-trainer
```

## Contributing

Want to add questions? Fork and submit PR with:
1. New questions following markdown format
2. Mix of difficulty levels
3. Clear explanations
4. Test locally first

## License

MIT - Use freely, share widely, help others learn.

## Credits

Built for interview prep. Inspired by the need for **memory muscle training** vs passive reading.

**Philosophy:** You already have the knowledge. This trains your brain to retrieve it faster under pressure.

---

**Good luck with your interviews! 🚀**