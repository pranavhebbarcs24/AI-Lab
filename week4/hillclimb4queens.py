import random


def calculate_heuristic(state):
    """
    Calculates the number of attacking pairs of queens on the board.
    h = 0 means a valid non-attacking solution.
    """
    attacks = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            # Same row attack
            if state[i] == state[j]:
                attacks += 1
            # Diagonal attack (|row_diff| == |col_diff|)
            elif abs(state[i] - state[j]) == abs(i - j):
                attacks += 1
    return attacks


def get_best_neighbor(current_state):
    """
    Evaluates all 12 possible single-move neighbors (4 columns * 3 alternative rows)
    and returns the neighbor with the lowest heuristic value.
    """
    n = len(current_state)
    current_h = calculate_heuristic(current_state)
    best_state = list(current_state)
    best_h = current_h

    # Check all possible single-queen movements
    for col in range(n):
        original_row = current_state[col]
        for row in range(n):
            if row != original_row:
                neighbor = list(current_state)
                neighbor[col] = row
                neighbor_h = calculate_heuristic(neighbor)

                # Keep track of the strictly best neighbor
                if neighbor_h < best_h:
                    best_h = neighbor_h
                    best_state = neighbor

    return best_state, best_h


def hill_climbing_4_queens():
    """
    Executes Steepest-Ascent Hill Climbing to solve the 4-Queens problem.
    """
    # 1. Generate a random initial state (e.g., [2, 0, 3, 1])
    current_state = [random.randint(0, 3) for _ in range(4)]
    current_h = calculate_heuristic(current_state)

    step = 0
    print(f"Step {step}: Initial State = {current_state}, Attacking Pairs (h) = {current_h}")

    # 2. Main Search Loop
    while True:
        best_neighbor, best_neighbor_h = get_best_neighbor(current_state)

        # If no neighbor improves the heuristic, we reached a peak/local minimum
        if best_neighbor_h >= current_h:
            break

        current_state = best_neighbor
        current_h = best_neighbor_h
        step += 1
        print(f"Step {step}: Moved to State = {current_state}, Attacking Pairs (h) = {current_h}")

    # 3. Final Result Verification
    print("-" * 50)
    if current_h == 0:
        print(f"SUCCESS: Found Global Solution in {step} steps: {current_state}")
    else:
        print(f"STUCK IN LOCAL MINIMUM at state {current_state} with h = {current_h}")

    return current_state, current_h


def print_board(state):
    """Utility to print a visual 4x4 board representation."""
    n = len(state)
    print("\nVisual Board Representation:")
    for row in range(n):
        line = ""
        for col in range(n):
            line += " Q " if state[col] == row else " . "
        print(line)


# --- Execute Strategy ---
if __name__ == "__main__":
    final_state, final_h = hill_climbing_4_queens()
    print_board(final_state)