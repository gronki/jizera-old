
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask('JizeraApp')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db/jizera.db'

db = SQLAlchemy(app)


# location
class Location(db.Model):

    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)
    # name of the observing spot -- entered by the user or
    # taken from google geolocalization
    name = db.Column(db.String(200))
    # location and altitude
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    altitude = db.Column(db.Float)
    # optional place for code used for google synchronization -- not neccesary?
    googlecode = db.Column(db.String(45))

    def __init__(self, latitude, longitude, name=None):
        self.latitude = latitude
        self.longitude = longitude
        if name != None:
            self.name = name

    def __str__(self):
        return ( '%.5f' % self.longitude ) + ', ' + ( '%.5f' % self.latitude )



# table for registered observers
class Observer(db.Model):

    __tablename__ = 'observers'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)
    # observer info
    name = db.Column(db.String(45))
    lastname = db.Column(db.String(45))
    email = db.Column(db.String(120), unique=True)
    # OpenID
    openid_openid = db.Column(db.String(255), unique=True)
    openid_identity = db.Column(db.String(255))
    openid_server = db.Column(db.String(255))

    def __str__(self):
        return self.name + ' ' + self.lastname + ' (' + self.code + ')'



# class for observations (1 filled form = 1 observation)
class Observation(db.Model):

    __tablename__ = 'observations'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)
    # observer name
    name = db.Column(db.String(100))
    # date of begin and end
    obs_date_start = db.Column(db.DateTime)
    obs_date_end = db.Column(db.DateTime)
    # conditions: clouds, moon and milky way
    cond_clouds = db.Column(db.Integer)
    cond_moon = db.Column(db.Integer)
    cond_milkyway = db.Column(db.Integer)
    # relations
    location = db.Column(db.Integer, db.ForeignKey('locations.id'))
    observer = db.Column(db.Integer, db.ForeignKey('observers.id'))



# optional review that can be written for given location
class Review(db.Model):

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)
    # survey about the observation spot
    has_current = db.Column(db.Integer)
    has_sleeping = db.Column(db.Integer)
    has_horizon = db.Column(db.Integer)
    # comment where user can put additional notes
    comment = db.Column(db.String(400))
    # relations
    location = db.Column(db.Integer, db.ForeignKey('locations.id'))
    # observation = db.Column(db.Integer, db.ForeignKey('observations.id'))

# Following entries are various kinds of measurments

# entries for bortle method
class BortleData(db.Model):
    __tablename__ = 'bortle_data'
    id = db.Column(db.Integer, primary_key=True)
    # bortle degree of sky darkness
    bortle = db.Column(db.Integer)
    # comment from the observer
    comment = db.Column(db.String(400))
    # relations
    observation = db.Column(db.Integer, db.ForeignKey('observations.id'))


# entries for dslr measurments
class DSLRData(db.Model):
    __tablename__ = 'dslr_data'
    id = db.Column(db.Integer, primary_key=True)
    # info about camera
    info_camera = db.Column(db.String(200))
    info_lens = db.Column(db.String(200))
    # field number
    field_nr = db.Column(db.Integer)
    # data as copied from the spreadsheet
    data = db.Column(db.String(400))
    # result: DSLR magnitude of background glow
    dlsr_mag = db.Column(db.Float)
    # comment from the observer
    comment = db.Column(db.String(400))
    # relations
    observation = db.Column(db.Integer, db.ForeignKey('observations.id'))


# entries for meteor (limiting magniude) method
class MeteorData(db.Model):
    __tablename__ = 'meteor_data'
    id = db.Column(db.Integer, primary_key=True)
    # number of field
    field_nr = db.Column(db.Integer)
    # user measurement
    stars = db.Column(db.Integer)
    # result: limiting magnitude
    lim_mag = db.Column(db.Float)
    # comment from the observer
    comment = db.Column(db.String(400))
    # relations
    observation = db.Column(db.Integer, db.ForeignKey('observations.id'))


# SQM measurments
class SQMData(db.Model):
    __tablename__ = 'sqm_data'
    id = db.Column(db.Integer, primary_key=True)
    sqm_model = db.Column(db.String(45))
    sqm_serial = db.Column(db.String(45))
    # all values entered by the user in json/csv format
    data = db.Column(db.String(500))
    # results obtained for zenith and all directions
    sqm_mag = db.Column(db.Float)
    sqm_mag_n = db.Column(db.Float)
    sqm_mag_s = db.Column(db.Float)
    sqm_mag_w = db.Column(db.Float)
    sqm_mag_e = db.Column(db.Float)
    # comment from the observer
    comment = db.Column(db.String(400))
    # relations
    observation = db.Column(db.Integer, db.ForeignKey('observations.id'))


# Tube measurments
class TubeData(db.Model):
    __tablename__ = 'tube_data'
    id = db.Column(db.Integer, primary_key=True)
    # additional parameters of the tube
    tube_diam = db.Column(db.Float)
    tube_length = db.Column(db.Float)
    tube_type = db.Column(db.String(6))
    tube_glasses = db.Column(db.Integer)
    # results from tube pointings as csv string
    data = db.Column(db.String(500))
    # result: stars visible in the sky
    sky_stars = db.Column(db.Integer)
    # comment from the observer
    comment = db.Column(db.String(400))
    # relations
    observation = db.Column(db.Integer, db.ForeignKey('observations.id'))
