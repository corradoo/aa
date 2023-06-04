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


def calculate_stationary_distribution(PG, alpha):
    n = PG.shape[0]
    Jn = np.ones((n, n))
    MG = (1 - alpha) * PG + alpha * (1 / n) * Jn

    breakpoint()
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
    print()
