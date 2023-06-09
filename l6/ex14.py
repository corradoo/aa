import numpy as np
import matplotlib.pyplot as plt
from markov import calculate_stationary_distribution_many


def calculate_stationary_distribution_iter(MG, num_steps):
    # distribution at time 0
    pi = np.ones(n) / n

    # List to store the distributions at each step
    distributions = [pi]

    # Perform the iterations
    for _ in range(num_steps):
        pi = np.dot(pi, MG)
        distributions.append(pi)

    return distributions


P = np.array(
    [
        [0, 1 / 2, 1 / 2, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 1 / 3, 0, 1 / 3, 1 / 3],
        [1, 0, 0, 0, 0],
        [1 / 5, 1 / 5, 1 / 5, 1 / 5, 1 / 5],
    ]
)

alpha_values = [0, 0.25, 0.5, 0.75, 0.85, 1]
num_steps = 25

# Calculate the distributions for different alpha values
distributions = {}
distributions_a = {}
for alpha in alpha_values:
    n = P.shape[0]
    Jn = np.ones((n, n))
    MG = (1 - alpha) * P + alpha * (1 / n) * Jn
    distributions[alpha] = calculate_stationary_distribution_iter(MG, num_steps)
    distributions_a[alpha] = calculate_stationary_distribution_many(MG)
    print(f"alpha: {alpha}: {distributions_a[alpha]}")


# Plot the distributions for different alpha values
for alpha, distribution in distributions.items():
    for i in range(len(distribution[0])):
        plt.plot(
            range(len(distribution)),
            [dist[i] for dist in distribution],
            label=f"Page {i+1}",
        )

    plt.xlabel("Step")
    plt.ylabel("Probability")
    plt.title(f"Convergence to Stationary Distribution (α={alpha})")
    plt.legend()
    plt.grid()
    plt.savefig(f"out2/conv{alpha}.png")
    plt.clf()

    # Plot the distributions
    for i in range(len(distribution[0])):
        plt.plot(
            range(len(distribution)),
            [np.abs(dist[i] - distributions_a[alpha][i]) for dist in distribution],
            label=f"Page {i+1}",
        )

    plt.xlabel("Step")
    plt.ylabel("Ratio")
    plt.title(f"Convergence to Stationary Distribution (α={alpha})")
    plt.legend()
    plt.grid()
    plt.savefig(f"out2/conv_ratio{alpha}.png")
    plt.clf()

# Plot norm for alphas
for alpha, distribution in distributions.items():
    plt.plot(
        range(len(distribution)),
        [np.sum([np.abs(dist[i] - distributions_a[alpha][i]) for i in range(5)]) for dist in distribution],
        # [np.linalg.norm(dist,distributions_a[alpha]) for dist in distribution],
        label=f"α={alpha}",
    )
plt.xlabel("Step")
plt.ylabel("Ratio")
plt.title(f"Convergence to Stationary Distribution")
plt.legend()
plt.grid()
plt.savefig(f"out2/conv.png")
plt.clf()

for alpha, distribution in distributions.items():
    plt.plot(
        range(len(distribution)),
        # [np.sum([np.abs(dist[i] - distributions_a[alpha][i]) for i in range(5)]) for dist in distribution],
        [np.linalg.norm(dist-distributions_a[alpha]) for dist in distribution],
        label=f"α={alpha}",
    )
plt.xlabel("Step")
plt.ylabel("Ratio")
plt.title(f"Convergence to Stationary Distribution")
plt.legend()
plt.grid()
plt.savefig(f"out2/conv_norm.png")
plt.clf()

# Plot and save the histograms for different alpha values
for alpha, distribution in distributions.items():
    distribution = distribution[-1]

    # Barplot
    plt.bar([1, 2, 3, 4, 5], distribution)

    plt.xlabel("page")
    plt.ylabel("PageRank Probability")
    plt.title(f"PageRank Distribution (alpha={alpha})")
    plt.grid()
    plt.savefig(f"out2/histogram_alpha_{alpha}.png")
    plt.clf()
