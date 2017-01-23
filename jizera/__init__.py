# -*- coding: utf-8 -*-

import os
from flask import Flask, g
from datetime import datetime

# tworzymy instancje flaska
app = Flask('Jizera')

googlemaps_api_key = 'AIzaSyBdhoSL2YRJZTYdaPKfSTrTkiDsgAiHbts'

from jizera.db import get_db, get_db_cursor, close_db
import jizera.filters
import jizera.cli
import jizera.views

if __name__ == '__main__':
    app.run(debug=True)
