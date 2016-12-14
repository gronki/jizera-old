# -*- coding: utf-8 -*-

from jizera import app, g, journal
import os
import sqlite3
from shutil import copy2
from datetime import datetime

def get_db_filename():
    return os.path.join(app.root_path, 'data','jizera.db')

def adapt_datetime(ts):
    return ts.strftime(r'%Y-%m-%d %H:%M:%S')
def convert_datetime(s):
    return datetime.strptime(s,r'%Y-%m-%d %H:%M:%S')

def get_db():
    if not hasattr(g,'db'):
        g.db_filename = get_db_filename()
        sqlite3.register_adapter(datetime, adapt_datetime)
        sqlite3.register_converter("datetime", convert_datetime)
        g.db = sqlite3.connect(g.db_filename, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

def get_db_cursor():
    return get_db().cursor()

@app.cli.command('drop')
def cli_drop_db():
    db = get_db()
    fn = get_db_filename()
    if os.path.exists(fn):
        journal(u'Znaleziono bazę w lokalizacji: %s' % fn)
        fn_copy = os.path.join(os.path.dirname(fn),
            'jizera.%s.db' % datetime.utcnow().strftime('%y%m%d.%H%M%S'))
        copy2(fn,fn_copy)
        journal(u'Wykonano kopię: %s' % fn_copy)

    with app.open_resource('sql/drop.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('init')
def cli_init_db():
    db = get_db()
    with app.open_resource('sql/schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
        db.commit()
        journal(u"Zainicjalizowano pustą bazę.")

@app.teardown_appcontext
def close_db(e):
    if hasattr(g,'db'):
        g.db.close()
        del g.db
