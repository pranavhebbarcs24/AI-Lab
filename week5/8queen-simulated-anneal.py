import math
import random


def calculate_heuristic(state):
    """
    Calculates the number of attacking pairs of queens on an 8x8 board.
    h = 0 indicates a valid non-attacking solution.
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


def get_random_neighbor(state):
    """
    Generates a single random neighbor state by moving one queen 
    in a randomly chosen column to a different row.
    """
    neighbor = list(state)
    col = random.randint(0, 7)
    current_row = state[col]

    # Pick a new row different from the current row
    new_row = random.choice([r for r in range(8) if r != current_row])
    neighbor[col] = new_row
    return neighbor


def simulated_annealing_8_queens(initial_temp=10.0, cooling_rate=0.995, min_temp=0.001, max_steps=100000):
    """
    Solves the 8-Queens problem using Simulated Annealing.
    """
    # 1. Initialize with a random state
    current_state = [random.randint(0, 7) for _ in range(8)]
    current_h = calculate_heuristic(current_state)
    
    temperature = initial_temp
    step = 0

    print(f"Initial State: {current_state} | Initial Conflicts (h): {current_h}\n")

    # 2. Annealing Loop
    while temperature > min_temp and current_h > 0 and step < max_steps:
        # Generate a random neighbor
        neighbor_state = get_random_neighbor(current_state)
        neighbor_h = calculate_heuristic(neighbor_state)

        # Calculate energy difference (delta E)
        delta_h = neighbor_h - current_h

        # Acceptance Criterion:
        # - If delta_h < 0 (better state), accept immediately.
        # - If delta_h >= 0 (worse state), accept with probability e^(-delta_h / T)
        if delta_h < 0:
            current_state = neighbor_state
            current_h = neighbor_h
        else:
            acceptance_prob = math.exp(-delta_h / temperature)
            if random.random() < acceptance_prob:
                current_state = neighbor_state
                current_h = neighbor_h

        # Cool down the temperature
        temperature *= cooling_rate
        step += 1

    # 3. Print Final Summary
    print("-" * 55)
    if current_h == 0:
        print(f"SUCCESS: Found solution in {step} iterations!")
    else:
        print(f"TERMINATED: Reached minimum temperature at step {step}.")
    
    print(f"Final State: {current_state}")
    print(f"Final Conflicts (h): {current_h}")
    
    return current_state, current_h


def print_board(state):
    """Utility function to render an ascii 8x8 chessboard."""
    n = len(state)
    print("\nVisual Board Representation:")
    print("┌───" + "┬───" * (n - 1) + "┐")
    for row in range(n):
        line = "│"
        for col in range(n):
            line += " Q │" if state[col] == row else "   │"
        print(line)
        if row < n - 1:
            print("├───" + "┼───" * (n - 1) + "┤")
    print("└───" + "┴───" * (n - 1) + "┘")


# --- Execution ---
if __name__ == "__main__":
    solution_state, final_conflicts = simulated_annealing_8_queens()
    print_board(solution_state)