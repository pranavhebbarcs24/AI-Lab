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

def dfs_solve(start, goal, limit=20):
    stack = [(start, [start])]
    visited = {start: 0}
    while stack:
        state, path = stack.pop()
        if state == goal:
            return path
        if len(path) - 1 >= limit:
            continue
        for neighbor in reversed(get_neighbors(state)):
            if neighbor not in visited or len(path) < visited[neighbor]:
                visited[neighbor] = len(path)
                stack.append((neighbor, path + [neighbor]))
    return None

start_state = (1, 2, 3, 4, 5, 6, 7, 0, 8)
goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
solution = dfs_solve(start_state, goal_state)
if solution:
    for step, state in enumerate(solution):
        print(f"Step {step}:")
        for i in range(0, 9, 3):
            print(state[i:i+3])
        print()
else:
    print("No solution found within depth limit.")