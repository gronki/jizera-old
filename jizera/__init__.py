from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask('Jizera')
testdb_location = '/tmp/jizera-testing.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + testdb_location
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import *
