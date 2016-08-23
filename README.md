# Jizera - baza danych ciemnego nieba

**Jizera** to baza danych, która zbiera pomiary ciemności nieba
od obserwatorów w całej Polsce.

## Instalacja
Aplikacja jest napisana we frameworku **Flask**. W systemie operacyjnym
musi być zainstalowany **Python 3**, **virtualenv**, **lessc** oraz **cleancss**. Środowisko wirtualne tworzymy poleceniem
```
virtualenv-3.5 venv
```
Następnie wchodzimy do środowiska poleceniem
```
source venv/bin/activate
```
Instalujemy wymagane paczki za pomocą menedżera **pip**.
```
pip install Flask Flask-SQLAlchemy Flask-OpenID
```
