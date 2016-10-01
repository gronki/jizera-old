from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# tworzymy instancje flaska
app = Flask('Jizera')

from jizera.database import *
