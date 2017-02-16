# -*- coding: utf-8 -*-

from jizera import app, g, db_filename
import os
import sqlite3
from datetime import datetime

def get_db():
    def adapt_datetime(ts):
        return ts.strftime(r'%Y-%m-%d %H:%M:%S')
    def convert_datetime(s):
        return datetime.strptime(s,r'%Y-%m-%d %H:%M:%S')
    if not hasattr(g,'db'):
        sqlite3.register_adapter(datetime, adapt_datetime)
        sqlite3.register_converter("datetime", convert_datetime)
        g.db = sqlite3.connect(db_filename, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

def get_db_cursor():
    return get_db().cursor()

@app.teardown_appcontext
def close_db(e):
    if hasattr(g,'db'):
        g.db.close()
        del g.db
