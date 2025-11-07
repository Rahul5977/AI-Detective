# 🕵️ AI Detective - Frontend

Beautiful web interface for the CSP-Based Detective AI system.

## Features

- 🎮 **Interactive Investigation** - Click to discover evidence and solve the case
- 🤖 **AI Suggestions** - Get optimal next actions using A\* search algorithm
- 🧠 **Minimax Strategy** - Find best interrogation questions using game tree search
- 🧩 **CSP Visualization** - See constraint propagation in real-time
- 📊 **Live Statistics** - Track costs, actions, and possible solutions
- ⚖️ **Make Accusations** - Submit your final answer when ready

## How to Use

### 1. Start the Backend Server

First, make sure the backend is running:

```bash
cd backend
source ../venv/bin/activate  # Activate virtual environment
python app.py
```

The backend will run on `http://localhost:5001`

### 2. Open the Frontend

Simply open `index.html` in your web browser:

```bash
cd frontend
open index.html  # macOS
# or just double-click index.html
```

### 3. Play the Game

1. Click **"Start New Game"** to begin
2. Investigate evidence by clicking "Investigate" buttons
3. Use **"Get AI Suggestion"** to see optimal next actions (A\* algorithm)
4. Use **"Best Question"** to see optimal interrogation strategy (Minimax)
5. Watch the CSP domains narrow down as you gather evidence
6. Make your accusation when you've solved the case!

## Game Strategy

- **Lower cost actions** are cheaper but may provide less information
- **A\* search** helps find the optimal investigation path
- **Watch the domains** - when each narrows to 1 value, you've solved it!
- **Minimax** shows best interrogation questions based on expected utility

## Technologies Used

- Pure HTML5, CSS3, and JavaScript (Vanilla JS)
- Fetch API for backend communication
- Modern CSS Grid and Flexbox layouts
- Responsive design for mobile and desktop
- Beautiful gradient UI with smooth animations

## API Endpoints Used

- `POST /api/game/start` - Initialize new game
- `POST /api/game/action` - Take investigation action
- `POST /api/ai/suggest` - Get A\* suggestion
- `POST /api/ai/minimax` - Get Minimax suggestion
- `POST /api/interrogation/ask` - Ask interrogation question
- `POST /api/game/accuse` - Make final accusation

## Enjoy Solving Mysteries! 🔍
