# Jizera - baza danych ciemnego nieba

**Jizera** to baza danych, która zbiera pomiary ciemności nieba
od obserwatorów w całej Polsce.

## Wymagania

Aplikacja jest napisana we frameworku **Flask**, z użyciem **SQLAlchemy** oraz **SQLite** do obsługi bazy danych (w wersji testowej). Front-end jest oparty na frameworku **Foundation**, zaś arkusze stylów są generowane ze skryptów **scss**.

W systemie operacyjnym
musi być zainstalowany **Python 2.7** i **virtualenv**. W systemie Fedora 24 zależności te zainstalujemy poleceniem:
```
sudo yum install -y git python python-pip python-virtualenv nodejs npm
```

## Instalacja

Pobieramy katalog projektu na nasz dysk:

```
git clone https://github.com/gronki/jizera.git
```

Tworzymy środowisko wirtualne w katalogu projektu i aktywujemy je
w sesji basha.
```
virtualenv venv
source venv/bin/activate
```
Instalujemy wymagane paczki za pomocą menedżera **pip**.
```
pip install Flask Flask-Login Flask-Mail Flask-WTF Flask-SQLAlchemy SQLAlchemy-Migrate Flask-OpenID Flask-Babel
```

### Aby zmodyfikować szablony

Szablon graficzny został napisany w środowisku Foundation. Aby zmienić wygląd strony,
należy przekompilować go. Upewniamy się, że mamy zainstalowane Foundation w systemie.
```
sudo npm install -g foundation-cli
```
Następnie w katalogu **jizera-ui** kompilujemy szablon poleceniem
```
foundation build
```

## Uruchamianie

W budowie.
