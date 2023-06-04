import numpy as np

def calculate_stationary_distribution(P):
    n = P.shape[0]
    P_transpose = P.T
    A = np.vstack((P_transpose - np.eye(n), np.ones(n)))
    b = np.zeros(n+1)
    b[-1] = 1

    stationary_distribution = np.linalg.lstsq(A, b, rcond=None)[0]
    stationary_distribution /= np.sum(stationary_distribution)

    return stationary_distribution

def calculate_state_probability(P,  num_steps, start_state=0, random_state=False):
    n = P.shape[0]
    state_vector = np.zeros(n)
    state_vector[start_state] = 1
    
    if random_state:
        state_vector = np.ones(n) / n

    for _ in range(num_steps):
        state_vector = np.dot(state_vector, P)

    return state_vector

# Define the transition matrix P
P = np.array([[0, 3/10, 1/10, 3/5],
              [1/10, 1/10, 7/10, 1/10],
              [1/10, 7/10, 1/10, 1/10],
              [9/10, 1/10, 0, 0]])

#Rozkład stacjonarny
stationary_distribution = calculate_stationary_distribution(P)
print("Stationary Distribution:")
print(stationary_distribution)

#P-stwo 3 po 32 krokach, jeśli zaczynamy w stanie 0.
start_state = 0
num_steps = 32

state_probability = calculate_state_probability(P,  num_steps,start_state)
probability_state_3 = state_probability[3]

print(f"The probability of being in state 3 after {num_steps} steps, starting from state {start_state}, is: {probability_state_3}")


#P-stwo 3 po 128 krokach zaczynając w losowym stanie
num_steps = 128

state_probability = calculate_state_probability(P, num_steps,random_state=True)
probability_state_3 = state_probability[3]

print(f"The probability of being in state 3 after {num_steps} steps, starting from a randomly chosen state, is: {probability_state_3}")

#Min t 
def find_min_steps(P, epsilon_values):
    start_state = 0
    num_steps = 1
    max_difference = np.inf
    min_steps = {}

    while len(epsilon_values) > 0:
        state_probability = calculate_state_probability(P, num_steps)
        max_difference = np.max(np.abs(state_probability - stationary_distribution))

        if max_difference <= epsilon_values[0]:
            min_steps[epsilon_values[0]] = num_steps
            epsilon_values.pop(0)

        num_steps += 1

    return min_steps

# Calculate the stationary distribution
stationary_distribution = calculate_state_probability(P, 1000)

# Define the epsilon values
epsilon_values = [1/10, 1/100, 1/1000]

# Find the minimum steps for each epsilon value
min_steps = find_min_steps(P, epsilon_values)

# Print the results
for epsilon, steps in min_steps.items():
    print(f"For ε = {epsilon}, the minimum number of steps required is: {steps}")