# Jizera - baza danych ciemnego nieba

**Jizera** to baza danych, która zbiera pomiary ciemności nieba
od obserwatorów w całej Polsce.

## Instalacja
Aplikacja jest napisana we frameworku **Flask**. W systemie operacyjnym
musi być zainstalowany **Python 3**, **virtualenv**, **lessc** oraz **cleancss**. W systemie Fedora 24 zależności te zainstalujemy poleceniem:
```
sudo dnf install -y nodejs-less nodejs-clean-css python3 python3-virtualenv
```
Tworzymy środowisko wirtualne w katalogu projektu i aktywujemy je
w sesji basha.
```
virtualenv-3.5 venv
source venv/bin/activate
```
Instalujemy wymagane paczki za pomocą menedżera **pip**.
```
pip install Flask Flask-SQLAlchemy Flask-OpenID
```
