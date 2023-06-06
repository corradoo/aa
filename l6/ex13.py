import numpy as np
from markov import (
    calculate_stationary_distribution_many,
    calculate_stationary_distribution,
    calculate_state_probability,
)

# transition matrix P
P = np.array([[0, 3/10, 1/10, 3/5],
              [1/10, 1/10, 7/10, 1/10],
              [1/10, 7/10, 1/10, 1/10],
              [9/10, 1/10, 0, 0]])

#Rozkład stacjonarny
stationary_distribution = calculate_stationary_distribution_many(P)
print("a) Stationary Distribution:")
print(stationary_distribution)
print()

#P-stwo 3 po 32 krokach, jeśli zaczynamy w stanie 0.
start_state = 0
num_steps = 32

state_probability = calculate_state_probability(P,  num_steps,start_state)
probability_state_3 = state_probability[3]

print(f"b) Probability of being in state 3 after {num_steps} steps, starting from state {start_state}: \n{probability_state_3}")
print()


#P-stwo 3 po 128 krokach zaczynając w losowym stanie
num_steps = 128

state_probability = calculate_state_probability(P, num_steps,random_state=True)
probability_state_3 = state_probability[3]

print(f"c) Probability of being in state 3 after {num_steps} steps, starting from a randomly chosen state: \n{probability_state_3}")
print()

#Min t 
def find_min_steps(P, epsilon_values):
    num_steps = 1
    max_difference = np.inf
    min_steps = {}

    while len(epsilon_values) > 0:
        state_probability = calculate_state_probability(P, num_steps,start_state=0)
        max_difference = np.max(np.abs(state_probability - stationary_distribution))
        
        if max_difference <= epsilon_values[0]:
            min_steps[epsilon_values[0]] = num_steps
            epsilon_values.pop(0)

        num_steps += 1

    return min_steps

# Calculate the stationary distribution
stationary_distribution = calculate_state_probability(P, 1000)

epsilon_values = [1/10, 1/100, 1/1000]

# Find the minimum steps for each epsilon value
min_steps = find_min_steps(P, epsilon_values)

# Print the results
print("d)")
for epsilon, steps in min_steps.items():
    print(f"For ε = {epsilon}, the minimum number of steps required is: {steps}")