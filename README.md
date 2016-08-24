# Jizera - baza danych ciemnego nieba

**Jizera** to baza danych, która zbiera pomiary ciemności nieba
od obserwatorów w całej Polsce.

## Wymagania

Aplikacja jest napisana we frameworku **Flask**, z użyciem **SQLAlchemy** oraz **SQLite** do obsługi bazy danych (w wersji testowej). Front-end jest oparty na frameworku **Bootstrap**, zaś arkusze stylów są generowane ze skryptów **less**.

W systemie operacyjnym
musi być zainstalowany **Python 2.7**, **virtualenv**, **lessc** oraz **cleancss**. W systemie Fedora 24 zależności te zainstalujemy poleceniem:
```
sudo yum install -y make nodejs-less nodejs-clean-css python python-virtualenv
```

## Instalacja

Tworzymy środowisko wirtualne w katalogu projektu i aktywujemy je
w sesji basha.
```
virtualenv venv
source venv/bin/activate
```
Instalujemy wymagane paczki za pomocą menedżera **pip**.
```
pip install Flask Flask-Login Flask-Mail Flask-SQLAlchemy SQLAlchemy-Migrate Flask-OpenID Flask-Babel
```
