# -*- coding: utf8 -*-
import urllib2
import json
from PyRTF import *

# Usuwanie znaczników HTML:
from pyparsing import anyOpenTag, anyCloseTag
from xml.sax.saxutils import unescape as unescape
unescape_xml_entities = lambda s: unescape(s, {"&apos;": "'", "&quot;": '"', "&nbsp;": " "})

stripper = (anyOpenTag | anyCloseTag).suppress()

#: Pobieramy dane ze strony:
url = urllib2.urlopen('http://polska.googleblog.com/feeds/posts/default?alt=json')
#: Formatujemy pobrane dane:
data = json.load(url)


def read_list(tab, section):
    """Funkcja rekurencyjna przechodząca po kolejnych elementach listy "tab" przekazanej w argumencie.

    Jeśli dany element wspomnianej listy również jest listą, to ponownie wywołujemy ową funkcję z argumentem
    będącym badanym właśnie elementem. Jeśli natomiast dany element jest słownikiem oraz jest różny od
    "content", "title" i "published", to wywołujemy funkcję "read_json" z argumentem będącym badanym elementem.
    Parametr "section" potrzebny jest w momencie wywoływania funkcji "read_json".
    """
    for i in range(len(tab)):
        if type(tab[i]) == list:
            read_list(tab[i], section)
        elif type(tab[i]) == dict and (tab[i] != 'content' and tab[i] != 'title' and
                                       tab[i] != 'published'):
            read_json(tab[i], section)


def read_json(tab, section):
    """Funkcja rekurencyjna przechodząca po kolejnych kluczach słownika "tab" przekazanego w argumencie.

    Jeśli element odpowiadający danemu kluczowi wspomnianego słownika również jest słownikiem
    oraz jest różny od "content", "title" i "published", to ponownie wywołujemy ową funkcję z argumentem
    będącym badanym elementem. Jeśli natomiast dany element jest listą, to wywołujemy
    funkcję "read_list" z argumentem będącym badanym elementem.
    Na koniec funkcja tworzy nowy paragraf i zapisuje do niego żądaną zawartość, tj. "content", "title"
    lub "published", dokonując jednocześnie odpowiedniego formatowania zapisywanego tekstu. Nowo powstały
    paragraf zapisujemy do sekcji "section", którą otrzymujemy w argumencie.
    """
    save = []  # Pomocnicza lista - chwilowo przechowujemy "content" oraz "title" (tytuł i treść artykułu),
    # aby kontrolować kolejność zapisywania danych do paragrafów.
    counter = 0  # Zmienna pomocnicza.
    for value in tab.keys():
        if type(tab[value]) == dict and (value != 'content' and value != 'title' and
                                         value != 'published'):
            read_json(tab[value], section)
        elif type(tab[value]) == list:
            read_list(tab[value], section)
        elif type(tab[value]) == dict and (value == 'content' or value == 'title'
                                           or value == 'published'):
            for index in tab[value].keys():
                # Wstawiamy tytuł bloga do paragrafu i dokonujemy formatowania tekstu:
                if tab[value][index].encode('utf-8') == 'The History of Python':
                    p = Paragraph()
                    p.append('\qc')
                    p.append(TEXT(tab[value][index].encode('utf-8'), bold=True, size=30))
                    section.append(p)
                # Wstawiamy datę publikacji artykułu do paragrafu i dokonujemy formatowania tekst:
                if index == '$t' and value == 'published':
                    p = Paragraph()
                    p.append(TEXT(tab[value][index].encode('utf-8'), bold=True, italic=True))
                    section.append(p)
                    counter += 1
                if index == '$t' and value == 'content':
                    save.append(tab[value][index])
                if index == '$t' and value == 'title':
                    save.append(tab[value][index])
            # Wstawiamy treść artykułu oraz tytuł i dokonujemy formatowania tekst:
            if counter == 1:
                p = Paragraph()
                p.append('\qc')
                tmp1 = unescape_xml_entities(stripper.transformString(save[0]))
                p.append(TEXT(tmp1.encode('utf-8'), bold=True))
                section.append(p)
                p = Paragraph()
                tmp2 = unescape_xml_entities(stripper.transformString(save[1]))
                p.append(tmp2.encode('utf-8'))
                section.append(p)
                save = []
                counter = 0


def create_doc():
    """Funkcja odpowiadająca za utworzenie dokumentu, sekcji oraz wywołanie metody "tworzącej" zawartość żądanego pliku."""
    doc = Document()
    section = Section()
    doc.Sections.append(section)
    read_json(data, section)
    return doc


if __name__ == '__main__':
    """Główna funkcja programu."""
    DR = Renderer()
    doc1 = create_doc()
    with open('articles.rtf', 'w') as my_file:
        DR.Write(doc1, my_file)
