"""
Enhanced CSP Solver with detailed step tracking
"""

class EnhancedCSPSolver:
    def __init__(self, domains, constraints):
        self.domains = domains
        self.constraints = constraints
        self.steps = []
        
    def solve(self):
        """
        Solve CSP using AC-3 algorithm with detailed logging
        """
        self.steps = []
        
        # Initialize queue with all arcs
        queue = []
        for var1 in self.domains:
            for var2 in self.domains:
                if var1 != var2:
                    queue.append((var1, var2))
        
        self.steps.append({
            'type': 'initialization',
            'algorithm': 'AC-3',
            'message': f'Initialized arc consistency queue with {len(queue)} arcs',
            'details': 'Starting constraint propagation'
        })
        
        while queue:
            var1, var2 = queue.pop(0)
            
            if self._revise(var1, var2):
                if len(self.domains[var1]) == 0:
                    self.steps.append({
                        'type': 'failure',
                        'algorithm': 'AC-3',
                        'message': f'Domain of {var1} became empty - inconsistency detected',
                        'details': 'No solution exists with current constraints'
                    })
                    return False
                
                # Add neighbors back to queue
                for var3 in self.domains:
                    if var3 != var1 and var3 != var2:
                        queue.append((var3, var1))
        
        self.steps.append({
            'type': 'completion',
            'algorithm': 'AC-3',
            'message': 'Arc consistency achieved',
            'details': f'Final domain sizes: {[(k, len(v)) for k, v in self.domains.items()]}'
        })
        
        return True
    
    def _revise(self, var1, var2):
        """
        Revise domain of var1 with respect to var2
        """
        revised = False
        
        for value1 in list(self.domains[var1]):
            # Check if there exists a value in var2's domain that satisfies constraints
            has_support = False
            for value2 in self.domains[var2]:
                if self._is_consistent(var1, value1, var2, value2):
                    has_support = True
                    break
            
            if not has_support:
                self.domains[var1].remove(value1)
                revised = True
                self.steps.append({
                    'type': 'elimination',
                    'algorithm': 'AC-3 Revision',
                    'message': f'Removed {value1} from {var1} domain',
                    'details': f'No consistent value found in {var2} domain'
                })
        
        return revised
    
    def _is_consistent(self, var1, val1, var2, val2):
        """
        Check if assignment is consistent with constraints
        """
        # Implement your constraint checking logic
        # For example: all different constraint
        if var1 == var2:
            return val1 == val2
        
        # Check against explicit constraints
        for constraint in self.constraints:
            if not constraint(var1, val1, var2, val2):
                return False
        
        return True
    
    def get_steps(self):
        """Return all algorithm steps for visualization"""
        return self.steps
