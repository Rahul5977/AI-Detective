from flask import Blueprint, request, jsonify
import heapq
from typing import Dict, List, Tuple
import copy

ai_detective_bp = Blueprint('ai_detective', __name__)

# Store AI state per session
ai_sessions = {}

class AIDetective:
    """AI Detective using A* search and CSP with enhanced heuristics"""
    
    def __init__(self, game_state, available_actions, solution):
        self.domains = copy.deepcopy(game_state['current_domains'])
        self.available_actions = copy.deepcopy(available_actions)
        self.solution = solution
        self.total_cost = 0
        self.actions_taken = []
        self.possible_solutions = self._count_solutions()
        self.algorithm_steps = []
        
    def _count_solutions(self):
        """Count possible solutions from current domains"""
        count = 1
        for values in self.domains.values():
            count *= len(values)
        return count
    
    def _heuristic(self, domains):
        """
        Enhanced heuristic for A* search
        Estimates cost to reach solution from current state
        """
        # H1: Remaining uncertainty (number of possible solutions)
        solutions_left = 1
        for values in domains.values():
            solutions_left *= len(values)
        
        # H2: Average domain size (prefer smaller domains)
        avg_domain_size = sum(len(v) for v in domains.values()) / len(domains)
        
        # H3: Unresolved categories (categories with multiple possibilities)
        unresolved = sum(1 for v in domains.values() if len(v) > 1)
        
        # Combined heuristic (weighted)
        h = (solutions_left * 2) + (avg_domain_size * 5) + (unresolved * 10)
        return h
    
    def _information_gain(self, action, current_domains):
        """
        Calculate expected information gain from an action
        Uses entropy-based approach
        """
        import math
        
        # Calculate current entropy
        current_entropy = 0
        for values in current_domains.values():
            if len(values) > 0:
                p = 1.0 / len(values)
                current_entropy -= len(values) * p * math.log2(p) if p > 0 else 0
        
        # Estimate expected entropy after action
        # (simplified - assumes action will eliminate some possibilities)
        expected_reduction = len(action.get('eliminates', [])) * 0.5
        
        # Information gain = current entropy - expected entropy after action
        info_gain = expected_reduction / (action['cost'] + 1)  # Normalize by cost
        
        return info_gain
    
    def get_best_action(self):
        """
        Use A* search to find the best next action
        Returns: (action, explanation, all_evaluations)
        """
        if not self.available_actions:
            return None, "No actions available", []
        
        evaluations = []
        best_action = None
        best_f_score = float('inf')
        
        for action in self.available_actions:
            # Simulate taking this action
            simulated_domains = copy.deepcopy(self.domains)
            
            # g(n): actual cost so far + action cost
            g_cost = self.total_cost + action['cost']
            
            # h(n): heuristic estimate to goal
            h_cost = self._heuristic(simulated_domains)
            
            # Information gain bonus
            info_gain = self._information_gain(action, self.domains)
            
            # f(n) = g(n) + h(n) - information_gain_bonus
            f_cost = g_cost + h_cost - (info_gain * 20)
            
            evaluations.append({
                'action': action['action'],
                'action_id': action['id'],
                'g_cost': g_cost,
                'h_cost': h_cost,
                'info_gain': info_gain,
                'f_cost': f_cost
            })
            
            if f_cost < best_f_score:
                best_f_score = f_cost
                best_action = action
        
        # Sort evaluations by f_cost
        evaluations.sort(key=lambda x: x['f_cost'])
        
        explanation = f"Selected '{best_action['action']}' using A* algorithm. " \
                     f"F-score: {best_f_score:.2f} (Cost: {best_action['cost']}, " \
                     f"Heuristic: {self._heuristic(self.domains):.2f})"
        
        self.algorithm_steps.append({
            'type': 'search',
            'algorithm': 'A* Search',
            'message': explanation,
            'details': f"Evaluated {len(evaluations)} possible actions"
        })
        
        return best_action, explanation, evaluations
    
    def apply_csp_constraints(self, evidence):
        """
        Apply CSP constraints based on evidence
        Uses arc consistency and forward checking
        """
        steps = []
        
        # Parse the clue
        clue = evidence['clue'].lower()
        
        # Extract constraint information
        if 'not' in clue or 'wasn\'t' in clue or 'didn\'t' in clue:
            # Elimination constraint
            for category in self.domains:
                for value in list(self.domains[category]):
                    if value.lower() in clue:
                        if len(self.domains[category]) > 1:
                            self.domains[category].remove(value)
                            steps.append({
                                'type': 'elimination',
                                'algorithm': 'CSP - Arc Consistency',
                                'message': f"Eliminated {value} from {category}",
                                'details': f"Clue indicated: {clue}"
                            })
        else:
            # Confirmation or implication constraint
            for category in self.domains:
                for value in list(self.domains[category]):
                    if value.lower() in clue:
                        if len(self.domains[category]) > 1:
                            self.domains[category] = [value]
                            steps.append({
                                'type': 'confirmation',
                                'algorithm': 'CSP - Domain Reduction',
                                'message': f"Confirmed {value} as {category}",
                                'details': f"Clue indicated: {clue}"
                            })
        
        # Forward checking - check if this creates new constraints
        self._forward_check(steps)
        
        self.possible_solutions = self._count_solutions()
        return steps
    
    def _forward_check(self, steps):
        """
        Forward checking to propagate constraints
        """
        # Check if any domain is solved (has one value)
        for category, values in self.domains.items():
            if len(values) == 1:
                solved_value = values[0]
                # Remove this value from other categories if applicable
                for other_cat, other_vals in self.domains.items():
                    if other_cat != category and solved_value in other_vals and len(other_vals) > 1:
                        other_vals.remove(solved_value)
                        steps.append({
                            'type': 'elimination',
                            'algorithm': 'CSP - Forward Checking',
                            'message': f"Eliminated {solved_value} from {other_cat} (already assigned to {category})",
                            'details': 'Constraint propagation'
                        })
    
    def is_solved(self):
        """Check if the case is solved"""
        return all(len(values) == 1 for values in self.domains.values())
    
    def get_solution(self):
        """Get the current solution"""
        if self.is_solved():
            return {
                'suspect': self.domains['suspect'][0],
                'weapon': self.domains['weapon'][0],
                'location': self.domains['location'][0]
            }
        return None

@ai_detective_bp.route('/make-move', methods=['POST'])
def make_ai_move():
    """AI makes one move in the investigation"""
    try:
        data = request.json
        session_id = data.get('session_id')
        
        # Import game state (you'll need to adapt this to your game management)
        from routes.game import get_game_state, apply_action
        
        game_state = get_game_state(session_id)
        if not game_state:
            return jsonify({
                'success': False,
                'message': 'No active game found'
            })
        
        # Initialize or get AI detective for this session
        if session_id not in ai_sessions:
            ai_sessions[session_id] = AIDetective(
                game_state,
                game_state.get('available_actions', []),
                game_state.get('solution')
            )
        
        ai_detective = ai_sessions[session_id]
        
        # Check if already solved
        if ai_detective.is_solved():
            return jsonify({
                'success': True,
                'ai_state': {
                    'solved': True,
                    'solution': ai_detective.get_solution(),
                    'total_cost': ai_detective.total_cost,
                    'actions_taken': len(ai_detective.actions_taken),
                    'possible_solutions': 1,
                    'current_domains': ai_detective.domains,
                    'confidence': 1.0,
                    'algorithm': 'A* Search + CSP'
                },
                'action_taken': None,
                'algorithm_explanation': ai_detective.algorithm_steps
            })
        
        # Get best action using A*
        best_action, explanation, evaluations = ai_detective.get_best_action()
        
        if not best_action:
            return jsonify({
                'success': False,
                'message': 'No available actions'
            })
        
        # Apply the action (simulate taking it)
        evidence = apply_action(session_id, best_action['id'])
        
        if evidence:
            # Update AI state
            ai_detective.total_cost += best_action['cost']
            ai_detective.actions_taken.append(evidence)
            
            # Apply CSP constraints
            csp_steps = ai_detective.apply_csp_constraints(evidence)
            ai_detective.algorithm_steps.extend(csp_steps)
            
            # Update available actions
            updated_game_state = get_game_state(session_id)
            ai_detective.available_actions = updated_game_state.get('available_actions', [])
            
            # Calculate confidence
            confidence = 1.0 - (ai_detective.possible_solutions / 27.0)
            
            # Get next best action for display
            next_action, _, _ = ai_detective.get_best_action()
            
            return jsonify({
                'success': True,
                'ai_state': {
                    'solved': ai_detective.is_solved(),
                    'solution': ai_detective.get_solution() if ai_detective.is_solved() else None,
                    'total_cost': ai_detective.total_cost,
                    'actions_taken': len(ai_detective.actions_taken),
                    'possible_solutions': ai_detective.possible_solutions,
                    'current_domains': ai_detective.domains,
                    'confidence': confidence,
                    'algorithm': 'A* Search + CSP',
                    'next_best_action': next_action['action'] if next_action else None
                },
                'action_taken': {
                    'action': evidence['action'],
                    'clue': evidence['clue'],
                    'cost': evidence['cost'],
                    'reasoning': explanation
                },
                'algorithm_explanation': ai_detective.algorithm_steps[-5:]  # Last 5 steps
            })
        
        return jsonify({
            'success': False,
            'message': 'Failed to take action'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@ai_detective_bp.route('/auto-solve', methods=['POST'])
def auto_solve():
    """AI automatically solves the entire case"""
    try:
        data = request.json
        session_id = data.get('session_id')
        
        from routes.game import get_game_state, apply_action
        
        game_state = get_game_state(session_id)
        if not game_state:
            return jsonify({
                'success': False,
                'message': 'No active game found'
            })
        
        # Initialize AI detective
        ai_detective = AIDetective(
            game_state,
            game_state.get('available_actions', []),
            game_state.get('solution')
        )
        
        solution_path = []
        max_iterations = 20  # Safety limit
        iteration = 0
        
        while not ai_detective.is_solved() and iteration < max_iterations:
            iteration += 1
            
            # Get best action
            best_action, explanation, _ = ai_detective.get_best_action()
            
            if not best_action:
                break
            
            # Apply action
            evidence = apply_action(session_id, best_action['id'])
            
            if evidence:
                ai_detective.total_cost += best_action['cost']
                ai_detective.actions_taken.append(evidence)
                
                # Apply CSP
                csp_steps = ai_detective.apply_csp_constraints(evidence)
                
                solution_path.append({
                    'step': iteration,
                    'action': evidence['action'],
                    'clue': evidence['clue'],
                    'cost': evidence['cost'],
                    'reasoning': explanation,
                    'domains_after': copy.deepcopy(ai_detective.domains),
                    'csp_steps': csp_steps
                })
                
                # Update available actions
                updated_game_state = get_game_state(session_id)
                ai_detective.available_actions = updated_game_state.get('available_actions', [])
        
        return jsonify({
            'success': True,
            'solved': ai_detective.is_solved(),
            'solution': ai_detective.get_solution(),
            'steps_taken': len(ai_detective.actions_taken),
            'total_cost': ai_detective.total_cost,
            'solution_path': solution_path,
            'final_domains': ai_detective.domains
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@ai_detective_bp.route('/reset', methods=['POST'])
def reset_ai():
    """Reset AI detective state"""
    try:
        data = request.json
        session_id = data.get('session_id')
        
        if session_id in ai_sessions:
            del ai_sessions[session_id]
        
        return jsonify({
            'success': True,
            'message': 'AI detective reset'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })
