# -*- coding: utf-8 -*-

from flask import render_template
from jizera import app
from jizera.db import get_db

@app.route('/browse')
def browser():
    db = get_db()
    return render_template("browse.html")
