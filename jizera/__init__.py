from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# tworzymy instancje flaska
app = Flask('Jizera')

# pare ustawien
testdb_location = '/tmp/jizera-testing.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + testdb_location
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# tworzymy obiekt SQLAlchemy
db = SQLAlchemy(app)

from models import *
