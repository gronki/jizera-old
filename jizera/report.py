# -*- coding: utf-8 -*-

from flask import request, g
from flask import render_template, abort, redirect, url_for
from flask import flash
from jizera import app, get_db, get_db_cursor
from datetime import datetime, timedelta

@app.route('/report', methods=['POST','GET'])
def new_observation():
    from jizera.validators import *
    if request.method == 'POST':

        # wypisujemy formularz (debug)
        print "{k:20} {v:20}".format(k='NAME',v='VALUE')
        if app.debug:
            for k,v in request.form.items():
                print "{k:20} {v:20}".format(k=k,v=v)

        validation = {}

        # sprawdzamy obowiązkowe pola
        validate(validation,'email','email')
        validate(validation,'date','date')
        validate(validation,'time','time_start')
        validate(validation,'time','time_end')
        validate(validation,'float','latitude')
        validate(validation,'float','longitude')

        if 'check_tube_data' in request.form:
            # jeżeli wypełniono pomiar tubą, sprawdzamy pola
            validate(validation,'float','tube_length')
            validate(validation,'float','tube_diam')
            validate(validation,'int-list','tube_data')

        if len(validation) != 0:
            return render_template("report.html",validation=validation)
        # brak błędów walidacji
        db = get_db()
        cur = db.cursor()
        now = datetime.now()

        # sprawdzamy, czy jest taki obserwator
        rows = cur.execute("SELECT id FROM observers \
            WHERE (observers.email = ?);",
            (request.form['email'],)).fetchone()
        if app.debug:
            print "Obserwator o emailu: {email}".format(email=request.form['email'])
        if rows:
            # obserwator istnieje w bazie
            observer_id = rows['id']
            if app.debug:
                print "\tobserwator w bazie, id: {oid}".format(oid=observer_id)
        else:
            # takiego obserwatora nie ma w bazie
            # dodajemy obserwatora
            cur.execute("""INSERT INTO observers (name,email,created,modified,anonymous) VALUES (?,?,?,?,?);""",
                (request.form['fullname'],
                request.form['email'],
                now, now, 1))
            observer_id = cur.lastrowid
            if app.debug:
                print "\tdodano obserwatora, id={oid}".format(oid=observer_id)

        # dodajemy lokalizację
        cur.execute("INSERT INTO locations \
            (created, modified, name, latitude, longitude) \
            VALUES (?,?,?,?,?);", (now, now, request.form['location_name'],
                request.form['latitude'], request.form['longitude']))
        location_id = cur.lastrowid

        # dodajemy obserwację
        # parsujemy datę i godzinę
        date_base = datetime.strptime(request.form['date'], r'%Y-%m-%d')
        time_start = datetime.strptime(request.form['time_start'], r'%H:%M')
        time_end = datetime.strptime(request.form['time_end'], r'%H:%M')

        # skladamy date i dwie godziny w dwie daty
        date_start = datetime.combine(date_base.date(),
                time_start.time())
        tdelta = timedelta(0)
        if time_end.hour < 12:
            # jezeli to godzina poranna, dodajemy 1 dzien do drugiej daty
            tdelta = timedelta(days=1)
        date_end = datetime.combine((date_base+tdelta).date(),
                time_end.time())

        if app.debug:
            print "\tpoczątek: {start}\n\tkoniec: {end}".format(
                start = date_start,
                end = date_end,
            )

        cur.execute("""INSERT INTO observations
            (created, modified, date_start, date_end,
            cond_clouds_octants, cond_milkyway,
            location_id, observer_id) VALUES (?,?,?,?,?,?,?,?);""",
            (now, now, date_start, date_end,
            request.form['cond_clouds_octants'],
            request.form['cond_milkyway'],
            location_id, observer_id))
        observation_id = cur.lastrowid

        # data_types to lista rodzajów wykonanych obserwacji
        data_types = []

        # dane z Bortla
        if request.form['bortle']:
            if app.debug:
                print "\tstopni Bortla: {b}".format(b=request.form['bortle'])
            cur.execute("INSERT INTO bortle_data \
                (created,modified,degrees,observation_id) \
                VALUES (?,?,?,?);",
                (now, now, request.form['bortle'], observation_id))
            data_types.append('bortle')


        # jeżeli są dane z tuby, dodajemy do bazy
        if 'check_tube_data' in request.form:

            num_stars = 0.0
            arr = request.form['tube_data'].split()
            for stars in arr:
                num_stars = num_stars + int(stars) * 1.0 / len(arr)

            if app.debug:
                print "\tsrednia liczba gwiazd na niebie: {num_stars:.2}".format(num_stars=num_stars)

            cur.execute("INSERT INTO tube_data \
                (created, modified, \
                tube_diam, tube_length, tube_type, \
                tube_glasses, data, num_stars, observation_id)\
                VALUES (?,?,?,?,?,?,?,?,?);",
                (now, now,
                request.form['tube_diam'],
                request.form['tube_length'],
                request.form['tube_type'],
                1 if 'tube_glasses' in request.form else 0,
                request.form['tube_data'],
                round(num_stars),
                observation_id,
                )
            )

            data_types.append('tube')

        if len(data_types) == 0:
            db.rollback()
            flash(u"Musisz wysłać jakiś rodzaj pomiaru!", "error")
            return render_template("report.html")

        # koniec
        db.commit()
        flash(u'Obserwacja dodana!', 'success')
        return redirect(url_for('index'))

    return render_template("report.html")
