"""
Współczynnik α w algorytmie PageRank nazywany jest czasem "współczynnikiem znudzenia" lub "damping factor" w języku angielskim. 
Nazwa ta wynika z roli, jaką odgrywa w modelowaniu zachowania użytkowników podczas przeglądania stron internetowych.

W przypadku algorytmu PageRank, α jest parametrem, który kontroluje prawdopodobieństwo, że użytkownik zamiast kliknąć w link na stronie, 
będzie kontynuować losowe przeglądanie stron. Innymi słowy, α reprezentuje prawdopodobieństwo "znudzenia" użytkownika, 
który może zdecydować się na zmianę strony zamiast kontynuować przeglądanie zgodnie z linkami.

Dlaczego jest to istotne? Gdyby α było równe 1, użytkownik byłby w pełni "zainteresowany" i kontynuowałby klikanie w kolejne linki. 
W takim przypadku, istnieje ryzyko, że użytkownik może utknąć w pętli lub cyklu stron, co nie jest pożądane. 
Dlatego też wprowadzenie współczynnika znudzenia, α < 1, pomaga uniknąć takich sytuacji, umożliwiając użytkownikowi czasem przechodzenie 
na nową stronę, niezależnie od linków na bieżącej stronie.

Praktycznie, wartość α jest często ustalana na 0,85 w algorytmie PageRank, co oznacza, że istnieje 15% szansa na to, 
że użytkownik "znudzi się" i przejdzie do innej strony, zamiast kontynuować klikanie w linki. 
Ten współczynnik znudzenia pomaga zrównoważyć algorytm, poprawiając jakość wyników wyszukiwania 
i zapobiegając utknięciu w nieskończonych pętlach stron.

W ten sposób, nazywanie α "współczynnikiem znudzenia" odzwierciedla jego rolę w modelowaniu zachowania 
użytkowników i wprowadzeniu pewnej losowości w proces nawigacji po stronach internetowych.
"""


import numpy as np
from scipy.linalg import solve


def calculate_state_probability(P, num_steps, alpha, start_state=0, random_state=False):
    n = P.shape[0]
    state_vector = np.zeros(n)
    state_vector[start_state] = 1

    Jn = np.ones((n, n))
    MG = (1 - alpha) * P + alpha * (1 / n) * Jn

    if random_state:
        state_vector = np.ones(n) / n
    # breakpoint()
    power = np.linalg.matrix_power(MG, num_steps)
    state_vector = np.dot(state_vector, power)
    # for _ in range(num_steps):
    #     state_vector = np.dot(state_vector, P)

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

def calculate_stationary_distribution_many(P, alpha):
    n = P.shape[0]
    Jn = np.ones((n, n))
    MG = (1 - alpha) * P + alpha * (1 / n) * Jn

    if alpha == 0:
        MG = P
    # Wektory i wartości własne
    eigenvalues, eigenvectors = np.linalg.eig(MG.T)

    # Znajdź wartość własną najbliższą 1
    stationary_indexes = np.where(np.isclose(eigenvalues,1))[0]

    # breakpoint()
    stationary_distribution = np.zeros(n)
    for i in stationary_indexes:
        stationary_distribution += np.abs(np.real(np.transpose(eigenvectors[:, i])))
        stationary_distribution /= np.sum(stationary_distribution)

    return stationary_distribution

# Define the directed graph G and its transition matrix PG
PG = np.array(
    [
        [1, 0, 0, 0, 0, 0],
        [0, 0, 1 / 2, 0, 1 / 2, 0],
        [1, 0, 0, 0, 0, 0],
        [0, 1 / 2, 0, 0, 1 / 2, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0],
    ]
)

PG2 = np.array(
    [
        [1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 0, 0],
        [0, 1 / 2, 0, 0, 1 / 2, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0],
    ]
)

# Define the damping factor alpha values
alpha_values = [0, 0.15, 0.5, 1]

for alpha in alpha_values:
    stationary_distribution = calculate_stationary_distribution(PG, alpha)
    stationary_distribution2 = calculate_stationary_distribution(PG2, alpha)
    print(f"Alpha = {alpha}:")
    print(f"PG:\t{stationary_distribution}")
    print(f"PG2:\t{stationary_distribution2}")
    print(f"PG2(MC):\t{calculate_state_probability(PG2,100,alpha, random_state=True)}")
    print(f"PG2(many):\t{calculate_stationary_distribution_many(PG2,alpha)}")
    print()
