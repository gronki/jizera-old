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

@app.cli.command('is-debug')
def cli_is_debug():
    journal(u'Debug mode: %s' % ('ON' if app.debug else 'OFF'))

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
