# -*- coding: utf-8 -*-

import os
from flask import Flask, g
from datetime import datetime

# tworzymy instancje flaska
app = Flask(__name__)

googlemaps_api_key = 'AIzaSyBdhoSL2YRJZTYdaPKfSTrTkiDsgAiHbts'
db_filename = '/tmp/jizera.db'
app.secret_key = 'J4893a8h2KbQKIjn278U80Xiv3443XZJ'

print 'root path: {root}'.format(root=app.root_path)

from jizera.db import get_db, get_db_cursor, close_db
import jizera.filters
import jizera.cli
import jizera.views

if __name__ == '__main__':
    app.run()
