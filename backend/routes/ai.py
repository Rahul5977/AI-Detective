from flask import Blueprint, request, jsonify
import copy
from algorithms.csp_solver import CSPSolver

ai_bp = Blueprint('ai', __name__)

# Store AI state per session
ai_sessions = {}

# Forward declaration - will be imported after game module loads
game_sessions = None
get_game_state = None
apply_action = None

def init_game_imports():
    """Initialize imports from game module to avoid circular imports"""
    global game_sessions, get_game_state, apply_action
    if game_sessions is None:
        from routes.game import game_sessions as gs, get_game_state as ggs, apply_action as aa
        game_sessions = gs
        get_game_state = ggs
        apply_action = aa

class AIDetective:
    """AI Detective using A* search and CSP"""
    
    def __init__(self, session_id):
        init_game_imports()
        self.session_id = session_id
        game_state = get_game_state(session_id)
        if not game_state:
            raise ValueError("Invalid session_id")
        self.domains = copy.deepcopy(game_state['current_domains'])
        self.total_cost = 0
        self.actions_taken = 0
        self.algorithm_steps = []
        
    def get_best_action(self):
        """Use A* search to find best action"""
        init_game_imports()
        game_state = get_game_state(self.session_id)
        if not game_state:
            return None, "Game state not found", []
            
        available_actions = game_state.get('available_actions', [])
        
        if not available_actions:
            return None, "No actions available", []
        
        evaluations = []
        best_action = None
        best_f_score = float('inf')
        
        for action in available_actions:
            # g(n): actual cost
            g_cost = self.total_cost + action['cost']
            
            # h(n): heuristic (possible solutions remaining)
            h_cost = self._calculate_heuristic()
            
            # f(n) = g(n) + h(n)
            f_cost = g_cost + h_cost
            
            evaluations.append({
                'action': action['action'],
                'action_id': action['id'],
                'g_cost': g_cost,
                'h_cost': h_cost,
                'f_cost': f_cost
            })
            
            if f_cost < best_f_score:
                best_f_score = f_cost
                best_action = action
        
        evaluations.sort(key=lambda x: x['f_cost'])
        
        explanation = f"Selected '{best_action['action']}' using A* algorithm (F-score: {best_f_score:.1f})"
        
        self.algorithm_steps.append({
            'type': 'search',
            'algorithm': 'A* Search',
            'message': explanation,
            'details': f"Evaluated {len(evaluations)} actions"
        })
        
        return best_action, explanation, evaluations
    
    def _calculate_heuristic(self):
        """Calculate heuristic based on domain sizes"""
        init_game_imports()
        game_state = get_game_state(self.session_id)
        if not game_state:
            return 100
            
        domains = game_state.get('current_domains', {})
        
        # Count possible solutions
        possible = 1
        for values in domains.values():
            possible *= len(values)
        
        # Heuristic: estimate cost to narrow down to 1 solution
        return possible * 2
    
    def update_state(self, evidence, csp_result):
        """Update AI state after taking action"""
        init_game_imports()
        game_state = get_game_state(self.session_id)
        if game_state:
            self.domains = copy.deepcopy(game_state['current_domains'])
        self.total_cost += evidence['cost']
        self.actions_taken += 1
        
        if csp_result and 'steps' in csp_result:
            self.algorithm_steps.extend(csp_result['steps'])
    
    def is_solved(self):
        """Check if case is solved"""
        return all(len(values) == 1 for values in self.domains.values())
    
    def get_solution(self):
        """Get current solution"""
        if self.is_solved():
            return {
                'suspect': self.domains['suspect'][0],
                'weapon': self.domains['weapon'][0],
                'location': self.domains['location'][0]
            }
        return None
    
    def get_confidence(self):
        """Calculate confidence level"""
        init_game_imports()
        game_state = get_game_state(self.session_id)
        if not game_state:
            return 0.0
        possible = game_state.get('possible_solutions', 27)
        return 1.0 - (possible / 27.0)

@ai_bp.route('/make-move', methods=['POST'])
def make_ai_move():
    """AI makes one move"""
    try:
        init_game_imports()
        data = request.json
        session_id = data.get('session_id')
        
        if not session_id:
            return jsonify({
                'success': False,
                'message': 'Missing session_id'
            }), 400
        
        game_state = get_game_state(session_id)
        if not game_state:
            return jsonify({
                'success': False,
                'message': 'No active game found'
            }), 404
        
        # Initialize or get AI detective
        if session_id not in ai_sessions:
            try:
                ai_sessions[session_id] = AIDetective(session_id)
            except ValueError as e:
                return jsonify({
                    'success': False,
                    'message': str(e)
                }), 400
        
        ai_detective = ai_sessions[session_id]
        
        # Check if already solved
        if ai_detective.is_solved():
            return jsonify({
                'success': True,
                'ai_state': {
                    'solved': True,
                    'solution': ai_detective.get_solution(),
                    'total_cost': ai_detective.total_cost,
                    'actions_taken': ai_detective.actions_taken,
                    'possible_solutions': 1,
                    'current_domains': ai_detective.domains,
                    'confidence': 1.0,
                    'algorithm': 'A* Search + CSP'
                },
                'action_taken': None,
                'algorithm_explanation': ai_detective.algorithm_steps[-5:] if ai_detective.algorithm_steps else []
            })
        
        # Get best action
        best_action, explanation, evaluations = ai_detective.get_best_action()
        
        if not best_action:
            return jsonify({
                'success': False,
                'message': 'No available actions'
            }), 400
        
        # Apply the action
        result = apply_action(session_id, best_action['id'])
        
        if not result:
            return jsonify({
                'success': False,
                'message': 'Failed to apply action'
            }), 500
        
        evidence, csp_result = result
        ai_detective.update_state(evidence, csp_result)
        
        # Get next best action
        next_action, _, _ = ai_detective.get_best_action()
        
        # Update game state reference
        updated_game_state = get_game_state(session_id)
        
        return jsonify({
            'success': True,
            'ai_state': {
                'solved': ai_detective.is_solved(),
                'solution': ai_detective.get_solution() if ai_detective.is_solved() else None,
                'total_cost': ai_detective.total_cost,
                'actions_taken': ai_detective.actions_taken,
                'possible_solutions': updated_game_state.get('possible_solutions', 27),
                'current_domains': ai_detective.domains,
                'confidence': ai_detective.get_confidence(),
                'algorithm': 'A* Search + CSP',
                'next_best_action': next_action['action'] if next_action else None
            },
            'action_taken': {
                'action': evidence['action'],
                'clue': evidence['clue'],
                'cost': evidence['cost'],
                'reasoning': explanation
            },
            'algorithm_explanation': ai_detective.algorithm_steps[-5:] if ai_detective.algorithm_steps else []
        })
    except Exception as e:
        import traceback
        print(f"Error in make_ai_move: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@ai_bp.route('/auto-solve', methods=['POST'])
def auto_solve():
    """AI automatically solves the case"""
    try:
        init_game_imports()
        data = request.json
        session_id = data.get('session_id')
        
        if not session_id:
            return jsonify({
                'success': False,
                'message': 'Missing session_id'
            }), 400
        
        game_state = get_game_state(session_id)
        if not game_state:
            return jsonify({
                'success': False,
                'message': 'No active game found'
            }), 404
        
        # Create fresh AI detective instance
        try:
            ai_detective = AIDetective(session_id)
            ai_sessions[session_id] = ai_detective
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400
        
        solution_path = []
        max_iterations = 15
        iteration = 0
        
        while not ai_detective.is_solved() and iteration < max_iterations:
            iteration += 1
            
            best_action, explanation, _ = ai_detective.get_best_action()
            if not best_action:
                break
            
            result = apply_action(session_id, best_action['id'])
            if not result:
                break
            
            evidence, csp_result = result
            ai_detective.update_state(evidence, csp_result)
            
            solution_path.append({
                'step': iteration,
                'action': evidence['action'],
                'clue': evidence['clue'],
                'cost': evidence['cost'],
                'reasoning': explanation,
                'type': 'search',
                'algorithm': 'A* + CSP',
                'message': f"Step {iteration}: {evidence['action']}",
                'details': explanation
            })
        
        final_game_state = get_game_state(session_id)
        
        return jsonify({
            'success': True,
            'solved': ai_detective.is_solved(),
            'solution': ai_detective.get_solution(),
            'steps_taken': ai_detective.actions_taken,
            'total_cost': ai_detective.total_cost,
            'solution_path': solution_path,
            'final_domains': final_game_state.get('current_domains', {})
        })
    except Exception as e:
        import traceback
        print(f"Error in auto-solve: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@ai_bp.route('/suggest', methods=['POST'])
def get_suggestion():
    """Get AI suggestion for next action"""
    try:
        init_game_imports()
        data = request.json
        session_id = data.get('session_id')
        
        if not session_id:
            return jsonify({
                'success': False,
                'message': 'Missing session_id'
            }), 400
        
        game_state = get_game_state(session_id)
        if not game_state:
            return jsonify({
                'success': False,
                'message': 'No active game found'
            }), 404
        
        try:
            ai_detective = AIDetective(session_id)
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400
            
        best_action, explanation, evaluations = ai_detective.get_best_action()
        
        if not best_action:
            return jsonify({
                'success': False,
                'message': 'No actions available'
            }), 400
        
        return jsonify({
            'success': True,
            'suggestion': {
                'action': best_action['action'],
                'explanation': explanation,
                'cost': best_action['cost']
            },
            'all_evaluations': evaluations
        })
    except Exception as e:
        import traceback
        print(f"Error in get_suggestion: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500
