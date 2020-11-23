#-*- coding: utf-8 -*-

import gi
# wymagamy biblioteki w wersji min 3.0
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
import random  #losowanie pozycji na planszy

class MainWindow(Gtk.Window):
    def __init__(self):
        """Następuje inicjalizacja odpowiednich zmiennych oraz stworzenie wizualnej strony gry..

        Tworzymy odpowiednie kontenery, do których dodajemy przyciski (odpowiednio ToggleButtons reprezentujące pola
        planszy, umieszczone w zmiennej "grid" oraz Button, zmienna "button_reset") i obiekty typu Label.
        Plansza gry na starcie zostaje wypełniona 50 wylosowanymi kulami. Wartości 0 w zmiennej "plansza" przechowują
        informację o tym, że dane pole jest puste, 1 - na danym polu umieszczona jest kula.
        """
        Gtk.Window.__init__(self, title="Kulki")
        self.stan = 0 # Zmienna pomocnicza wykorzystywana w funkcji "kliknieto()".
        self.wspl_stanu_1 = (-1, -1) # Zmienna pomocnicza przechowująca informację o pozycji przycisku (z którego
                                     # pobieramy kulę), mającego zostać dezaktywowanym po umieszczeniu wybranej
                                     # kuli na pustym polu.
        self.wspl_stanu_2 = (-1, -1) # Zmienna pomocnicza przechowująca informację o pozycji przycisku (do którego
                                     # "przenosimy" kulę), mającego zostać dezaktywowanym po umieszczeniu wybranej
                                     # kuli na pustym polu.
        self.s = 0 # Zmienna pomocnicza, przechowująca kolor, wykorzystywana w funkcji "kliknieto()".
        self.a = 0 # Zmienna przechowująca liczbę punktów podczas danej rozgrywki.
        self.b = "" # Pomocnicza zmienna - początkowo labelki tworzące pozycje rankingu są puste, zmienna "self.b" jest
                    # pustym napisem.
        self.tablica_rankingowa = [] # Lista przechowująca kolejne wyniki punktowe po zakończonej grze.
        self.licznik_aktywacji = 0 # Zmienna pomocnicza, wykorzystywana w funkcji "kliknieto()".
        self.kule_do_usuniecia = [] # Lista elementów do usunięcia z planszy po wykonaniu metody sprawdz_czy_piec().
        # Pomocnicze zmienne do przechowywania obrazu pobieranego i wstawianego do ToggleButton.
        self.image = Gtk.Image.new_from_pixbuf()
        self.image_2 = Gtk.Image.new_from_pixbuf()
        self.plansza = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        self.tablica_nazw = ["kulka1.svg", "kulka2.svg", "kulka3.svg", "kulka4.svg", "kulka5.svg"]

        self.lista_wylosowanych = [] # Lista przechowująca pozycje kul na planszy.
        self.lista_kul = [] # Lista przechowująca pozycje kul na planszy wraz z ich kolorami.
        self.losuj_kule(50) # Losujemy pozycje na planszy, do których wstawimy kule.
        grid = Gtk.Grid() # Zawiera poszczególne buttony tworzące planszę gry.

        # Tworzymy i wstawiamy do grida przyciski na wylosowanych pozycjach wraz z odpowiednimi (wylosowanymi) kulami.
        for i in range(10):
            for j in range(10):
                b = Gtk.ToggleButton()
                b.set_size_request(40, 40)
                if self.znajdz(i, j, self.lista_wylosowanych) == 1:
                    k = random.randint(0, 4)
                    b.set_image(Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.
                                                          new_from_file_at_size(self.tablica_nazw[k], 35, 35)))
                    self.plansza[i][j] = 1
                    self.lista_kul.append((k, i, j))
                grid.attach(b, i, j, 1, 1)
                b.connect("clicked", self.kliknieto, i, j)
                b.connect("released", self.puszczono, grid)

        box_glowny = Gtk.VBox() # "Wyjściowy" box, w którym umieszczone są pozostałe boxy i button do resetowania gry.
        box_posredni = Gtk.HBox() # Kontener zawierający grid z planszą oraz box odpowiedzialny za ranking.
        box_ranking = Gtk.VBox() # Przechowuje odpowiednie labelki do wyświetlania rankingu.
        # Ustawiamy rozmiary boxów:
        box_posredni.set_size_request(480, 40)
        box_ranking.set_size_request(80, 400)

        # Tworzymy kolejne labelki przechowujące odpowiednio:
        # -- label - tekst wyświetlające liczbę punktów gracza,
        # -- label2 - wyświetla słowo "Ranking",
        # -- label_r1, label_r2, label_r3, label_r4, label_r5 - kolejne pozycje w rankingu (maksymalnie 5), jeśli
        # jest mniej niż pięć, to pozostałe labelki są puste.
        # Dodatkowo odpowiednio modyfikujemy wygląd napisów (grubość, wielkość czcionki) i ich położenie.

        self.label = Gtk.Label()
        self.label.set_markup('<span foreground="black"><big><b>Liczba punktów: </b></big></span>'
                         + '<span foreground="black"><big><b>{:10s}</b></big></span>'.format(str(self.a)))
        self.label.set_xalign(0.013)

        label2 = Gtk.Label()
        label2.set_markup('<span foreground="black"><big><b>Ranking: </b></big></span>')
        label2.set_yalign(0)

        self.label_r1 = Gtk.Label()
        self.label_r1.set_markup('<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str(self.b))
                         + '<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str(self.b)))
        self.label_r2 = Gtk.Label()
        self.label_r2.set_markup('<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str(self.b))
                                 + '<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str(self.b)))
        self.label_r3 = Gtk.Label()
        self.label_r3.set_markup('<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str(self.b))
                                 + '<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str(self.b)))
        self.label_r4 = Gtk.Label()
        self.label_r4.set_markup('<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str(self.b))
                                 + '<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str(self.b)))
        self.label_r5 = Gtk.Label()
        self.label_r5.set_markup('<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str(self.b))
                                 + '<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str(self.b)))

        box_glowny.pack_start(self.label, False, False, 0)
        box_ranking.pack_start(label2, False, False, 0)
        box_ranking.pack_start(self.label_r1, False, False, 0)
        box_ranking.pack_start(self.label_r2, False, False, 0)
        box_ranking.pack_start(self.label_r3, False, False, 0)
        box_ranking.pack_start(self.label_r4, False, False, 0)
        box_ranking.pack_start(self.label_r5, False, False, 0)

        box_posredni.pack_start(box_ranking, False, False, 0)
        box_posredni.pack_start(grid, True, True, 0)

        button_reset = Gtk.Button("Graj od początku")
        button_reset.connect("clicked", self.wyczysc, grid)

        box_glowny.add(box_posredni)
        box_glowny.add(button_reset)
        self.add(box_glowny)

    def aktualizuj_ranking(self):
        """
        Funkcja aktualizująca ranking wyświetlany w oknie gry.

        W zależności od długości listy "tablica_rankingowa" wyświetlamy odpowiednią liczbę labeli, maksymalnie możemy
        wyświetlić 5 najlepszych wyników (tablicę sortujemy nierosnąco), jednak długość listy może być większa,
        wybieramy pierwsze 5 bądź mniej elementów.
        """
        self.liczba = 0
        for i in range(10):
            for j in range(10):
                if self.plansza[i][j] != 0:
                    self.liczba += 1
        if self.liczba == 100:
            self.tablica_rankingowa.append(self.a)
            self.tablica_rankingowa.sort(reverse=True)
            self.dlugosc = len(self.tablica_rankingowa)
            if self.dlugosc == 1:
                self.label_r1.set_markup('<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str("1."))
                + '<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str(self.tablica_rankingowa[0])))
            elif self.dlugosc == 2:
                self.label_r1.set_markup('<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str("1."))
                + '<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str(self.tablica_rankingowa[0])))
                self.label_r2.set_markup('<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str("2."))
                + '<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str(self.tablica_rankingowa[1])))
            elif self.dlugosc == 3:
                self.label_r1.set_markup('<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str("1."))
                + '<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str(self.tablica_rankingowa[0])))
                self.label_r2.set_markup('<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str("2."))
                + '<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str(self.tablica_rankingowa[1])))
                self.label_r3.set_markup('<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str("3."))
                + '<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str(self.tablica_rankingowa[2])))
            elif self.dlugosc == 4:
                self.label_r1.set_markup('<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str("1."))
                + '<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str(self.tablica_rankingowa[0])))
                self.label_r2.set_markup('<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str("2."))
                + '<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str(self.tablica_rankingowa[1])))
                self.label_r3.set_markup('<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str("3."))
                + '<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str(self.tablica_rankingowa[2])))
                self.label_r4.set_markup('<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str("4."))
                + '<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str(self.tablica_rankingowa[3])))
            elif self.dlugosc >= 5:
                self.label_r1.set_markup('<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str("1."))
                + '<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str(self.tablica_rankingowa[0])))
                self.label_r2.set_markup('<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str("2."))
                + '<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str(self.tablica_rankingowa[1])))
                self.label_r3.set_markup('<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str("3."))
                + '<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str(self.tablica_rankingowa[2])))
                self.label_r4.set_markup('<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str("4."))
                + '<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str(self.tablica_rankingowa[3])))
                self.label_r5.set_markup('<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str("5."))
                + '<span foreground="black"><big><b>{:5s}</b></big></span>'.format(str(self.tablica_rankingowa[4])))

    def sprawdz_czy_piec(self):
        """
        Funkcja sprawdzająca, czy na planszy wystąpiły kule tego samego koloru w jednym rzędzie, kolumnie, bądż na skos.

        W zmiennej "kolor" przechowujemy kolor kuli znajdującej się na danej pozycji (i, j). Przekazujemy ją do funkcji
        "zgodnosc", która zwraca informację o tym, czy na odpowiedniej pozycji znajduje się kula o danym kolorze,
        zgodnym z kolorem w zmiennej "kolor".
        Jeśli zostały znalezione pola z odpowiednim układem kul, to zapisujemy je do listy "kule_do_usuniecia".
        """
        for i in range(10):
            for j in range(10):
                l_1 = i + 1
                l_2 = j + 1
                u_11 = i + 1
                u_12 = j + 1
                u_21 = i + 1
                u_22 = j - 1
                if self.plansza[i][j] != 0:
                    self.kolor = self.znajdz_kolor(i, j, self.lista_kul)
                    for k in range(4):
                        if l_1 >= 0 and l_1 < 10 and self.plansza[l_1][j] != 0 and self.zgodnosc(self.kolor, l_1, j)==1:
                            l_1 += 1
                        if l_2 >= 0 and l_2 < 10 and self.plansza[i][l_2] != 0 and \
                                self.zgodnosc(self.kolor, i, l_2) == 1:
                            l_2 += 1
                        if u_11 >= 0 and u_12 >= 0 and u_11 < 10 and u_12 < 10 and self.plansza[u_11][u_12] != 0 and \
                                self.zgodnosc(self.kolor, u_11, u_12) == 1:
                            u_11 += 1
                            u_12 += 1
                        if u_21 >= 0 and u_22 >= 0 and u_21 < 10 and u_22 < 10 and self.plansza[u_21][u_22] != 0 and \
                               self.zgodnosc(self.kolor, u_21, u_22) == 1:
                            u_21 += 1
                            u_22 -= 1
                if l_1 == i + 5:
                    for w in range(5):
                        if self.znajdz(i + w, j, self.kule_do_usuniecia) == 0:
                            self.kule_do_usuniecia.append((i + w,j))
                if l_2 == j + 5:
                    for w in range(5):
                        if self.znajdz(i, j + w, self.kule_do_usuniecia) == 0:
                            self.kule_do_usuniecia.append((i, j + w))
                if u_11 == i + 5 and u_12 == j + 5:
                    for [w, h] in zip(range(5), range(5)):
                        if self.znajdz(i + w, j + h, self.kule_do_usuniecia) == 0:
                            self.kule_do_usuniecia.append((i + w, j + h))
                if u_21 == i + 5 and u_22 == j - 5:
                    for [w, h] in zip(range(5), range(5)):
                        if self.znajdz(i + w, j - h, self.kule_do_usuniecia) == 0:
                            self.kule_do_usuniecia.append((i + w, j - h))

    def dodaj_nowe(self, grid):
        """W zależności od ilości wolnych pól na planszy funkcja losuje i wstawia 3, 2 lub 1 kulę po każdym ruchu."""

        self.licznik = 0 # Zmienna pomocnicza.
        for i in range(10):
            for j in range (10):
                if self.plansza[i][j] == 0:
                    self.licznik += 1
        if self.licznik >= 3:
            self.losuj_kule(3)
            dlg = len(self.lista_wylosowanych)
            for s in range(1, 4):
                k = random.randint(0, 4)
                grid.get_child_at(self.lista_wylosowanych[dlg - s][0], self.lista_wylosowanych[dlg - s][1])\
                    .set_image(Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.
                                                         new_from_file_at_size(self.tablica_nazw[k], 35, 35)))
                self.plansza[self.lista_wylosowanych[dlg - s][0]][self.lista_wylosowanych[dlg - s][1]] = 1
                self.lista_kul.append((k, self.lista_wylosowanych[dlg - s][0], self.lista_wylosowanych[dlg - s][1]))
        elif self.licznik == 2:
            self.losuj_kule(2)
            dlg = len(self.lista_wylosowanych)
            for s in range(1, 3):
                k = random.randint(0, 4)
                grid.get_child_at(self.lista_wylosowanych[dlg - s][0], self.lista_wylosowanych[dlg - s][1]) \
                    .set_image(Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.
                                                         new_from_file_at_size(self.tablica_nazw[k], 35, 35)))
                self.plansza[self.lista_wylosowanych[dlg - s][0]][self.lista_wylosowanych[dlg - s][1]] = 1
                self.lista_kul.append((k, self.lista_wylosowanych[dlg - s][0], self.lista_wylosowanych[dlg - s][1]))
        elif self.licznik == 1:
            self.losuj_kule(1)
            dlg = len(self.lista_wylosowanych)
            k = random.randint(0, 4)
            grid.get_child_at(self.lista_wylosowanych[dlg - 1][0], self.lista_wylosowanych[dlg - 1][1]) \
                    .set_image(Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.
                                                         new_from_file_at_size(self.tablica_nazw[k], 35, 35)))
            self.plansza[self.lista_wylosowanych[dlg - 1][0]][self.lista_wylosowanych[dlg - 1][1]] = 1
            self.lista_kul.append((k, self.lista_wylosowanych[dlg - 1][0], self.lista_wylosowanych[dlg - 1][1]))
            self.licznik = 0

    def usun_z_planszy(self, grid):
        """Funkcja usuwająca kule z planszy zgodnie z tymi, które zostały wstawione do listy "kule_do_usuniecia"."""
        for (i, j) in self.kule_do_usuniecia:
            self.image_2 = grid.get_child_at(i,j).get_image()
            self.image_2.clear()
            self.plansza[i][j] = 0
            self.lista_wylosowanych.pop(self.znajdz_do_usuniecia(i, j, self.lista_wylosowanych))
            self.lista_kul.pop(self.znajdz_do_usuniecia_2(i, j, self.lista_kul))
        self.kule_do_usuniecia = []

    def losuj_kule(self, x):
        """Funkcja losująca x pozycji na planszy, na których umieszczone zostaną kule na początku gry."""
        for i in range(x):
            self.tupla_wyl = (random.randint(0, 9), random.randint(0, 9))
            while self.znajdz(self.tupla_wyl[0], self.tupla_wyl[1],self.lista_wylosowanych) == 1:
                self.tupla_wyl = (random.randint(0, 9), random.randint(0, 9))
            self.lista_wylosowanych.append(self.tupla_wyl)

    def znajdz(self, i, j, tab):
        """Funkcja pomocnicza służąca do znalezienia odpowiednich elementów w podanej w argumencie tablicy.

        Jeśli współrzędne elementu są równe odpowiednio wartościom "i" oraz "j" przekazanym
        w argumencie, to funkcja zwraca wartośći 1, w przeciwnym wypadku zwraca 0.
        """
        for (a, b) in tab:
            if (a, b) == (i, j): return 1
        return 0

    def znajdz_do_usuniecia(self, i, j, tab):
        """Funkcja zwracająca indeks elementu tablicy "tab", którego wartość jest równa wartośći (i, j) z argumentu."""
        for index, (a, b) in enumerate(tab):
            if (a, b) == (i, j): return index
        return -1

    def znajdz_kolor(self, i, j, tab):
        """Funkcja zwracająca kolor kulki umieszczonej na pozycji (i, j)."""
        for (a, b, c) in tab:
            if (b, c) == (i, j): return a
        return -1

    def znajdz_do_usuniecia_2(self, i, j, tab):
        """Funkcja pomocnicza, zwracająca indeks elementu tablicy "tab", spełniającego określoną zależność

        Jeśli druga i trzecia współrzędna elementu są równe odpowiednio wartościom "i" oraz "j" przekazanym
        w argumencie, to następuje zwrócenie indeksu tablicy "tab".
        """
        for index, (a, b, c) in enumerate(tab):
            if (b, c) == (i, j): return index
        return -1

    def zgodnosc(self, k, i, j):
        """Funkcja porównująca elementy listy "lista_kul" z wartościami przekazanymi w argumencie.

        Jeśli dany element z listy "lista_kul" jest równy elementowi "(k, i, j)", czyli elementowi złożonemu
        z przekazanych argumentów to funkcja zwraca 1, w przeciwnym wypadku zwraca 0.
        """
        for (a, b, c) in self.lista_kul:
            if (a, b, c) == (k, i, j): return 1
        return -1


    def aktualizuj(self, a, b, c, zadanie):
        """Funkcja aktualizująca wartości list "lista_kul" i "lista_wylosowanych" w zależności od argumentu "zadanie".

        Jeśli do owej funkcji jako czwarty argument przekażemy 1, to z list "lista_kul" i "lista_wylosowanych" zostanie
        usunięty element (tupla) o wartości (a, b, c) - a, b, c to zmienne przekazane w argumencie funkcji.
        Jeśli natomiast czwarty argument będzie wynosić 2, to wspomniana tupla zostanie dodana do powyższych list.
        Funkcja wykorzystywana jest podczas "zdejmowania" kuli z przycisku w momencie kliknięcia na dane pole planszy
        i umieszczania tejże kuli w innym (pustym) wskazanym przez gracza polu.
        """
        if zadanie == 1:
            for index, (i, j, k) in enumerate(self.lista_kul):
                if (i, j, k) == (a, b, c):
                    self.lista_kul.pop(index)
                    self.lista_wylosowanych.pop(self.znajdz_do_usuniecia(j, k, self.lista_wylosowanych))
        elif zadanie == 2:
            self.lista_kul.append((a, b, c))
            self.lista_wylosowanych.append((b, c))

    def kliknieto(self, btn, x, y):
        """Funkcja obsługująca sygnał wysłany podczas kliknięcia na dowolne pole planszy (przycisk ToggleButton).

        W zależności od zmiennych pomocniczych "stan" oraz "licznik_aktywacji" dokonujemy odpowiedniej
        aktualizacji kul na planszy podczas kliknięcia w dane pole, tj. wstawienie, bądź usunięcie kuli.
        """
        if self.licznik_aktywacji != 2:
            if self.plansza[x][y] != 0 and self.stan == 0:
                self.licznik_aktywacji += 1
                self.wspl_stanu_1 = (x, y)
                self.image = btn.get_image()
                self.s = self.znajdz_kolor(x, y, self.lista_kul)
                self.aktualizuj(self.s, x, y, 1)
                self.stan = 1
            elif self.plansza[x][y] == 0 and self.stan == 0:
                btn.set_active(False)
            elif self.plansza[x][y] == 0 and self.stan == 1:
                self.licznik_aktywacji += 1
                self.wspl_stanu_2 = (x, y)
                btn.set_image(Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.
                                                        new_from_file_at_size(self.tablica_nazw[self.s], 35, 35)))
                self.image.clear()
                self.aktualizuj(self.s, x, y, 2)
                self.stan = 0
                self.plansza[x][y] = 1
                self.plansza[self.wspl_stanu_1[0]][self.wspl_stanu_1[1]] = 0
            elif self.plansza[x][y] != 0 and self.stan == 1:
                btn.set_active(False)

    def puszczono(self, btn, grid):
        """Funkcja obsługująca sygnał wysłany podczas puszczenia przycisku myszy po kliknięciu na dane pole planszy.

        W funkcji tej dezaktywujemy aktywne przyciski, aktualizujemy punktację oraz układ kul na planszy,
        czyli jeśli wystąpiło 5 kul tego samego koloru w rzędzie, kolumnie, bądź na skos, to usuwamy je, dodatkowo
        losujemy 3 (lub mniej - w zależności od liczby wolnych pól) kolejne kule, które umieszczamy na planszy.
        """
        if self.licznik_aktywacji == 2 and self.licznik_aktywacji != 0:
            grid.get_child_at(self.wspl_stanu_1[0], self.wspl_stanu_1[1]).set_active(False)
            grid.get_child_at(self.wspl_stanu_2[0], self.wspl_stanu_2[1]).set_active(False)
            self.licznik_aktywacji = 0
            self.a += 1
            self.label.set_markup('<span foreground="black"><big><b>Liczba punktów: </b></big></span>'
                                  + '<span foreground="black"><big><b>{:10s}</b></big></span>'.format(str(self.a)))

            self.sprawdz_czy_piec()
            self.usun_z_planszy(grid)
            self.dodaj_nowe(grid)
            self.sprawdz_czy_piec()
            self.usun_z_planszy(grid)
            self.aktualizuj_ranking()

    def wyczysc(self, btn, grid):
        """Funkcja obsługująca sygnał wysłany w momencie kliknięcia w przycisk "button_reset", czyli "Graj od początku".

        Następuje w niej zerowanie odpowiednich tablic i zmiennych, zerowanie planszy oraz ponowne losowanie 50 kul.
        Liczba punktów również od tego momentu liczona będzie od nowa. Rozpoczyna się nowa rozgrywka.
        """
        for i in range(10):
            for j in range(10):
                if self.plansza[i][j] != 0:
                    self.image = grid.get_child_at(i, j).get_image()
                    self.image.clear()
                    self.plansza[i][j] = 0
        self.stan = 0
        self.wspl_stanu_1 = (-1, -1)
        self.wspl_stanu_2 = (-1, -1)
        self.s = 0
        self.a = 0
        self.licznik_aktywacji = 0
        self.kule_do_usuniecia = []
        self.lista_wylosowanych = []
        self.lista_kul = []
        self.losuj_kule(50)
        for i in range(10):
            for j in range(10):
                if self.znajdz(i, j, self.lista_wylosowanych) == 1:
                    k = random.randint(0, 4)
                    grid.get_child_at(i, j).\
                        set_image(Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.
                                                            new_from_file_at_size(self.tablica_nazw[k], 35, 35)))
                    self.plansza[i][j] = 1
                    self.lista_kul.append((k, i, j))
        self.label.set_markup('<span foreground="black"><big><b>Liczba punktów: </b></big></span>'
                             + '<span foreground="black"><big><b>{:10s}</b></big></span>'.format(str(self.a)))


if __name__ == "__main__":
    win = MainWindow()
    win.connect("delete-event", lambda x, y: Gtk.main_quit())
    win.show_all()
    Gtk.main()