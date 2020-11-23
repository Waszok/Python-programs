#-*- coding: utf-8 -*-

import gi
# Wymagamy biblioteki w wersji min 3.0.
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import random  # Losowanie pozycji min na planszy.
from numpy import *  # Wykorzystujemy do reprezentacji zaktualizowanych pozycji planszy w postaci tablicy dwuwymiarowej.


class Plansza(Gtk.Grid):
    """Klasa reprezentująca planszę, dziedzicząca po Gtk.Grid.

    W konstruktorze klasy wywołujemy konstruktor klasy bazowej, tj. konstruktor klasy Gtk.Grid. Następnie w gridzie
    umieszczamy elementy typu Gtk.Button (reprezentujące poszczególne pola planszy) o rozmiarze 60x60.
    Plansza jest wielkości n x n, gdzie "n" to zmienna przekazywana w kostruktorze klasy Plansza (Użytkownik
    podaje wartośc "n" samodzielnie).
    """
    def __init__(self, n):
        """W pierwszej kolejności wywoływany jest konstruktor klasy Gtk.Grid.

        Argument "n" to wielkość tworzonej planszy.
        """
        Gtk.Grid.__init__(self)
        for i in range(n):
            for j in range(n):
                b = Gtk.Button.new_with_label('')
                b.set_size_request(60, 60)
                self.attach(b, i, j, 1, 1)


class MainWindow(Gtk.Window):
    """Główna klasa programu, odpowiedzialna za mechanikę gry."""
    def __init__(self, rozmiar_planszy):
        """Następuje inicjalizacja odpowiednich zmiennych oraz stworzenie wizualnej strony gry..

        Tworzymy obiekt klasy Plansza (self.plansza). Wartość zmiennej "rozmiar_planszy" wprowadzana jest
        przez użytkownika programu. Wszystkie elementy, tj. grid z planszą oraz przycisk do resetowania stanu gry
        umiszczone są w Gtk.VBox. Dodatkowo następuję losowanie rozmieszczenia min na planszy (ich liczba jest
        równa rozmiarowi planszy) oraz aktualizacja pozostałych pozycji wartościami odpowiadającymi liczbie min
        sąsiadujących z danym polem.
        """
        Gtk.Window.__init__(self, title="Saper")
        self.plansza = Plansza(rozmiar_planszy)  # Obiekt klasy Plansza
        self.plansza_pozycje = zeros((rozmiar_planszy, rozmiar_planszy), int)  # Zmienna przechowująca zaktualizowane
        # pozycje.
        self.liczba_odslonietych = 0  # Zmienna pomocnicza.
        self.losuj_miny(rozmiar_planszy)  # Losowanie min na planszy.
        self.aktualizuj_pozycje()  # Aktualizacja pozycji.

        for i in xrange(rozmiar_planszy):
            for j in xrange(rozmiar_planszy):
                self.plansza.get_child_at(i, j).connect("clicked", self.kliknieto, i, j)

        button_reset = Gtk.Button("Nowa gra")
        button_reset.connect("clicked", self.resetuj)
        box_glowny = Gtk.VBox()
        box_glowny.pack_start(self.plansza, False, False, 0)
        box_glowny.pack_start(button_reset, False, False, 0)
        self.add(box_glowny)

    def wypelnij_label(self, btn, x, y):
        """Funkcja wstawiająca tekst (label) do zmiennej Gtk.Button (btn) o współrzędnych x, y."""
        if self.plansza_pozycje[x][y] == -1:
            btn.get_child().set_markup('<span foreground="red" font="12"><big><b>M</b></big></span>')
        elif self.plansza_pozycje[x][y] == 0:
            btn.get_child().set_markup('<span foreground="black" font="12"><big><b>0</b></big></span>')
        elif self.plansza_pozycje[x][y] == 1:
            btn.get_child().set_markup('<span foreground="orange" font="12"><big><b>1</b></big></span>')
        elif self.plansza_pozycje[x][y] == 2:
            btn.get_child().set_markup('<span foreground="orangered" font="12"><big><b>2</b></big></span>')
        elif self.plansza_pozycje[x][y] == 3:
            btn.get_child().set_markup('<span foreground="tomato" font="12"><big><b>3</b></big></span>')
        else:
            btn.get_child().set_markup(
                '<span foreground="brown" font="12"><big><b>{:2s}</b></big></span>'
                .format(str(self.plansza_pozycje[x][y])))
        btn.set_sensitive(False)  # Dezaktywacja danego przycisku.

    def aktualizuj_pozycje(self):
        """Aktualizacja pozycji w tablicy "plansza_pozycje" w zależności od rozkładu min."""
        licznik = 0
        for i in xrange(rozmiar_planszy):
            for j in xrange(rozmiar_planszy):
                if self.plansza_pozycje[i][j] != -1:
                    l = j - 1
                    p = j + 1
                    g = i - 1
                    d = i + 1
                    u_gl = (i - 1, j - 1)
                    u_gp = (i - 1, j + 1)
                    u_dl = (i + 1, j - 1)
                    u_dp = (i + 1, j + 1)
                    if l >= 0 and self.plansza_pozycje[i][l] == -1:
                        licznik += 1
                    if p < rozmiar_planszy and self.plansza_pozycje[i][p] == -1:
                        licznik += 1
                    if g >= 0 and self.plansza_pozycje[g][j] == -1:
                        licznik += 1
                    if d < rozmiar_planszy and self.plansza_pozycje[d][j] == -1:
                        licznik += 1
                    if u_gl[0] >= 0 and u_gl[1] >= 0 and self.plansza_pozycje[u_gl[0]][u_gl[1]] == -1:
                        licznik += 1
                    if u_gp[0] >= 0 and u_gp[1] < rozmiar_planszy and self.plansza_pozycje[u_gp[0]][u_gp[1]] == -1:
                        licznik += 1
                    if u_dl[0] < rozmiar_planszy and u_dl[1] >= 0 and self.plansza_pozycje[u_dl[0]][u_dl[1]] == -1:
                        licznik += 1
                    if u_dp[0] < rozmiar_planszy and u_dp[1] < rozmiar_planszy and \
                            self.plansza_pozycje[u_dp[0]][u_dp[1]] == -1:
                        licznik += 1
                    self.plansza_pozycje[i][j] = licznik
                    licznik = 0

    def losuj_miny(self, x):
        """Funkcja losująca x pozycji na planszy, w których rozmieszczone zostaną miny na początku gry."""
        self.lista_wyl = []
        for i in range(x):
            self.wyl = (random.randint(0, x), random.randint(0, x))
            while self.znajdz(self.wyl[0], self.wyl[1], self.lista_wyl) == 1:
                self.wyl = (random.randint(0, x), random.randint(0, x))
            self.lista_wyl.append(self.wyl)
        for element in self.lista_wyl:
            self.plansza_pozycje[element[0]][element[1]] = -1

    def znajdz(self, i, j, tab):
        """Funkcja pomocnicza służąca do znalezienia odpowiednich elementów w podanej w argumencie tablicy.

        Jeśli współrzędne elementu są równe odpowiednio wartościom "i" oraz "j" przekazanym
        w argumencie, to funkcja zwraca wartośći 1, w przeciwnym wypadku zwraca 0.
        """
        for (a, b) in tab:
            if (a, b) == (i, j):
                return 1
        return 0

    def czy_wygrana(self, x, y):
        """Funkcja sprawdzająca obecny stan gry i wyświetlająca okno z komunikatem o wygranej lub przegranej."""
        if self.plansza_pozycje[x][y] == -1:
            dialog = Gtk.MessageDialog(parent=self, type=Gtk.MessageType.INFO,
                                       buttons=Gtk.ButtonsType.OK, message_format="PRZEGRANA")
            dialog.connect("response", self.dialog_response)
            dialog.show()
            return 1
        if self.plansza_pozycje[x][y] != -1 and self.liczba_odslonietych == rozmiar_planszy ** 2 - rozmiar_planszy:
            dialog = Gtk.MessageDialog(parent=self, type=Gtk.MessageType.INFO,
                                       buttons=Gtk.ButtonsType.OK, message_format="WYGRANA")
            dialog.connect("response", self.dialog_response)
            dialog.show()
            return 1
        return 0

    def dialog_response(self, widget, response_id):
        """Obsługa okienka z komunikatem."""
        if response_id == Gtk.ResponseType.OK:
            widget.destroy()

    def kliknieto(self, btn, x, y):
        """Funkcja obsługująca sygnał wysłany podczas kliknięcia na dowolne pole planszy (przycisk Button)."""
        self.wypelnij_label(btn, x, y)
        self.liczba_odslonietych += 1
        if self.czy_wygrana(x, y) == 1:
            for i in xrange(rozmiar_planszy):
                for j in xrange(rozmiar_planszy):
                    if self.plansza.get_child_at(i, j).get_sensitive():
                        self.wypelnij_label(self.plansza.get_child_at(i, j), i, j)
                        self.plansza.get_child_at(i, j).set_sensitive(False)

    def resetuj(self, btn):
        """Funkcja obsługująca sygnał wysłany w momencie kliknięcia w przycisk "button_reset", czyli "Nowa gra".

        Następuje w niej zerowanie odpowiednich tablic i zmiennych oraz ponowne losowanie min.
        """
        for i in xrange(rozmiar_planszy):
            for j in xrange(rozmiar_planszy):
                self.plansza.get_child_at(i, j).set_label('')
                self.plansza.get_child_at(i, j).set_sensitive(True)
        self.plansza_pozycje = zeros((rozmiar_planszy, rozmiar_planszy), int)
        self.liczba_odslonietych = 0
        self.losuj_miny(rozmiar_planszy)
        self.aktualizuj_pozycje()
        print self.plansza_pozycje


if __name__ == "__main__":
    print 'Podaj rozmiary planszy: '
    rozmiar_planszy = int(raw_input())
    win = MainWindow(rozmiar_planszy)
    win.connect("delete-event", lambda x, y: Gtk.main_quit())
    win.show_all()
    Gtk.main()