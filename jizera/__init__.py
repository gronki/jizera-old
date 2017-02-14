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

app.secret_key = r't.8(g0(XQgc|*Z85f-D;u0^Q[;h-VQvy`4x.r_KNCnY7M{kGiU>1@ht]EW%dGQg'

if __name__ == '__main__':
    app.run(debug=True)
