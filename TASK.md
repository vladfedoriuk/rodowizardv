RODO Wizard
=======

Wymagania
---------

System do zbierania danych dla RODO przed szkoleniami online.

W najprostszej wersji, po zalogowaniu się do django admina tworzymy obiekt, w którym definiujemy nazwę szkolenia, czas
rozpoczęcia i zakończenia oraz adres e-mail, na który będą wysłane informacje po uzupełnieniu formularzy. Po zapisaniu
obiektu generuje się unikatowy link - po wejściu w ten link wyświetla się wizard z 4 krokami (screeny w folderze
examples). Osoba, która otrzyma taki link, uzupełnia wszystkie dane, a po kliknięciu Wyślij system wysyła te dane na adres
e-mail podany przy tworzeniu obiektu ze szkoleniem, w bazie oznaczamy cały proces jako ukończony, a użytkownikowi wysyłamy na adres
e-mail unikatowy link do potwierdzenia autentyczności e-maila. Po kliknięciu w taki link, oznaczamy ten adres e-mail
jako potwierdzony.

Do zaprojektowania model do generowania linku dla szkolenia i do trzymania danych osobowych na podstawie screenów.


W wersji 1.0 frontend w oparciu o templatki django i django forms.


Jako bonus - wersji 2.0 (tzw zadanie z gwiazdką *) zachęcamy do przygotowania API w DRF / flex fields i frontendu w react.js.


Na co zwracamy uwagę:
---------------------

* łatwość instalacji i uruchomienia (opis w README.md)
* testy
* caly kod i dokumentacja powinne byc w jezyku angielskim
* iteratywne podejście odzwierciedlające się w merge requestach (każdy merge request powinien być przypisany do
  @lchojnacki lub @citos)

Wymagania techniczne:
---------------------

* python3
* Django 3.x
* Docker
* django admin - jazzmin
