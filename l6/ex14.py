import numpy as np
import matplotlib.pyplot as plt

def calculate_stationary_distribution(MG, alpha, num_steps):
    n = MG.shape[0]
    Jn = np.ones((n, n))
    PG = MG / MG.sum(axis=0)  # Transition matrix

    # Initialize the distribution at time 0
    pi = np.ones(n) / n

    # List to store the distributions at each step
    distributions = [pi]

    # Perform the iterations
    for _ in range(num_steps):
        pi = (1 - alpha) * np.dot(PG, pi) + alpha * (1 / n) * np.dot(Jn, pi)
        distributions.append(pi)

    return distributions

# Define the adjacency matrix of the directed graph G
NG = np.array([[0, 1/2, 1/2, 0, 0],
               [0, 0, 0, 1, 0],
               [0, 1/3, 0, 1/3, 1/3],
               [1, 0, 0, 0, 0],
               [1/5, 1/5, 1/5, 1/5, 1/5]])

# Define the parameters
alpha_values = [0, 0.25, 0.5, 0.75, 0.85, 1]
num_steps = 25

# Calculate the distributions for different alpha values
distributions = {}
for alpha in alpha_values:
    distributions[alpha] = calculate_stationary_distribution(NG, alpha, num_steps)

# Plot the distributions for different alpha values
for alpha, distribution in distributions.items():
    
    # Plot the distributions
    for i in range(len(distribution[0])):
        plt.plot(range(len(distribution)), [dist[i] for dist in distribution], label=f'Page {i+1}')
        
    plt.xlabel('Step')
    plt.ylabel('Probability')
    plt.title('Convergence to Stationary Distribution')
    plt.legend()
    plt.savefig(f'conv{alpha}.png')
    plt.clf()

# Plot and save the histograms for different alpha values
for alpha, distribution in distributions.items():
    
    # Get final distribution
    distribution = distribution[-1]
    # breakpoint()

    # Plot the histogram
    plt.bar([1,2,3,4,5],distribution)

    plt.xlabel('page')
    plt.ylabel('PageRank Probability')
    plt.title(f'PageRank Distribution (alpha={alpha})')

    # Save the plot to a file
    plt.savefig(f'histogram_alpha_{alpha}.png')
    plt.clf()
