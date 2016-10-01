
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta

from jizera import app, db


# table for registered observers
class Observer(db.Model):

    __tablename__ = 'observers'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)
    # observer info
    name = db.Column(db.Unicode(60))
    lastname = db.Column(db.Unicode(60))
    email = db.Column(db.Unicode(255), unique=True)
    # OpenID
    openid_openid = db.Column(db.String(255), unique=True)
    openid_identity = db.Column(db.String(255))
    openid_server = db.Column(db.String(255))

    # relationships
    observations = db.relationship('Observation', back_populates='observer')
    reviews = db.relationship('Review', back_populates='observer')

    def __init__(self,name,lastname,email):
        self.created = datetime.now()
        self.modified = self.created
        self.name = name
        self.lastname = lastname
        self.email = email

    def __unicode__(self):
        return u'%s %s <%s>' % (self.name, self.lastname, self.email)
        # return '%s' % self.name

    def __str__(self):
        return self.__unicode__().encode('utf-8')


# location
class Location(db.Model):

    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)
    # name of the observing spot -- entered by the user or
    # taken from google geolocalization
    name = db.Column(db.Unicode(200))
    # location and altitude
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    altitude = db.Column(db.Float)
    # optional place for code used for google synchronization -- not neccesary?
    googlecode = db.Column(db.String(45))
    # relationships
    reviews = db.relationship('Review', back_populates='location')
    observations = db.relationship('Observation', back_populates='location')

    def __init__(self, latitude, longitude, name=None):
        self.latitude = latitude
        self.longitude = longitude
        if name != None:
            self.name = name

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def __unicode__(self):
        nswe = u'%.4f %s, %.4f %s' % (\
            abs(self.latitude), \
            'N' if self.latitude >= 0 else 'S', \
            abs(self.longitude),  \
            'E' if self.longitude >= 0 else 'W'  )
        if self.name != None:
            return u'%s (%s)' % ( self.name, nswe )
        return  nswe


# optional review that can be written for given location
class Review(db.Model):

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)
    # survey about the observation spot
    has_current = db.Column(db.Boolean)
    has_sleeping = db.Column(db.Boolean)
    has_horizon = db.Column(db.Boolean)
    # comment where user can put additional notes
    comment = db.Column(db.Unicode)
    # relations
    location = db.relationship('Location', back_populates='reviews')
    observer = db.relationship('Observer', back_populates='reviews')
    # foreign keys
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    observer_id = db.Column(db.Integer, db.ForeignKey('observers.id'))


    def __init__(self, location, observer, comment):
        self.location = location
        self.observer = observer
        self.comment = comment

    def __unicode__(self):
        return u'%s commented on location %s: %s' % (self.observer, self.location, self.comment)

    def __str__(self):
        return self.__unicode__().encode('utf-8')


# class for observations (1 filled form = 1 observation)
class Observation(db.Model):

    __tablename__ = 'observations'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)
    # date of begin and end
    date_start = db.Column(db.DateTime)
    date_end = db.Column(db.DateTime)
    # conditions: clouds, moon and milky way
    cond_clouds = db.Column(db.Boolean)
    cond_moon = db.Column(db.Boolean)
    cond_milkyway = db.Column(db.Boolean)
    # relations
    location = db.relationship('Location', back_populates='observations')
    observer = db.relationship('Observer', back_populates='observations')
    # typy pomiarow
    bortle_data = db.relationship('BortleData', back_populates='observation')
    dslr_data = db.relationship('DSLRData', back_populates='observation')
    sqm_data = db.relationship('SQMData', back_populates='observation')
    meteor_data = db.relationship('MeteorData', back_populates='observation')
    tube_data = db.relationship('TubeData', back_populates='observation')
    # foreign keys
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    observer_id = db.Column(db.Integer, db.ForeignKey('observers.id'))

    def __init__(self, location, observer, date_start=None, date_end=None):

        self.created = datetime.now()
        self.modified = self.created

        self.location = location
        self.observer = observer

        if date_start != None:
            self.date_start = date_start
        else:
            self.date_start = (datetime.now() + timedelta(days=-1)) \
                .replace(hour=22,minute=0,second=0,microsecond=0)

        if date_end != None:
            self.date_end = date_end
        else:
            self.date_end = self.date_start + timedelta(hours=1)


    def __unicode__(self):
        return u'observation performed on %s by %s in location %s'   \
            % (self.date_start,self.observer,self.location)

    def __str__(self):
        return self.__unicode__().encode('utf-8')


# Following entries are various kinds of measurments

# entries for bortle method
class BortleData(db.Model):
    __tablename__ = 'bortle_data'
    id = db.Column(db.Integer, primary_key=True)
    # bortle degree of sky darkness
    bortle = db.Column(db.Integer)
    # comment from the observer
    comment = db.Column(db.Unicode)
    # relations
    observation = db.relationship('Observation', back_populates='bortle_data')
    # foreign keys
    observation_id = db.Column(db.Integer, db.ForeignKey('observations.id'))

    def __init__(self, observation, bortle):
        self.observation = observation
        self.bortle = bortle

    def __unicode__(self):
        return u'%d in Bortle scale' % self.bortle

    def __str__(self):
        return self.__unicode__().encode('utf-8')


# entries for dslr measurments
class DSLRData(db.Model):
    __tablename__ = 'dslr_data'
    id = db.Column(db.Integer, primary_key=True)
    # info about camera
    info_camera = db.Column(db.Unicode(200))
    info_lens = db.Column(db.Unicode(200))
    # field number
    field_nr = db.Column(db.Integer)
    # data as copied from the spreadsheet
    data = db.Column(db.String(400))
    # result: DSLR magnitude of background glow
    dlsr_mag = db.Column(db.Float)
    # comment from the observer
    comment = db.Column(db.Unicode)
    # relations
    observation = db.relationship('Observation', back_populates='dslr_data')
    # foreign keys
    observation_id = db.Column(db.Integer, db.ForeignKey('observations.id'))

    def __init__(self, observation, field_nr, dslr_mag):
        self.observation = observation
        self.field_nr = field_nr
        self.dslr_mag = dslr_mag

    def __unicode__(self):
        return u'DSLR observation in field %d with result %0.2f' \
            % ( self.field_nr, self.dslr_mag )

    def __str__(self):
        return self.__unicode__().encode('utf-8')

def yfun(x1,y1,x2,y2,x):
    return float(x - x1) * (y2-y1)/float(x2-x1) + y1

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
    comment = db.Column(db.Unicode)
    # relations
    observation = db.relationship('Observation', back_populates='meteor_data')
    # foreign keys
    observation_id = db.Column(db.Integer, db.ForeignKey('observations.id'))

    def __init__(self, observation, field_nr, stars):
        self.observation = observation
        self.field_nr = field_nr
        self.stars = stars
        self.lim_mag = yfun(10,3.5,60,7.5,stars)

    def __unicode__(self):
        return u'%d stars in field %d which yields limiting magnitude %0.2f' \
            % ( self.stars, self.field_nr, self.lim_mag )

    def __str__(self):
        return self.__unicode__().encode('utf-8')


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
    comment = db.Column(db.Unicode)
    # relations
    observation = db.relationship('Observation', back_populates='sqm_data')
    # foreign keys
    observation_id = db.Column(db.Integer, db.ForeignKey('observations.id'))

    def __init__(self, observation, sqm_mag_tuple):
        ( self.sqm_mag, self.sqm_mag_n, self.sqm_mag_e, self.sqm_mag_s, \
            self.sqm_mag_w ) = sqm_mag_tuple
        self.observation = observation

    def __unicode__(self):
        return u'SQM results: zenith %0.2f, N %0.2f, E %0.2f, S %0.2f, W %0.2f' \
            % ( self.sqm_mag, self.sqm_mag_n, self.sqm_mag_e, self.sqm_mag_s, \
                self.sqm_mag_w )

    def __str__(self):
        return self.__unicode__().encode('utf-8')


# Tube measurments
class TubeData(db.Model):
    __tablename__ = 'tube_data'
    id = db.Column(db.Integer, primary_key=True)
    # additional parameters of the tube
    tube_diam = db.Column(db.Float)
    tube_length = db.Column(db.Float)
    tube_type = db.Column(db.String(6))
    tube_glasses = db.Column(db.Boolean)
    # results from tube pointings as csv string
    data = db.Column(db.String(500))
    # result: stars visible in the sky
    sky_stars = db.Column(db.Integer)
    # comment from the observer
    comment = db.Column(db.Unicode)
    # relations
    observation = db.relationship('Observation', back_populates='tube_data')
    # foreign keys
    observation_id = db.Column(db.Integer, db.ForeignKey('observations.id'))

    def __init__(self, observation, sky_stars):
        self.observation = observation
        self.sky_stars = sky_stars

    def __unicode__(self):
        return u'total of %d stars in the sky' % self.sky_stars

    def __str__(self):
        return self.__unicode__().encode('utf-8')
