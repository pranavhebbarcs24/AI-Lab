import heapq

# Goal state
GOAL = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)


# Heuristic 1: Misplaced Tiles
def misplaced_tiles(state):
    count = 0

    for i in range(9):
        if state[i] != 0 and state[i] != GOAL[i]:
            count += 1

    return count


# Heuristic 2: Manhattan Distance
def manhattan_distance(state):
    distance = 0

    for i in range(9):
        tile = state[i]

        if tile != 0:
            # Current position
            row, col = divmod(i, 3)

            # Goal position of the tile
            goal_row, goal_col = divmod(tile - 1, 3)

            distance += abs(row - goal_row)
            distance += abs(col - goal_col)

    return distance


# Generate all valid neighboring states
def get_neighbors(state):
    neighbors = []

    zero = state.index(0)
    row, col = divmod(zero, 3)

    moves = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1)    # Right
    ]

    for dr, dc in moves:
        new_row = row + dr
        new_col = col + dc

        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_zero = new_row * 3 + new_col

            new_state = list(state)
            new_state[zero], new_state[new_zero] = (
                new_state[new_zero], new_state[zero]
            )

            neighbors.append(tuple(new_state))

    return neighbors


# A* Search Algorithm
def astar(start, heuristic):
    # (f_cost, g_cost, state)
    pq = [(heuristic(start), 0, start)]

    parent = {start: None}
    g_cost = {start: 0}

    while pq:
        f, g, state = heapq.heappop(pq)

        # Ignore outdated queue entries
        if g != g_cost[state]:
            continue

        # Goal reached
        if state == GOAL:
            path = []

            while state is not None:
                path.append(state)
                state = parent[state]

            return path[::-1]

        for neighbor in get_neighbors(state):
            new_g = g + 1

            if new_g < g_cost.get(neighbor, float("inf")):
                g_cost[neighbor] = new_g
                parent[neighbor] = state

                new_f = new_g + heuristic(neighbor)
                heapq.heappush(
                    pq, (new_f, new_g, neighbor)
                )

    return None


# Print the solution
def print_solution(path):
    if path is None:
        print("No solution found.")
        return

    print("Number of moves:", len(path) - 1)

    for step, state in enumerate(path):
        print("\nStep", step)

        for i in range(0, 9, 3):
            print(state[i:i + 3])


# Initial state (0 represents the blank)
start = (1, 2, 3,
         4, 0, 6,
         7, 5, 8)


print("A* with Misplaced Tiles:")
path1 = astar(start, misplaced_tiles)
print_solution(path1)

print("\nA* with Manhattan Distance:")
path2 = astar(start, manhattan_distance)
print_solution(path2)
