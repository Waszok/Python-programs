import matplotlib.pyplot as plt
import numpy as np

def linear(x, y):
    """ Interpolacja liniowa, rysowana na podstawie przekazanych w argumencie list punktow postaci (x, y).

    x -- lista wspolrzednych x,
    y -- lista wposlrzednych y.
    linewidth - szerokosc linii, kolor czerwony.
    """
    plt.plot(x, y, linewidth=1.5, color='r')


def nearest(x, y):
    """ Interpolacja typu nearest, rysowana na podstawie przekazanych w argumencie list punktow postaci (x, y)."""
    tab_x = [] #  Tablica przechowujaca ostateczne wartosci x.
    tab_y = [] #  Tablica pomocnicza przechowujaca ostateczne wartosci y.
    pom_1 = [] #  Tablica pomocnicza.
    pom_2 = [] #  Tablica pomocnicza.
    for i in range(len(x) - 1):
        pom_1.append((x[i + 1] - x[i])/2.0)
    for j in range(len(y) - 1):
        pom_2.append(y[j + 1] - y[j])
    for index, (s, m) in enumerate(zip(x, y)):
        if index < len(x) - 1:
            # Rysujemy linie poziome od danego x do polowy odcinka x[i+1] - x[i].
            for xi in np.arange(s, s + pom_1[index] + 0.1, 0.1):
                tab_x.append(xi)
                tab_y.append(m)
            # Rysujemy linie ukosna.
            tab_x.append(s + pom_1[index] + 0.1)
            tab_y.append(m + pom_2[index])
            # Rysujemy linie poziome od polowy odcinka x[i+1] - x[i] do kolejnego x.
            for xi in np.arange(s + pom_1[index] + 0.2, s + 2 * pom_1[index], 0.1):
                tab_x.append(xi)
                tab_y.append(m + pom_2[index])
    plt.plot(tab_x, tab_y, linewidth=1.5, color='y')

def zero(x, y):
    """ Interpolacja typu zero, rysowana na podstawie przekazanych w argumencie list punktow postaci (x, y)."""
    tab_x = [] #  Tablica przechowujaca ostateczne wartosci x.
    tab_y = [] # Tablica pomocnicza przechowujaca ostateczne wartosci y.
    pom_1 = [] #  Tablica pomocnicza.
    pom_2 = [] #  Tablica pomocnicza.
    for i in range(len(x) - 1):
        pom_1.append(x[i + 1] - x[i])
    for j in range(len(y) - 1):
        pom_2.append(y[j + 1] - y[j])
    for index, (s, m) in enumerate(zip(x, y)):
        if index < len(x) - 1:
            for xi in np.arange(s, s + pom_1[index], 0.1):
                tab_x.append(xi)
                tab_y.append(m)
            tab_x.append(s + pom_1[index])
            tab_y.append(m + pom_2[index])
    plt.plot(tab_x, tab_y, linewidth=1.5, color='c')

def lagrange(x, y):
    """ Interpolacja Lagrange'a, rysowana na podstawie przekazanych w argumencie list punktow postaci (x, y).

    Dokladniej, przekazujemy dwie listy, wspolrzednych x oraz wspolrzednych y.
    """
    tab_x = [] #  Lista pomocnicza
    tab_y = [] #  Lista pomocnicza.
    for d in np.arange(x[0], x[len(x) - 1], 0.01):
        w = 0 # Przechowuje wartosci wielomianu, ostateczne y.
        for i in range(len(x)):
            iloczyn = 1 #  Zmienna przechowujaca kolejne iloczyny ze wzoru na wielomian interpolujacy.
            for j in range(len(x)):
                if j != i:
                    iloczyn *= (d - x[j])/(x[i] - x[j])
            w += y[i] * iloczyn
        tab_x.append(d)
        tab_y.append(w)
    plt.plot(tab_x, tab_y, linewidth=1.5, color='b')

def draw_points(x, y):
    """Funkcja rysujaca kolejne punkty (x, y) na podstawie ktorych dokonujemy interpolacji."""
    plt.plot(x, y, 'ro', color='b', markersize='8')

x = np.arange(0, 10) #  Przykladowy zbior wartosci x - argumentow funkcji.
y = np.sin(x) #  Przykladowa funkcja ktora chcemy interpolowac.

#  Wywolujemy kolejne funkcje funkcje dokonujace poszczegolnych interpolacji:
draw_points(x, y)
linear(x, y)
lagrange(x, y)
nearest(x, y)
zero(x, y)

# Ustawiamy siatke oraz podpisujemy osie Ox i Oy:
plt.grid(color=(0.7, 0.8, 1.0), linestyle='-')
plt.ylabel('Interpolacja wartosci $y$', fontsize=23)
plt.xlabel('Wartosci $x$', fontsize=23)

# Rysujemy legende:
plt.legend(('punkty','linear', 'Lagrange', 'nearest', 'zero'), loc=(0.01, 0.01), handlelength=1.5)
plt.show()