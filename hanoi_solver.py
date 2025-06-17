#!/usr/bin/env python3
"""
Tower of Hanoi Solver - Standalone Version
==========================================

This script solves the Tower of Hanoi puzzle using the optimal recursive algorithm.
The minimum number of moves required to solve a puzzle with n discs is 2^n - 1.

Usage:
    python hanoi_solver.py
    
Or import as a module:
    from hanoi_solver import HanoiSolver
    solver = HanoiSolver(3)
    moves = solver.solve()
"""

class HanoiSolver:
    """
    Tower of Hanoi solver using the optimal recursive algorithm.
    """
    
    def __init__(self, n_discs):
        """
        Initialize the solver with the specified number of discs.
        
        Args:
            n_discs (int): Number of discs to solve for (1-20 recommended)
        """
        if n_discs < 1:
            raise ValueError("Number of discs must be at least 1")
        
        self.n_discs = n_discs
        self.moves = []
        self.move_count = 0
        
        # Initialize towers: A has all discs, B and C are empty
        self.towers = {
            'A': list(range(n_discs, 0, -1)),  # [n, n-1, ..., 2, 1]
            'B': [],
            'C': []
        }
    
    def solve(self, show_steps=True):
        """
        Solve the Tower of Hanoi puzzle and return the sequence of moves.
        
        Args:
            show_steps (bool): Whether to print each move as it's made
            
        Returns:
            list: List of dictionaries containing move information
        """
        print(f"\n🗼 Solving Tower of Hanoi with {self.n_discs} discs")
        print(f"📊 Minimum moves required: {self.get_minimum_moves()}")
        print("=" * 50)
        
        if show_steps:
            self._print_towers("Initial state:")
        
        # Reset state
        self.moves = []
        self.move_count = 0
        self.towers = {
            'A': list(range(self.n_discs, 0, -1)),
            'B': [],
            'C': []
        }
        
        # Solve recursively
        self._hanoi_recursive(self.n_discs, 'A', 'C', 'B', show_steps)
        
        if show_steps:
            print("=" * 50)
            print(f"🎉 Puzzle solved in {self.move_count} moves!")
            print(f"✅ This is the optimal solution (minimum possible moves)")
        
        return self.moves
    
    def _hanoi_recursive(self, n, source, destination, auxiliary, show_steps=True):
        """
        Recursive function to solve Tower of Hanoi.
        
        Args:
            n (int): Number of discs to move
            source (str): Source tower ('A', 'B', or 'C')
            destination (str): Destination tower ('A', 'B', or 'C')
            auxiliary (str): Auxiliary tower ('A', 'B', or 'C')
            show_steps (bool): Whether to print each move
        """
        if n == 1:
            # Move the single disc from source to destination
            self._make_move(source, destination, show_steps)
        else:
            # Move n-1 discs from source to auxiliary (using destination as temp)
            self._hanoi_recursive(n-1, source, auxiliary, destination, show_steps)
            
            # Move the largest disc from source to destination
            self._make_move(source, destination, show_steps)
            
            # Move n-1 discs from auxiliary to destination (using source as temp)
            self._hanoi_recursive(n-1, auxiliary, destination, source, show_steps)
    
    def _make_move(self, source, destination, show_steps=True):
        """
        Make a single move and record it.
        
        Args:
            source (str): Source tower
            destination (str): Destination tower
            show_steps (bool): Whether to print the move
        """
        # Move the disc
        disc = self.towers[source].pop()
        self.towers[destination].append(disc)
        self.move_count += 1
        
        # Record the move
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
        
        if show_steps:
            print(f"Move {self.move_count:2d}: Move disc {disc} from Tower {source} to Tower {destination}")
            self._print_towers()
    
    def _print_towers(self, title=""):
        """
        Print the current state of all towers.
        
        Args:
            title (str): Optional title to print above the towers
        """
        if title:
            print(f"\n{title}")
        
        print("Tower A:", self.towers['A'] if self.towers['A'] else "empty")
        print("Tower B:", self.towers['B'] if self.towers['B'] else "empty")
        print("Tower C:", self.towers['C'] if self.towers['C'] else "empty")
        print()
    
    def get_minimum_moves(self):
        """
        Calculate the minimum number of moves required for n discs.
        
        Returns:
            int: Minimum number of moves (2^n - 1)
        """
        return (2 ** self.n_discs) - 1
    
    def verify_solution(self):
        """
        Verify that the solution is correct and optimal.
        
        Returns:
            dict: Verification results
        """
        expected_moves = self.get_minimum_moves()
        actual_moves = len(self.moves)
        
        # Check if all discs ended up on tower C
        final_state = self.moves[-1]['towers'] if self.moves else self.towers
        correct_final_state = final_state['C'] == list(range(self.n_discs, 0, -1))
        
        return {
            'optimal': actual_moves == expected_moves,
            'correct_final_state': correct_final_state,
            'expected_moves': expected_moves,
            'actual_moves': actual_moves,
            'valid': correct_final_state and actual_moves == expected_moves
        }


def solve_hanoi_interactive():
    """
    Interactive function to solve Tower of Hanoi with user input.
    """
    print("🗼 Welcome to the Tower of Hanoi Solver! 🗼")
    print("=" * 50)
    
    while True:
        try:
            n_discs = input("\nEnter the number of discs (1-10, or 'q' to quit): ").strip()
            
            if n_discs.lower() == 'q':
                print("Thanks for using the Tower of Hanoi Solver! 👋")
                break
            
            n_discs = int(n_discs)
            
            if n_discs < 1:
                print("❌ Please enter a positive number of discs.")
                continue
            elif n_discs > 10:
                print("⚠️  Warning: More than 10 discs will require many moves!")
                confirm = input("Continue anyway? (y/n): ").strip().lower()
                if confirm != 'y':
                    continue
            
            # Solve the puzzle
            solver = HanoiSolver(n_discs)
            moves = solver.solve(show_steps=True)
            
            # Verify the solution
            verification = solver.verify_solution()
            
            print("\n📋 Solution Summary:")
            print(f"   • Total moves: {len(moves)}")
            print(f"   • Optimal moves: {solver.get_minimum_moves()}")
            print(f"   • Solution is optimal: {'✅ Yes' if verification['optimal'] else '❌ No'}")
            print(f"   • Solution is correct: {'✅ Yes' if verification['correct_final_state'] else '❌ No'}")
            
        except ValueError:
            print("❌ Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n\nThanks for using the Tower of Hanoi Solver! 👋")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    solve_hanoi_interactive() 