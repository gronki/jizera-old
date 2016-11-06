from flask import Flask, render_template

# tworzymy instancje flaska
app = Flask('Jizera')

from jizera.database import *
from jizera.models import *

@app.route('/')
def index():
    init_db()
    data = dbsession.query(Observation.date_start,Observer.name,Observer.lastname,
        Location.name, Location.latitude, Location.longitude, MeteorData.magnitude,
        DSLRData.magnitude, SQMData.magnitude_z) \
        .join(Observer,Location,MeteorData,DSLRData,SQMData).all()
    destroy_db()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run()
