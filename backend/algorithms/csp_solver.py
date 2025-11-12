"""
Enhanced CSP Solver with Arc Consistency (AC-3) and detailed step tracking
"""
import copy

class CSPSolver:
    def __init__(self, domains, constraints):
        """
        Initialize CSP Solver
        domains: dict of {variable: [possible_values]}
        constraints: list of (category, value, action_type) tuples
        """
        self.domains = copy.deepcopy(domains)
        self.constraints = constraints
        self.steps = []
    
    def solve(self):
        """
        Solve CSP using constraint propagation
        Returns True if consistent, False if inconsistency detected
        """
        self.steps = []
        
        # Apply explicit constraints first
        for category, value, action_type in self.constraints:
            if action_type == 'eliminate':
                if value in self.domains[category]:
                    self.domains[category].remove(value)
                    self.steps.append({
                        'step': 'Elimination',
                        'message': f"Eliminated {value} from {category}",
                        'type': 'elimination'
                    })
            elif action_type == 'confirm':
                if len(self.domains[category]) > 1:
                    self.domains[category] = [value]
                    self.steps.append({
                        'step': 'Confirmation',
                        'message': f"Confirmed {value} as {category}",
                        'type': 'confirmation'
                    })
        
        # Apply arc consistency
        changed = True
        iterations = 0
        max_iterations = 10
        
        while changed and iterations < max_iterations:
            changed = False
            iterations += 1
            
            # Check for singleton domains and propagate
            for var1, values1 in self.domains.items():
                if len(values1) == 1:
                    # This variable is assigned, check others
                    assigned_value = values1[0]
                    
                    for var2, values2 in self.domains.items():
                        if var1 != var2 and assigned_value in values2 and len(values2) > 1:
                            # Remove this value from other domain
                            self.domains[var2].remove(assigned_value)
                            changed = True
                            self.steps.append({
                                'step': 'Arc Consistency',
                                'message': f"Removed {assigned_value} from {var2} (already assigned to {var1})",
                                'type': 'elimination'
                            })
        
        # Check for empty domains
        for var, values in self.domains.items():
            if len(values) == 0:
                self.steps.append({
                    'step': 'Inconsistency',
                    'message': f"Domain of {var} is empty - no solution possible",
                    'type': 'error'
                })
                return False
        
        return True
    
    def get_steps(self):
        """Return all algorithm steps for visualization"""
        return self.steps
    
    def is_solved(self):
        """Check if all variables are assigned"""
        return all(len(values) == 1 for values in self.domains.values())
    
    def count_solutions(self):
        """Count number of possible solutions"""
        count = 1
        for values in self.domains.values():
            count *= len(values)
        return count