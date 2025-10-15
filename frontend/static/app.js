// State management
let currentDomain = null;
let questions = [];
let currentQuestionIndex = 0;
let userAnswers = {};

// Page elements
const landingPage = document.getElementById('landing-page');
const gamePage = document.getElementById('game-page');
const resultsPage = document.getElementById('results-page');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadStats();
    setupEventListeners();
});

// Load stats for all domains
async function loadStats() {
    const domains = ['go', 'k8s', 'linux'];
    
    for (const domain of domains) {
        try {
            const response = await fetch(`/stats/${domain}`);
            const data = await response.json();
            
            const statsEl = document.getElementById(`stats-${domain}`);
            statsEl.textContent = `${data.unseen} unseen • ${data.seen_once + data.seen_twice} active`;
        } catch (error) {
            console.error(`Failed to load stats for ${domain}:`, error);
        }
    }
}

// Event listeners
function setupEventListeners() {
    // Domain selection
    document.querySelectorAll('.domain-card').forEach(card => {
        card.addEventListener('click', () => {
            const domain = card.dataset.domain;
            startSession(domain);
        });
    });
    
    // Navigation
    document.getElementById('prev-btn').addEventListener('click', () => {
        navigateQuestion(-1);
    });
    
    document.getElementById('next-btn').addEventListener('click', () => {
        navigateQuestion(1);
    });
    
    document.getElementById('submit-btn').addEventListener('click', () => {
        submitSession();
    });
    
    // Results actions
    document.getElementById('retry-btn').addEventListener('click', () => {
        startSession(currentDomain);
    });
    
    document.getElementById('home-btn').addEventListener('click', () => {
        showPage('landing');
        loadStats();
    });
}

// Start new session
async function startSession(domain) {
    currentDomain = domain;
    userAnswers = {};
    currentQuestionIndex = 0;
    
    // Apply domain theme
    document.body.className = `domain-${domain}`;
    
    try {
        const response = await fetch('/session/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ domain, count: 10 })
        });
        
        const data = await response.json();
        questions = data.questions;
        
        // Update title
        const titles = {
            go: 'Gopardy',
            k8s: 'Kuberpardy',
            linux: 'Jeolinux'
        };
        document.getElementById('game-title').textContent = titles[domain];
        
        showPage('game');
        displayQuestion(0);
    } catch (error) {
        console.error('Failed to start session:', error);
        alert('Failed to start session. Please try again.');
    }
}

// Display question
function displayQuestion(index) {
    const question = questions[index];
    
    // Update counter
    document.getElementById('question-counter').textContent = `${index + 1}/${questions.length}`;
    
    // Update badges
    const difficultyBadge = document.getElementById('difficulty-badge');
    difficultyBadge.textContent = question.difficulty;
    difficultyBadge.className = `difficulty-badge ${question.difficulty}`;
    
    document.getElementById('type-badge').textContent = question.type;
    
    // Update question text
    document.getElementById('question-text').innerHTML = marked.parse(question.question);
    
    // Clear and setup answer area
    const mcOptions = document.getElementById('mc-options');
    const fillBlank = document.getElementById('fill-blank');
    
    if (question.type === 'multiple-choice') {
        mcOptions.classList.remove('hidden');
        fillBlank.classList.add('hidden');
        
        // Generate options
        mcOptions.innerHTML = '';
        question.options.forEach(option => {
            const optionEl = document.createElement('label');
            optionEl.className = 'mc-option';
            
            const radio = document.createElement('input');
            radio.type = 'radio';
            radio.name = 'answer';
            radio.value = option.charAt(0); // A, B, C, D
            
            // Restore previous answer
            if (userAnswers[question.id] === option.charAt(0)) {
                radio.checked = true;
                optionEl.classList.add('selected');
            }
            
            radio.addEventListener('change', () => {
                // Update UI
                document.querySelectorAll('.mc-option').forEach(opt => {
                    opt.classList.remove('selected');
                });
                optionEl.classList.add('selected');
                
                // Save answer
                userAnswers[question.id] = radio.value;
            });
            
            optionEl.appendChild(radio);
            optionEl.appendChild(document.createTextNode(option));
            mcOptions.appendChild(optionEl);
        });
    } else {
        mcOptions.classList.add('hidden');
        fillBlank.classList.remove('hidden');
        
        const input = document.getElementById('fill-answer');
        input.value = userAnswers[question.id] || '';
        
        input.oninput = () => {
            userAnswers[question.id] = input.value;
        };
        
        // Focus input
        setTimeout(() => input.focus(), 100);
    }
    
    // Update navigation buttons
    document.getElementById('prev-btn').disabled = index === 0;
    
    const nextBtn = document.getElementById('next-btn');
    const submitBtn = document.getElementById('submit-btn');
    
    if (index === questions.length - 1) {
        nextBtn.classList.add('hidden');
        submitBtn.classList.remove('hidden');
    } else {
        nextBtn.classList.remove('hidden');
        submitBtn.classList.add('hidden');
    }
}

// Navigate questions
function navigateQuestion(direction) {
    const newIndex = currentQuestionIndex + direction;
    
    if (newIndex >= 0 && newIndex < questions.length) {
        currentQuestionIndex = newIndex;
        displayQuestion(newIndex);
    }
}

// Submit session
async function submitSession() {
    // Build submission
    const answers = questions.map(q => ({
        question_id: q.id,
        user_answer: userAnswers[q.id] || ''
    }));
    
    try {
        const response = await fetch('/session/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                domain: currentDomain,
                answers
            })
        });
        
        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('Failed to submit session:', error);
        alert('Failed to submit answers. Please try again.');
    }
}

// Display results
function displayResults(data) {
    // Update score
    document.getElementById('score-text').textContent = `${data.score}/${data.total}`;
    document.getElementById('score-percent').textContent = `${data.percentage}%`;
    
    // Update title
    const titles = {
        go: 'Gopardy Results',
        k8s: 'Kuberpardy Results',
        linux: 'Jeolinux Results'
    };
    document.getElementById('results-title').textContent = titles[currentDomain];
    
    // Generate results list
    const resultsList = document.getElementById('results-list');
    resultsList.innerHTML = '';
    
    data.results.forEach((result, index) => {
        const item = document.createElement('div');
        item.className = `result-item ${result.is_correct ? 'correct' : 'incorrect'}`;
        
        const header = document.createElement('div');
        header.className = 'result-header';
        
        const questionNum = document.createElement('span');
        questionNum.textContent = `Question ${index + 1}`;
        
        const status = document.createElement('span');
        status.className = `result-status ${result.is_correct ? 'correct' : 'incorrect'}`;
        status.textContent = result.is_correct ? '✅ Correct' : '❌ Incorrect';
        
        header.appendChild(questionNum);
        header.appendChild(status);
        
        const questionText = document.createElement('div');
        questionText.className = 'result-question';
        questionText.innerHTML = marked.parse(result.question);
        
        const answers = document.createElement('div');
        answers.className = 'result-answers';
        
        if (!result.is_correct) {
            const userAnswer = document.createElement('div');
            userAnswer.className = 'user-answer';
            userAnswer.textContent = `Your answer: ${result.user_answer || '(no answer)'}`;
            answers.appendChild(userAnswer);
        }
        
        const correctAnswer = document.createElement('div');
        correctAnswer.className = 'correct-answer';
        correctAnswer.textContent = `Correct answer: ${result.correct_answer}`;
        answers.appendChild(correctAnswer);
        
        const explanation = document.createElement('div');
        explanation.className = 'result-explanation';
        explanation.textContent = result.explanation;
        
        item.appendChild(header);
        item.appendChild(questionText);
        item.appendChild(answers);
        item.appendChild(explanation);
        
        resultsList.appendChild(item);
    });
    
    showPage('results');
}

// Page navigation
function showPage(page) {
    landingPage.classList.remove('active');
    gamePage.classList.remove('active');
    resultsPage.classList.remove('active');
    
    if (page === 'landing') {
        landingPage.classList.add('active');
        document.body.className = '';
    } else if (page === 'game') {
        gamePage.classList.add('active');
    } else if (page === 'results') {
        resultsPage.classList.add('active');
    }
}