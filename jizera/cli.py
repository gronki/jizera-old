# -*- coding: utf-8 -*-

from jizera import app, get_db, db_filename
from jizera.dummy_init import cli_dummy_init
from shutil import copy2
import os.path
from datetime import datetime

@app.cli.command('drop')
def cli_drop_db():
    db = get_db()
    if os.path.exists(db_filename):
        print(u'Znaleziono bazę w lokalizacji: %s' % db_filename)
        db_filename_copy = os.path.join(os.path.dirname(db_filename),
            'jizera.%s.db' % datetime.utcnow().strftime('%y%m%d.%H%M%S'))
        copy2(db_filename,db_filename_copy)
        print(u'Wykonano kopię: %s' % db_filename_copy)

    with app.open_resource('sql/drop.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('init')
def cli_init_db():
    db = get_db()
    with app.open_resource('sql/schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
        db.commit()
        print(u"Zainicjalizowano pustą bazę.")
