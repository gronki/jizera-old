# -*- coding: utf-8 -*-

from flask import render_template, abort, request, g
from jizera import app, get_db_cursor

@app.route('/')
def index():
    cur = get_db_cursor()
    cur.execute("""SELECT
        observations.id AS observation_id,
        observations.created AS created,
        observations.date_start AS date_start,
        observers.id AS observer_id,
        (observers.name || " " || observers.lastname) AS observer_name,
        locations.name AS location_name,
        locations.latitude AS latitude,
        locations.longitude AS longitude,
        printf("@%.5f,%.5f", locations.latitude, locations.longitude) as latlng
        FROM observations
        JOIN observers ON (observers.id = observations.observer_id)
        JOIN locations ON (locations.id = observations.location_id)
        ORDER BY observations.created DESC
        LIMIT 5;
        """)
    recent = cur.fetchall()
    return render_template('index.html', recent=recent)

@app.route('/observation/<eid>')
def show_observation(eid):
    observation_id = int(eid)
    cur = get_db_cursor()
    cur.execute("""SELECT
        observations.id AS observation_id,
        observations.created AS created,
        observations.date_start AS date_start,
        observers.id AS observer_id,
        (observers.name || " " || observers.lastname) AS observer_name,
        locations.name AS location_name,
        locations.latitude AS latitude,
        locations.longitude AS longitude,
        printf("@%.5f,%.5f", locations.latitude, locations.longitude) as latlng
        FROM observations
        JOIN observers ON (observers.id = observations.observer_id)
        JOIN locations ON (locations.id = observations.location_id)
        WHERE observations.id = ?;
        """, (observation_id,))
    obs_info = cur.fetchone()
    if obs_info == None:
        abort(404)
    obs_extras = {}

    for dt in ['sqm','tube','meteor','dslr','bortle']:
        cur.execute("""SELECT * FROM %s_data
            WHERE %s_data.observation_id = ?;""" % (dt,dt), (observation_id,))
        obs_extras[dt] = cur.fetchall()

    return render_template('observation_show.html', data=obs_info, extras=obs_extras)



@app.route('/new', methods=['POST','GET'])
def new_observation():
    from jizera.validators import *
    validation = {}
    if request.method == 'POST':
        validate(validation,['email','required'],'email')
        validate(validation,'date','date')
        validate(validation,'time','time_start')
        validate(validation,'time','time_end')
    return render_template("add.html",validation=validation)

@app.route('/browse')
def browser():
    return "This is not yet implemented."

@app.route('/articles/<name>')
def show_article(name):
    return "This is not yet implemented."
