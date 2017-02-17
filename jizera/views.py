# -*- coding: utf-8 -*-

from flask import request, g
from flask import render_template, abort, redirect, url_for
from flask import flash
from jizera import app, get_db, get_db_cursor

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

    cur.execute("""SELECT observers.id AS id,
        (observers.name || " " || observers.lastname) AS name,
        observers.created as joined
        FROM observers ORDER BY observers.created DESC LIMIT 5;""")
    new_observers = cur.fetchall()

    return render_template('index.html',
        recent=recent,
        new_observers = new_observers)

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
        print "{k:20} {v:20}".format(k='NAME',v='VALUE')
        if app.debug:
            for k,v in request.form.items():
                print "{k:20} {v:20}".format(k=k,v=v)
        validate(validation,['email','required'],'email')
        validate(validation,'date','date')
        validate(validation,'time','time_start')
        validate(validation,'time','time_end')
        validate(validation,'float','latitude')
        validate(validation,'float','longitude')
        if 'check_tube_data' in request.form:
            validate(validation,['float','required'],'tube_length')
            validate(validation,['float','required'],'tube_diam')
            validate(validation,['int_list','required'],'tube_data')
        if len(validation) == 0:
            db = get_db()
            cur = db.cursor()
            now = datetime.now()
            cur.execute("""INSERT INTO observers (name,email,created,modified) VALUES (?,?,?,?);""",
                (request.form['fullname'],
                request.form['email'],
                now, now))
            print 'cur.lastrowid = %d' % cur.lastrowid
            db.commit()
            flash(u'Obserwacja dodana!', 'success')
            return redirect(url_for('index'))
    return render_template("add.html",validation=validation)

@app.route('/browse')
def browser():
    return "This is not yet implemented."

@app.route('/articles/<name>')
def show_article(name):
    return "This is not yet implemented."
