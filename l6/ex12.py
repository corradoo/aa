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
from markov import (
    calculate_stationary_distribution_many,
    calculate_stationary_distribution,
    calculate_state_probability,
)

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

alpha_values = [0, 0.15, 0.5, 1]

for alpha in alpha_values:
    stationary_distribution = calculate_stationary_distribution(PG, alpha)
    stationary_distribution2 = calculate_stationary_distribution(PG2, alpha)
    print(f"Alpha = {alpha}:")
    print(f"PG:\t\t{[round(n,3) for n in stationary_distribution]}")
    print(f"PG2:\t\t{[round(n,3) for n in stationary_distribution2]}")
    print(f"PG2(MC):\t{[round(n,3) for n in calculate_state_probability(PG2,100,alpha, random_state=True)]}")
    print(f"PG2(many):\t{[round(n,3) for n in calculate_stationary_distribution_many(PG2,alpha)]}")
    print()
