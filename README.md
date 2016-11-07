# Jizera - baza danych ciemnego nieba

**Jizera** to baza danych, która zbiera pomiary ciemności nieba
od obserwatorów w całej Polsce.

## Wymagania

Aplikacja jest napisana we frameworku **Flask**, oraz **SQLite** do obsługi bazy danych (w wersji testowej). Front-end jest oparty na frameworku **Foundation**, zaś arkusze stylów są generowane ze skryptów **scss**.

W systemie operacyjnym
musi być zainstalowany **Python 2.7** i **virtualenv**. W systemie Fedora/CentOS/RHEL zależności te zainstalujemy poleceniem:
```
sudo yum install -y git python python-pip python-virtualenv
```

## Instalacja

Pobieramy katalog projektu na nasz dysk:

```
git clone https://github.com/gronki/jizera.git
```

Tworzymy środowisko wirtualne w katalogu projektu i aktywujemy je
w sesji basha.
```
cd jizera
virtualenv venv
. venv/bin/activate
```
Jeżeli wszystko przebiegnie poprawnie, adnotacja o tym, ze jesteśmy w środowisku wirtualnym zostanie umieszczone na lewo od znaku zachęty.
```
(venv) [uzytkownik@maszyna jizera]$
```
Instalujemy wymagane paczki za pomocą menedżera **pip**.
```
pip install Flask sqlite3
```
## Uruchomienie
Ustawiamy najpierw zmienne środowiskowe:
```
export FLASK_APP=jizera
export FLASK_DEBUG=1
```

### Inicjalizacja pustej bazy i usunięcie bazy
Przed pierwszym uruchomieniem należy utworzyć strukturę tabel bazy danych. W tym celu używamy polecenia
```
python -m flask init
```
Po eksperymentach możemy wyczyścić z powrotem bazę poleceniem
```
python -m flask drop
```
Ponieważ testowanie pustej bazy jest nudne, jest możliwość wygenerowania losowych danych za pomocą polecenia
```
python -m flask dummy-init
```

### Uruchomienie serwera
Uruchamiamy serwer testowy bazy poleceniem:
```
python -m flask run
```
Powinniśmy w rezultacie dostać komunikat zawierający adres w przeglądarce pod który należy wejść by przeglądać bazę (w tym przypadku ``http://127.0.0.1:5000/``).
```
* Serving Flask app "jizera"
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
Na ekranie mogą się ukazywać różne komunikaty. Zostają one równocześnie zapisane w pliku ``data/journal.txt``.

## Narzędzia programistyczne

### Modyfikacja szablonów

Szablon graficzny został napisany w środowisku Foundation. Aby zmienić wygląd strony,
należy przekompilować go. Upewniamy się, że mamy zainstalowane Foundation w systemie.
```
sudo yum install -y nodejs npm
sudo npm install -g foundation-cli
```
Następnie w katalogu **jizera-ui** kompilujemy szablon poleceniem
```
foundation build
```

### Przeglądanie bazy SQLite

W celu przeglądania struktury bazy danych, można użyć narzędzia **sqlitebrowser**.
```
sudo yum install -y sqlitebrowser
sqlitebrowser /tmp/jizera-testing.db &
```
