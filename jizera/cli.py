# -*- coding: utf-8 -*-

from jizera import app, get_db
from jizera.db import get_db_filename
from jizera.dummy_init import cli_dummy_init
from shutil import copy2
import os
from datetime import datetime

@app.cli.command('drop')
def cli_drop_db():
    db = get_db()
    fn = get_db_filename()
    if os.path.exists(fn):
        print(u'Znaleziono bazę w lokalizacji: %s' % fn)
        fn_copy = os.path.join(os.path.dirname(fn),
            'jizera.%s.db' % datetime.utcnow().strftime('%y%m%d.%H%M%S'))
        copy2(fn,fn_copy)
        print(u'Wykonano kopię: %s' % fn_copy)

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
