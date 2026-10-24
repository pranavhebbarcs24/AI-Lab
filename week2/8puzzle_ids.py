def get_neighbors(state):
    neighbors = []
    zero_idx = state.index(0)
    row, col = zero_idx // 3, zero_idx % 3
    moves = []
    if row > 0: moves.append(-3)
    if row < 2: moves.append(3)
    if col > 0: moves.append(-1)
    if col < 2: moves.append(1)
    for move in moves:
        new_zero = zero_idx + move
        new_state = list(state)
        new_state[zero_idx], new_state[new_zero] = new_state[new_zero], new_state[zero_idx]
        neighbors.append(tuple(new_state))
    return neighbors

def dls_solve(state, goal, depth, path, visited):
    if state == goal:
        return path
    if depth <= 0:
        return None
    for neighbor in get_neighbors(state):
        if neighbor not in visited or len(path) < visited[neighbor]:
            visited[neighbor] = len(path)
            result = dls_solve(neighbor, goal, depth - 1, path + [neighbor], visited)
            if result is not None:
                return result
    return None

def ids_solve(start, goal, max_depth=50):
    for depth in range(max_depth):
        visited = {start: 0}
        result = dls_solve(start, goal, depth, [start], visited)
        if result is not None:
            return result
    return None

start_state = (1, 2, 3, 0, 4, 6, 7, 5, 8)
goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
solution = ids_solve(start_state, goal_state)
if solution:
    for step, state in enumerate(solution):
        print(f"Step {step}:")
        for i in range(0, 9, 3):
            print(state[i:i+3])
        print()
else:
    print("No solution found within depth limit.")