# -*- coding: utf-8 -*-
# UWAGA: ze względu na wielkość plików xml program wykonuje się około 2-3 min.
import matplotlib.pyplot as plt
import StringIO
import xml.etree.ElementTree as ET

#: Tworzymy szablon dokumentu
root = ET.Element("html")

# Nagłówek z tytułem:
head = ET.SubElement(root, "head")
title = ET.SubElement(head, "title")
title.text = "Wykresy"

#: Zawartość
body = ET.SubElement(root, "body")
#: Tworzymy pierwszy paragraf
paragraph = ET.SubElement(body, "p")
#: Dodajemy tekst "WYKRESY" do utworzonego paragrafu:
paragraph.text = "WYKRESY:"

#: Lista przechowująca nazwy poszczególnych plików xml:
countries = ['cze_Country_en_xml_v2.xml', 'deu_Country_en_xml_v2.xml',
             'pol_Country_en_xml_v2.xml', 'ukr_Country_en_xml_v2.xml']

#: Lista przechowująca nazwy kluczy identyfikujących interesujące nas dane:
keys = ['AG.LND.AGRI.ZS', 'NE.EXP.GNFS.CD', 'EN.POP.DNST', 'ST.INT.ARVL']

#: Zmienne odpowiedzialne za utworzenie czterech wykresów:
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()
fig4, ax4 = plt.subplots()

#: Lista przechowująca wszystkie pobrane dane, z których wyciągamy wyłącznie określone wartości
data_tmp = []
#: Lista przechowująca dane dla wykresów (ostateczne)
data = [([], []), ([], []), ([], []), ([], [])]


def get_data(element, type_chart):
    """Funkcja pobierająca dane z pliku i zwracająca dwie listy zawierające odpowiednie wielkości (rok, wartość).

    Parsujemy dane z pliku xml o nazwie "element" przekazanej w argumencie, jeżeli odpowiedni klucz jest równy
    "type_chart" (rodzaj danych, np. gęstość zalednienia, wskazany w argumencie tejże funkcji) oraz wartość (value)
    jest różna od NONE, to do pierwszej listy dodajemy rok, do drugiej zaś ową wartość.
    """
    tree_country1 = ET.parse(element)
    root_country1 = tree_country1.getroot()
    listx = []
    listy = []
    for record in root_country1[0].findall('record'):
        if record[1].get('key') == type_chart:
            year = record[2].text
            value = record[3].text
            if type(value) is str:
                listx.append(int(year))
                listy.append(float(value))
    return listx, listy


def transfer(data_tmp, data):
    """Funkcja sprawdzająca, czy dane dla odpowiednich lat dostępne są dla wszystkich czterech krajów.

    Dokładniej, przechodzimy po liście "data_tmp" i zapisujemy w pomocniczej liście "to_remove" te dane, które
    spełniają odpowiedni warunek i których nie będziemy chcieli uwzględniać podczas rysowania wykresów.
    Lista "data_tmp" składa się z czterech tupli, sprawdzamy wyłącznie pierwsze elementy
    tych tupli, czyli np. dla (a,b), sprawdzamy tylko element a (w tym przypadku są to listy) i jeśli wspomniane
    "pierwsze elementy" wszystkich z czterech tupli zawierają daną wartość (rok) to trafi ona do listy "data",
    w przeciwnym razie trafia do listy "to_remove" i ostatecznie nie zostaje przekopiowana.
    """
    to_remove = []
    for x in range(4):
        to_remove.append([])
    for i in range(4):
        for k in range(len(data_tmp[i][0])):
            if ((data_tmp[i][0][k] not in data_tmp[0][0]) or (data_tmp[i][0][k] not in data_tmp[1][0]) or
               (data_tmp[i][0][k] not in data_tmp[2][0]) or (data_tmp[i][0][k] not in data_tmp[3][0])):
                to_remove[i].append(data_tmp[i][0][k])
    for i in range(4):
        for j in range(len(data_tmp[i][0])):
            if data_tmp[i][0][j] not in to_remove[i]:
                data[i][0].append(data_tmp[i][0][j])
                data[i][1].append(data_tmp[i][1][j])


def create(fig):
    """Funkcja dodająca odpowiednie obrazki (wykresy) w formacie "svg" do dokumentu.

    W argumencie przekazujemy "uchwyt" do odpowiedniego wykresu ("fig").
    """
    imgdata = StringIO.StringIO()  # Bufor 'imitujący' obiekt pliku.
    fig.savefig(imgdata, format="svg")

    svg_txt = imgdata.getvalue()  # Pobieramy dane z bufora.
    imgdata.close()  # Czyścimy bufor ("zamykamy" wirtualny plik).

    ET.register_namespace("", "http://www.w3.org/2000/svg")
    ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')

    svg_tree_root = ET.fromstring(svg_txt)  # Wczytujemy dokument, metoda fromstring zwraca korzeń, czyli element svg.
    paragraph = ET.SubElement(body, "p")
    paragraph.append(svg_tree_root)  # Dodajemy obrazek do dokumentu.


# Rysujemy odpowiednie wykresy, zgodnie z danymi w liście "dane", dodajemy podpisy, legendy i wywołujemy funkcję
# "create()" dla każdego z czterech obrazków, która tworzy nowy paragraf i zapisuje obrazek do dokumentu:
for index, k in enumerate(keys):
    for i in countries:
        data_tmp.append(get_data(i, k))
    transfer(data_tmp, data)
    if index == 0:
        for s in range(4):
            ax1.plot(data[s][0], data[s][1])
            ax1.set_title(u'Wielkość obszarów uprawnych', fontsize=15)
            leg = ax1.legend(('Czechy', 'Niemcy', 'Polska', 'Ukraina'), loc='upper left',
                             shadow=True, title="Legenda", fancybox=True)
        create(fig1)
    if index == 1:
        for s in range(4):
            ax2.plot(data[s][0], data[s][1])
            ax2.set_title(u'Wielkość eksportu dóbr i usług', fontsize=15)
            leg = ax2.legend(('Czechy', 'Niemcy', 'Polska', 'Ukraina'), loc='upper left',
                             shadow=True, title="Legenda", fancybox=True)
        create(fig2)
    if index == 2:
        for s in range(4):
            ax3.plot(data[s][0], data[s][1])
            ax3.set_title(u'Gęstość zaludnienia', fontsize=15)
            leg = ax3.legend(('Czechy', 'Niemcy', 'Polska', 'Ukraina'), loc='upper left',
                             shadow=True, title="Legenda", fancybox=True)
        create(fig3)
    if index == 3:
        for s in range(4):
            ax4.plot(data[s][0], data[s][1])
            ax4.set_title(u'Ilość przyjeżdżających turystów', fontsize=15)
            leg = ax4.legend(('Czechy', 'Niemcy', 'Polska', 'Ukraina'), loc='upper left',
                             shadow=True, title="Legenda", fancybox=True)
        create(fig4)
    data_tmp = []
    data = [([], []), ([], []), ([], []), ([], [])]

# Zapisujemy wynik do pliku o nazwie "stats.html":
with open("stats.html", "w") as f:
    f.write(ET.tostring(root))