# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template, request, session, g, \
    redirect, url_for, abort, flash
from datetime import datetime

# tworzymy instancje flaska
app = Flask('Jizera')

def journal(s):
    ds0 = datetime.utcnow().strftime('%y-%m-%d %H:%M:%S')
    ds = ''
    if not hasattr(g,'journal_last_datetime') or g.journal_last_datetime != ds0:
        ds = ds0
        g.journal_last_datetime = ds0

    buf = u'%18s -- %s' % (ds,s)
    print(buf)
    with open(os.path.join(app.root_path, 'data','journal.txt'), 'a') as f:
        f.write(buf.encode('utf-8') + '\n')

from jizera.db import *
from jizera.dummy_init import cli_dummy_init
from jizera.filters import *

@app.cli.command('is-debug')
def cli_is_debug():
    journal(u'Debug mode: %s' % ('ON' if app.debug else 'OFF'))

@app.route('/')
def index():
    cur = get_db().cursor()
    cur.execute("""SELECT
        observations.id AS observation_id,
        observations.created AS created,
        observations.date_start AS date_start,
        observers.id AS observer_id,
        observers.name AS observer_name,
        observers.lastname AS observer_lastname,
        locations.name AS location_name,
        locations.latitude AS latitude,
        locations.longitude AS longitude
        FROM observations
        JOIN observers ON (observers.id = observations.observer_id)
        JOIN locations ON (locations.id = observations.location_id)
        ORDER BY observations.created DESC
        LIMIT 5;
        """)
    recent = cur.fetchall()
    return render_template('index.html', recent=recent)

if __name__ == '__main__':
    app.run()
