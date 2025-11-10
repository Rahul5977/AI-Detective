from flask import Flask, request, jsonify
from flask_cors import CORS
from your_csp_module import solve_csp  # Import your CSP solver here

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# In-memory storage for game sessions
game_sessions = {}

@app.route('/api/start_game', methods=['POST'])
def start_game():
    data = request.json
    session_id = data.get('session_id')
    
    # Initialize a new game state
    game_state = {
        'session_id': session_id,
        'available_actions': [],
        'actions_taken': [],
        'current_domains': {},  # Add this line
        'total_cost': 0,  # Add this line
        'ai_state': None  # Add this line
    }
    
    # Store the initial game state
    game_sessions[session_id] = game_state
    
    return jsonify({
        'success': True,
        'game_state': game_state,
        'available_actions': game_state['available_actions']
    })

@app.route('/api/take_action', methods=['POST'])
def take_action():
    data = request.json
    session_id = data.get('session_id')
    evidence_id = data.get('evidence_id')
    
    # Apply the action
    evidence = apply_action(session_id, evidence_id)
    
    if evidence is None:
        return jsonify({'success': False}), 400
    
    # Solve CSP after action
    csp_result = solve_csp(game_sessions[session_id])
    
    return jsonify({
        'success': True,
        'game_state': game_sessions[session_id],
        'available_actions': game_sessions[session_id]['available_actions'],
        'evidence': evidence,
        'csp_result': csp_result  # Return CSP result
    })

@app.route('/api/ai_move', methods=['POST'])
def ai_move():
    data = request.json
    session_id = data.get('session_id')
    
    # AI logic here (similar to your existing code)
    # For now, let's just return a dummy action
    if session_id in game_sessions:
        game_state = game_sessions[session_id]
        if game_state['available_actions']:
            action = game_state['available_actions'][0]  # Pick the first available action
            return jsonify({
                'success': True,
                'action_taken': action
            })
    
    return jsonify({'success': False}), 400

@app.route('/api/accuse', methods=['POST'])
def accuse():
    data = request.json
    session_id = data.get('session_id')
    guess = data.get('guess')
    
    # Check the guess (dummy logic for now)
    if session_id in game_sessions:
        game_state = game_sessions[session_id]
        correct = (guess == "correct_solution")  # Replace with your logic
        return jsonify({
            'success': True,
            'correct': correct
        })
    
    return jsonify({'success': False}), 400

def get_game_state(session_id):
    """
    Get current game state for a session
    Add this helper function if it doesn't exist
    """
    if session_id in game_sessions:
        return game_sessions[session_id]
    return None

def apply_action(session_id, evidence_id):
    """
    Apply an action and return the evidence
    Add this helper function if it doesn't exist
    """
    if session_id not in game_sessions:
        return None
    
    game_state = game_sessions[session_id]
    
    # Find the evidence
    evidence = next((e for e in game_state['available_actions'] if e['id'] == evidence_id), None)
    
    if not evidence:
        return None
    
    # Apply the evidence (your existing logic)
    # Remove from available actions
    game_state['available_actions'] = [a for a in game_state['available_actions'] if a['id'] != evidence_id]
    
    # Update constraints and domains
    game_state['actions_taken'].append(evidence)
    game_state['total_cost'] += evidence['cost']
    
    # Apply CSP logic here (use your existing CSP solver)
    # ...
    
    return evidence

if __name__ == '__main__':
    app.run(port=5002)