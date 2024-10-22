from typing import List, Tuple, Dict, Set
from collections import defaultdict

class PuzzleSolver:
    def __init__(self):
        self.target = 2024
        self.grid_values = [
            ['A', 'B', 'B', 'C', 'C', 'C'],
            ['A', 'B', 'B', 'C', 'C', 'C'],
            ['A', 'A', 'B', 'B', 'C', 'C'],
            ['A', 'A', 'B', 'B', 'C', 'C'],
            ['A', 'A', 'A', 'B', 'B', 'C'],
            ['A', 'A', 'A', 'B', 'B', 'C']
        ]
        # Precompute all valid knight moves for each position
        self.knight_moves = self._precompute_knight_moves()
        # Cache for path scores
        self.score_cache = {}
        
    def _precompute_knight_moves(self) -> Dict[Tuple[int, int], List[Tuple[int, int]]]:
        """Precompute all valid knight moves for each position."""
        moves = {}
        knight_deltas = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]
        for i in range(6):
            for j in range(6):
                valid = []
                for dx, dy in knight_deltas:
                    new_x, new_y = i + dx, j + dy
                    if 0 <= new_x < 6 and 0 <= new_y < 6:
                        valid.append((new_x, new_y))
                moves[(i,j)] = valid
        return moves

    def calculate_score(self, path: List[Tuple[int, int]], values: Dict[str, int]) -> int:
        """Calculate score for a path with early termination if exceeding target."""
        path_tuple = tuple(path)
        if path_tuple in self.score_cache:
            return self.score_cache[path_tuple]
        
        score = values[self.grid_values[path[0][0]][path[0][1]]]
        
        for i in range(1, len(path)):
            curr_val = self.grid_values[path[i][0]][path[i][1]]
            prev_val = self.grid_values[path[i-1][0]][path[i-1][1]]
            curr_num = values[curr_val]
            
            if curr_val == prev_val:
                score += curr_num
            else:
                score *= curr_num
                
            # Early termination if score exceeds target
            if score > self.target:
                self.score_cache[path_tuple] = score
                return score
                
        self.score_cache[path_tuple] = score
        return score

    def find_path(self, start: Tuple[int, int], end: Tuple[int, int], 
                 values: Dict[str, int]) -> List[Tuple[int, int]]:
        """Find a valid path using iterative deepening with pruning."""
        def dfs(pos: Tuple[int, int], path: List[Tuple[int, int]], 
                visited: Set[Tuple[int, int]], depth: int, max_depth: int) -> List[Tuple[int, int]]:
            if depth > max_depth:
                return None
            if pos == end:
                score = self.calculate_score(path, values)
                if score == self.target:
                    return path
                return None
            
            curr_score = self.calculate_score(path, values)
            if curr_score > self.target:
                return None
                
            for next_pos in self.knight_moves[pos]:
                if next_pos not in visited:
                    path.append(next_pos)
                    visited.add(next_pos)
                    result = dfs(next_pos, path, visited, depth + 1, max_depth)
                    if result:
                        return result
                    visited.remove(next_pos)
                    path.pop()
            return None

        # Iterative deepening with practical depth limit
        for max_depth in range(4, 12):  # Most solutions should be within this range
            path = [start]
            visited = {start}
            result = dfs(start, path, visited, 0, max_depth)
            if result:
                return result
        return None

    def format_path(self, path: List[Tuple[int, int]]) -> str:
        """Convert path coordinates to algebraic notation."""
        return ','.join(f"{chr(97 + y)}{6 - x}" for x, y in path)

    def solve(self) -> str:
        """Find optimal solution with minimal A + B + C."""
        best_sum = float('inf')
        best_solution = None
        
        # Optimize value ranges based on target
        # Since we need to reach 2024, values can't be too small
        for A in range(1, 20):  # A is typically small
            # Early pruning based on minimum possible score
            if A > self.target:
                break
                
            for B in range(A + 1, 30):  # B should be larger than A
                if A * B > self.target:  # Early pruning
                    break
                    
                for C in range(B + 1, 50 - A - B):  # C should be largest
                    curr_sum = A + B + C
                    if curr_sum >= best_sum:
                        continue
                    
                    values = {'A': A, 'B': B, 'C': C}
                    
                    # Clear cache for new value set
                    self.score_cache.clear()
                    
                    # Find paths
                    path1 = self.find_path((5, 0), (0, 5), values)  # a1 to f6
                    if not path1:
                        continue
                        
                    path2 = self.find_path((0, 0), (5, 5), values)  # a6 to f1
                    if not path2:
                        continue
                    
                    best_sum = curr_sum
                    best_solution = (A, B, C, path1, path2)
                    print(f"Found solution with sum {best_sum}")
                    
                    # If we find a very good solution, we can increase our pruning
                    if best_sum < 20:  # Arbitrary threshold for a "very good" solution
                        print('Good solution: ', self.format_solution(*best_solution))
        
        return self.format_solution(*best_solution) if best_solution else "No solution found"

    def format_solution(self, A: int, B: int, C: int, path1: List[Tuple[int, int]], 
                       path2: List[Tuple[int, int]]) -> str:
        """Format the final solution string."""
        return f"{A},{B},{C},{self.format_path(path1)},{self.format_path(path2)}"

def main():
    solver = PuzzleSolver()
    solution = solver.solve()
    print(f"Solution: {solution}")

if __name__ == "__main__":
    main()
