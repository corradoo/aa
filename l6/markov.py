import numpy as np


def calculate_state_probability(P, num_steps, alpha=0, start_state=0, random_state=False, ):
    n = P.shape[0]
    state_vector = np.zeros(n)
    state_vector[start_state] = 1

    Jn = np.ones((n, n))
    MG = (1 - alpha) * P + alpha * (1 / n) * Jn

    if random_state:
        state_vector = np.ones(n) / n
    
    power = np.linalg.matrix_power(MG, num_steps)
    state_vector = np.dot(state_vector, power)

    return state_vector


def calculate_stationary_distribution(P, alpha):
    n = P.shape[0]
    Jn = np.ones((n, n))
    MG = (1 - alpha) * P + alpha * (1 / n) * Jn

    if alpha == 0:
        MG = P
    # Wektory i wartości własne
    eigenvalues, eigenvectors = np.linalg.eig(MG.T)

    # Znajdź wartość własną najbliższą 1
    stationary_index = np.argmin(np.abs(eigenvalues - 1))

    # extracts the eigenvector corresponding to the stationary eigenvalue.
    stationary_distribution = np.real(eigenvectors[:, stationary_index])

    # normalizes the stationary distribution vector to ensure that its elements sum up to 1.
    # To produce a probability vector, every element in the selected
    # eigenvector is divided by the sum of the eigenvector.
    stationary_distribution /= np.sum(stationary_distribution)

    return stationary_distribution


def calculate_stationary_distribution_many(P, alpha=0):
    n = P.shape[0]
    Jn = np.ones((n, n))
    MG = (1 - alpha) * P + alpha * (1 / n) * Jn

    if alpha == 0:
        MG = P
    # Wektory i wartości własne
    eigenvalues, eigenvectors = np.linalg.eig(MG.T)

    # Znajdź wartość własną najbliższą 1
    stationary_indexes = np.where(np.isclose(eigenvalues, 1))[0]

    # breakpoint()
    stationary_distribution = np.zeros(n)
    for i in stationary_indexes:
        stationary_distribution += np.abs(np.real(np.transpose(eigenvectors[:, i])))
        stationary_distribution /= np.sum(stationary_distribution)

    return stationary_distribution
