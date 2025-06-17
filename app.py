from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

class HanoiSolver:
    def __init__(self, n_discs):
        self.n_discs = n_discs
        self.moves = []
        self.move_count = 0
        # Initialize towers: A has all discs, B and C are empty
        self.towers = {
            'A': list(range(n_discs, 0, -1)),  # [n, n-1, ..., 2, 1]
            'B': [],
            'C': []
        }
    
    def solve(self):
        """Solve the Tower of Hanoi puzzle"""
        self.moves = []
        self.move_count = 0
        self._hanoi_recursive(self.n_discs, 'A', 'C', 'B')
        return self.moves
    
    def _hanoi_recursive(self, n, source, destination, auxiliary):
        """Recursive function to solve Tower of Hanoi"""
        if n == 1:
            # Move the single disc from source to destination
            self._make_move(source, destination)
        else:
            # Move n-1 discs from source to auxiliary
            self._hanoi_recursive(n-1, source, auxiliary, destination)
            # Move the largest disc from source to destination
            self._make_move(source, destination)
            # Move n-1 discs from auxiliary to destination
            self._hanoi_recursive(n-1, auxiliary, destination, source)
    
    def _make_move(self, source, destination):
        """Make a single move and record it"""
        disc = self.towers[source].pop()
        self.towers[destination].append(disc)
        self.move_count += 1
        
        # Record the move with current state
        move_info = {
            'move_number': self.move_count,
            'from': source,
            'to': destination,
            'disc': disc,
            'towers': {
                'A': self.towers['A'].copy(),
                'B': self.towers['B'].copy(),
                'C': self.towers['C'].copy()
            }
        }
        self.moves.append(move_info)
    
    def get_minimum_moves(self):
        """Calculate the minimum number of moves required"""
        return (2 ** self.n_discs) - 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve_hanoi():
    try:
        n_discs = int(request.json.get('discs', 3))
        if n_discs < 1 or n_discs > 10:
            return jsonify({'error': 'Number of discs must be between 1 and 10'}), 400
        
        solver = HanoiSolver(n_discs)
        moves = solver.solve()
        minimum_moves = solver.get_minimum_moves()
        
        return jsonify({
            'success': True,
            'moves': moves,
            'total_moves': len(moves),
            'minimum_moves': minimum_moves,
            'initial_state': {
                'A': list(range(n_discs, 0, -1)),
                'B': [],
                'C': []
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True) 