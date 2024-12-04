import random
import math

# Define the objects with value and weight
Objects = {
    'A': (10, 2),
    'B': (6, 3),
    'C': (4, 8),
    'D': (8, 5),
    'E': (9, 4),
    'F': (7, 6)
}

# Bag capacity
P = 15

# List of object keys to help index the state
object_keys = list(Objects.keys())
n = len(object_keys)

def eval_function(state):
    """
    Evaluate the state by calculating the total value of the selected objects
    while ensuring the total weight doesn't exceed the bag's capacity.
    """
    total_value = 0
    total_weight = 0

    for i, selected in enumerate(state):
        if selected:  # If object is included in the bag
            value, weight = Objects[object_keys[i]]
            total_value += value
            total_weight += weight

    # If weight exceeds capacity, return -1 to invalidate the state
    if total_weight > P:
        return -1
    return total_value


def getNeighbor(state):
    """
    Generate a neighboring state by flipping the inclusion of a random object.
    """
    neighbor = state.copy()
    idx = random.randint(0, n - 1)  # Select a random object
    neighbor[idx] = 1 - neighbor[idx]  # Flip its inclusion
    return neighbor


def simulated_annealing():
    """
    Perform simulated annealing to solve the Knapsack Problem.
    """
    # Initialize temperature and cooling rate
    T = 100.0  # Initial temperature
    alpha = 0.99  # Cooling rate

    # Generate a random initial state
    current_state = [random.randint(0, 1) for _ in range(n)]
    current_value = eval_function(current_state)

    best_state = current_state
    best_value = current_value

    while T > 1e-3:  # Stop when temperature is close to 0
        # Generate a neighbor state
        neighbor_state = getNeighbor(current_state)
        neighbor_value = eval_function(neighbor_state)

        # If the neighbor is invalid (value = -1), skip it
        if neighbor_value == -1:
            continue

        # Accept the neighbor state if it's better, or probabilistically if it's worse
        delta = neighbor_value - current_value
        if delta > 0 or random.random() < math.exp(delta / T):
            current_state = neighbor_state
            current_value = neighbor_value

            # Update the best state found
            if current_value > best_value:
                best_state = current_state
                best_value = current_value

        # Cool down the temperature
        T *= alpha

    return best_state, best_value


# Run the simulated annealing algorithm
best_state, best_value = simulated_annealing()

# Display results
selected_objects = [object_keys[i] for i in range(n) if best_state[i] == 1]
print("Selected objects:", selected_objects)
print("Best value:", best_value)
