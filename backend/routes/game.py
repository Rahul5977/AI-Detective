from flask import Blueprint, request, jsonify
import random
from algorithms.csp_solver import CSPSolver

game_bp = Blueprint('game', __name__)

# Global game sessions storage
game_sessions = {}

# Game data
SUSPECTS = ["Butler", "Chef", "Gardener"]
WEAPONS = ["Knife", "Poison", "Rope"]
LOCATIONS = ["Kitchen", "Library", "Garden"]

EVIDENCE_LIST = [
    {"id": 1, "action": "Question the Butler", "cost": 5},
    {"id": 2, "action": "Search the Kitchen", "cost": 8},
    {"id": 3, "action": "Examine the Knife", "cost": 6},
    {"id": 4, "action": "Question the Chef", "cost": 5},
    {"id": 5, "action": "Search the Library", "cost": 8},
    {"id": 6, "action": "Examine the Poison", "cost": 6},
    {"id": 7, "action": "Question the Gardener", "cost": 5},
    {"id": 8, "action": "Search the Garden", "cost": 8},
    {"id": 9, "action": "Examine the Rope", "cost": 6},
    {"id": 10, "action": "Check alibis", "cost": 10},
    {"id": 11, "action": "Review security footage", "cost": 12},
    {"id": 12, "action": "Analyze fingerprints", "cost": 10},
]

def generate_clues(solution):
    """Generate clues based on solution"""
    clues = {}
    
    for evidence in EVIDENCE_LIST:
        action = evidence["action"].lower()
        clue_text = ""
        
        if "butler" in action:
            if solution["suspect"] == "Butler":
                clue_text = "The Butler seems nervous and avoids eye contact."
            else:
                clue_text = "The Butler has a solid alibi."
        elif "chef" in action:
            if solution["suspect"] == "Chef":
                clue_text = "The Chef was seen near the crime scene."
            else:
                clue_text = "The Chef was in the kitchen all evening."
        elif "gardener" in action:
            if solution["suspect"] == "Gardener":
                clue_text = "The Gardener's tools are missing."
            else:
                clue_text = "The Gardener was working outside."
        elif "kitchen" in action:
            if solution["location"] == "Kitchen":
                clue_text = "Signs of struggle found in the Kitchen."
            else:
                clue_text = "The Kitchen appears undisturbed."
        elif "library" in action:
            if solution["location"] == "Library":
                clue_text = "Books are scattered in the Library."
            else:
                clue_text = "The Library is pristine."
        elif "garden" in action:
            if solution["location"] == "Garden":
                clue_text = "Footprints found in the Garden."
            else:
                clue_text = "The Garden shows no signs of disturbance."
        elif "knife" in action:
            if solution["weapon"] == "Knife":
                clue_text = "The Knife has traces of blood."
            else:
                clue_text = "The Knife is clean."
        elif "poison" in action:
            if solution["weapon"] == "Poison":
                clue_text = "Poison bottle found partially empty."
            else:
                clue_text = "Poison bottle is sealed and full."
        elif "rope" in action:
            if solution["weapon"] == "Rope":
                clue_text = "Rope shows signs of recent use."
            else:
                clue_text = "The Rope is neatly coiled and unused."
        elif "alibi" in action:
            clue_text = f"One suspect's alibi doesn't check out."
        elif "footage" in action:
            clue_text = f"Camera shows someone near the {solution['location']}."
        elif "fingerprint" in action:
            clue_text = f"Fingerprints match someone who frequents the {solution['location']}."
        else:
            clue_text = "Investigation reveals some useful information."
        
        clues[evidence["id"]] = clue_text
    
    return clues

def initialize_game(session_id):
    """Initialize a new game session"""
    solution = {
        "suspect": random.choice(SUSPECTS),
        "weapon": random.choice(WEAPONS),
        "location": random.choice(LOCATIONS)
    }
    
    clues = generate_clues(solution)
    
    game_state = {
        "solution": solution,
        "current_domains": {
            "suspect": SUSPECTS.copy(),
            "weapon": WEAPONS.copy(),
            "location": LOCATIONS.copy()
        },
        "available_actions": [
            {**evidence, "clue": clues[evidence["id"]]} 
            for evidence in EVIDENCE_LIST
        ],
        "actions_taken": [],
        "total_cost": 0,
        "constraints": [],
        "constraints_count": 0,
        "possible_solutions": 27
    }
    
    game_sessions[session_id] = game_state
    return game_state

def get_game_state(session_id):
    """Get current game state"""
    return game_sessions.get(session_id)

def apply_action(session_id, evidence_id):
    """Apply an action and return evidence"""
    game_state = get_game_state(session_id)
    if not game_state:
        return None
    
    # Find the evidence
    evidence = None
    for action in game_state['available_actions']:
        if action['id'] == evidence_id:
            evidence = action
            break
    
    if not evidence:
        return None
    
    # Remove from available actions
    game_state['available_actions'] = [
        a for a in game_state['available_actions'] 
        if a['id'] != evidence_id
    ]
    
    # Add to taken actions
    game_state['actions_taken'].append(evidence)
    game_state['total_cost'] += evidence['cost']
    
    # Apply CSP constraints
    csp_result = apply_csp_constraints(game_state, evidence)
    
    return evidence, csp_result

def apply_csp_constraints(game_state, evidence):
    """Apply CSP constraints based on evidence"""
    clue = evidence['clue'].lower()
    action = evidence['action'].lower()
    solution = game_state['solution']
    
    constraints = []
    steps = []
    
    # Parse clues and create constraints
    if 'nervous' in clue or 'near the crime scene' in clue or 'missing' in clue:
        # Positive indicator - likely the suspect
        if 'butler' in action:
            constraints.append(('suspect', 'Butler', 'confirm'))
            steps.append({
                'step': 'Confirmation',
                'message': f"Strong evidence points to Butler as suspect",
                'type': 'confirmation'
            })
        elif 'chef' in action:
            constraints.append(('suspect', 'Chef', 'confirm'))
            steps.append({
                'step': 'Confirmation',
                'message': f"Strong evidence points to Chef as suspect",
                'type': 'confirmation'
            })
        elif 'gardener' in action:
            constraints.append(('suspect', 'Gardener', 'confirm'))
            steps.append({
                'step': 'Confirmation',
                'message': f"Strong evidence points to Gardener as suspect",
                'type': 'confirmation'
            })
    
    if 'alibi' in clue or 'kitchen all evening' in clue or 'working outside' in clue:
        # Negative indicator - eliminates suspect
        if 'butler' in action:
            constraints.append(('suspect', 'Butler', 'eliminate'))
            steps.append({
                'step': 'Elimination',
                'message': f"Butler eliminated as suspect due to alibi",
                'type': 'elimination'
            })
        elif 'chef' in action:
            constraints.append(('suspect', 'Chef', 'eliminate'))
            steps.append({
                'step': 'Elimination',
                'message': f"Chef eliminated as suspect due to alibi",
                'type': 'elimination'
            })
        elif 'gardener' in action:
            constraints.append(('suspect', 'Gardener', 'eliminate'))
            steps.append({
                'step': 'Elimination',
                'message': f"Gardener eliminated as suspect due to alibi",
                'type': 'elimination'
            })
    
    # Location constraints
    if 'struggle' in clue or 'scattered' in clue or 'footprints' in clue:
        if 'kitchen' in action:
            constraints.append(('location', 'Kitchen', 'confirm'))
            steps.append({
                'step': 'Confirmation',
                'message': f"Evidence confirms Kitchen as crime location",
                'type': 'confirmation'
            })
        elif 'library' in action:
            constraints.append(('location', 'Library', 'confirm'))
            steps.append({
                'step': 'Confirmation',
                'message': f"Evidence confirms Library as crime location",
                'type': 'confirmation'
            })
        elif 'garden' in action:
            constraints.append(('location', 'Garden', 'confirm'))
            steps.append({
                'step': 'Confirmation',
                'message': f"Evidence confirms Garden as crime location",
                'type': 'confirmation'
            })
    
    if 'undisturbed' in clue or 'pristine' in clue or 'no signs' in clue:
        if 'kitchen' in action:
            constraints.append(('location', 'Kitchen', 'eliminate'))
            steps.append({
                'step': 'Elimination',
                'message': f"Kitchen eliminated as crime location",
                'type': 'elimination'
            })
        elif 'library' in action:
            constraints.append(('location', 'Library', 'eliminate'))
            steps.append({
                'step': 'Elimination',
                'message': f"Library eliminated as crime location",
                'type': 'elimination'
            })
        elif 'garden' in action:
            constraints.append(('location', 'Garden', 'eliminate'))
            steps.append({
                'step': 'Elimination',
                'message': f"Garden eliminated as crime location",
                'type': 'elimination'
            })
    
    # Weapon constraints
    if 'blood' in clue or 'empty' in clue or 'recent use' in clue:
        if 'knife' in action:
            constraints.append(('weapon', 'Knife', 'confirm'))
            steps.append({
                'step': 'Confirmation',
                'message': f"Evidence confirms Knife as murder weapon",
                'type': 'confirmation'
            })
        elif 'poison' in action:
            constraints.append(('weapon', 'Poison', 'confirm'))
            steps.append({
                'step': 'Confirmation',
                'message': f"Evidence confirms Poison as murder weapon",
                'type': 'confirmation'
            })
        elif 'rope' in action:
            constraints.append(('weapon', 'Rope', 'confirm'))
            steps.append({
                'step': 'Confirmation',
                'message': f"Evidence confirms Rope as murder weapon",
                'type': 'confirmation'
            })
    
    if 'clean' in clue or 'sealed and full' in clue or 'unused' in clue:
        if 'knife' in action:
            constraints.append(('weapon', 'Knife', 'eliminate'))
            steps.append({
                'step': 'Elimination',
                'message': f"Knife eliminated as murder weapon",
                'type': 'elimination'
            })
        elif 'poison' in action:
            constraints.append(('weapon', 'Poison', 'eliminate'))
            steps.append({
                'step': 'Elimination',
                'message': f"Poison eliminated as murder weapon",
                'type': 'elimination'
            })
        elif 'rope' in action:
            constraints.append(('weapon', 'Rope', 'eliminate'))
            steps.append({
                'step': 'Elimination',
                'message': f"Rope eliminated as murder weapon",
                'type': 'elimination'
            })
    
    # Apply constraints using CSP solver
    if constraints:
        game_state['constraints'].extend(constraints)
        game_state['constraints_count'] = len(game_state['constraints'])
        
        # Update domains
        for category, value, action_type in constraints:
            if action_type == 'eliminate':
                if value in game_state['current_domains'][category]:
                    game_state['current_domains'][category].remove(value)
            elif action_type == 'confirm':
                if len(game_state['current_domains'][category]) > 1:
                    game_state['current_domains'][category] = [value]
        
        # Use CSP solver for additional inference
        solver = CSPSolver(
            game_state['current_domains'],
            game_state['constraints']
        )
        solver.solve()
        additional_steps = solver.get_steps()
        steps.extend(additional_steps)
        
        # Update domains from solver
        game_state['current_domains'] = solver.domains
    
    # Calculate possible solutions
    game_state['possible_solutions'] = (
        len(game_state['current_domains']['suspect']) *
        len(game_state['current_domains']['weapon']) *
        len(game_state['current_domains']['location'])
    )
    
    return {
        'constraints_applied': len(constraints),
        'steps': steps
    }

@game_bp.route('/start', methods=['POST'])
def start_game():
    """Start a new game"""
    try:
        data = request.json
        session_id = data.get('session_id', f"session-{random.randint(1000, 9999)}")
        
        game_state = initialize_game(session_id)
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'game_state': {
                'current_domains': game_state['current_domains'],
                'total_cost': game_state['total_cost'],
                'actions_taken': game_state['actions_taken'],
                'possible_solutions': game_state['possible_solutions'],
                'constraints_count': game_state['constraints_count']
            },
            'available_actions': [
                {
                    'id': action['id'],
                    'action': action['action'],
                    'cost': action['cost']
                }
                for action in game_state['available_actions']
            ]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@game_bp.route('/action', methods=['POST'])
def take_action():
    """Take an investigation action"""
    try:
        data = request.json
        session_id = data.get('session_id')
        evidence_id = data.get('evidence_id')
        
        if not session_id or evidence_id is None:
            return jsonify({
                'success': False,
                'message': 'Missing session_id or evidence_id'
            }), 400
        
        result = apply_action(session_id, evidence_id)
        
        if not result:
            return jsonify({
                'success': False,
                'message': 'Action not found or session invalid'
            }), 404
        
        evidence, csp_result = result
        game_state = get_game_state(session_id)
        
        return jsonify({
            'success': True,
            'evidence': {
                'id': evidence['id'],
                'action': evidence['action'],
                'clue': evidence['clue'],
                'cost': evidence['cost']
            },
            'csp_result': csp_result,
            'game_state': {
                'current_domains': game_state['current_domains'],
                'total_cost': game_state['total_cost'],
                'actions_taken': game_state['actions_taken'],
                'possible_solutions': game_state['possible_solutions'],
                'constraints_count': game_state['constraints_count']
            },
            'available_actions': [
                {
                    'id': action['id'],
                    'action': action['action'],
                    'cost': action['cost']
                }
                for action in game_state['available_actions']
            ]
        })
    except Exception as e:
        import traceback
        print(f"Error in take_action: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@game_bp.route('/accuse', methods=['POST'])
def make_accusation():
    """Make final accusation"""
    try:
        data = request.json
        session_id = data.get('session_id')
        guess = data.get('guess')
        
        if not session_id or not guess:
            return jsonify({
                'success': False,
                'message': 'Missing session_id or guess'
            }), 400
        
        game_state = get_game_state(session_id)
        if not game_state:
            return jsonify({
                'success': False,
                'message': 'Game session not found'
            }), 404
        
        solution = game_state['solution']
        correct = (
            guess['suspect'] == solution['suspect'] and
            guess['weapon'] == solution['weapon'] and
            guess['location'] == solution['location']
        )
        
        return jsonify({
            'success': True,
            'correct': correct,
            'solution': solution,
            'total_cost': game_state['total_cost'],
            'actions_taken': len(game_state['actions_taken'])
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500