
from sqlalchemy import create_engine, Column, DateTime, Integer, String, \
    Unicode, Boolean, Float, ForeignKey, Enum
from sqlalchemy.orm import  deferred, relationship
from datetime import datetime,timedelta

from jizera.database import Base

# table for registered observers
class Observer(Base):

    __tablename__ = 'observers'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # observer info
    name = Column(Unicode(60))
    lastname = Column(Unicode(60))
    email = Column(Unicode(255), unique=True)
    # OpenID
    openid_openid = Column(String(255), unique=True)
    openid_identity = Column(String(255))
    openid_server = Column(String(255))

    # relationships
    observations = relationship('Observation', back_populates='observer')
    reviews = relationship('Review', back_populates='observer')

    def __unicode__(self):
        return u'%s %s <%s>' % (self.name, self.lastname, self.email)
        # return '%s' % self.name

    def __str__(self):
        return self.__unicode__().encode('utf-8')


# location
class Location(Base):

    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # name of the observing spot -- entered by the user or
    # taken from google geolocalization
    name = Column(Unicode(200))
    # location and altitude
    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(Float)
    # optional place for code used for google synchronization -- not neccesary?
    googlecode = Column(String(45))
    lettercode = Column(String(12))
    # relationships
    reviews = relationship('Review', back_populates='location')
    observations = relationship('Observation', back_populates='location')

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def __unicode__(self):
        nswe = u'%.4f %s, %.4f %s' % (\
            abs(self.latitude), \
            'N' if self.latitude >= 0 else 'S', \
            abs(self.longitude),  \
            'E' if self.longitude >= 0 else 'W'  )
        if self.name != None:
            return u'%s (%s)' % ( nswe, self.name )
        return  nswe


# optional review that can be written for given location
class Review(Base):

    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # survey about the observation spot
    has_current = Column(Enum('free','limited','none'))
    has_caraccess = Column(Enum('free','limited','none'))
    has_sleeping = Column(Enum('free','limited','none'))
    has_horizon = Column(Enum('visible','southonly','none'))
    # comment where user can put additional notes
    comment = Column(Unicode)
    # relations
    location = relationship('Location', back_populates='reviews')
    observer = relationship('Observer', back_populates='reviews')
    # foreign keys
    location_id = Column(Integer, ForeignKey('locations.id'))
    observer_id = Column(Integer, ForeignKey('observers.id'))

    def __unicode__(self):
        return u'%s commented on location %s: %s' % (self.observer, self.location, self.comment)

    def __str__(self):
        return self.__unicode__().encode('utf-8')


# class for observations (1 filled form = 1 observation)
class Observation(Base):

    __tablename__ = 'observations'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # date of begin and end
    date_start = Column(DateTime)
    date_end = Column(DateTime)
    # conditions: clouds, moon and milky way
    cond_clouds_octants = Column(Enum('clear','scattered','broken','overcast'))
    # cond_moon = Column(Boolean)
    cond_milkyway = Column(Boolean)
    # relations
    location = relationship('Location', back_populates='observations')
    observer = relationship('Observer', back_populates='observations')
    # typy pomiarow
    bortle_data = relationship('BortleData', back_populates='observation')
    dslr_data = relationship('DSLRData', back_populates='observation')
    sqm_data = relationship('SQMData', back_populates='observation')
    meteor_data = relationship('MeteorData', back_populates='observation')
    tube_data = relationship('TubeData', back_populates='observation')
    # foreign keys
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    observer_id = Column(Integer, ForeignKey('observers.id'), nullable=False)

    def __unicode__(self):
        return u'observation performed on %s by %s in location %s'   \
            % (self.date_start,self.observer,self.location)

    def __str__(self):
        return self.__unicode__().encode('utf-8')


# Following entries are various kinds of measurments

# entries for bortle method
class BortleData(Base):
    __tablename__ = 'bortle_data'
    id = Column(Integer, primary_key=True)
    # bortle degree of sky darkness
    degrees = Column(Integer)
    # comment from the observer
    comment = deferred(Column(Unicode), group='extras')
    # relations
    observation = relationship('Observation', back_populates='bortle_data')
    # foreign keys
    observation_id = Column(Integer, ForeignKey('observations.id'))

    def recalc(self):
        pass

    def __unicode__(self):
        return u'%d in Bortle scale' % self.degrees

    def __str__(self):
        return self.__unicode__().encode('utf-8')


# entries for dslr measurments
class DSLRData(Base):
    __tablename__ = 'dslr_data'
    id = Column(Integer, primary_key=True)
    # info about camera
    info_camera = Column(Unicode(200))
    info_lens = Column(Unicode(200))
    # field number
    field_nr = Column(Integer)
    # data as copied from the spreadsheet
    data = deferred(Column(String(400)), group='raw')
    # result: DSLR magnitude of background glow
    magnitude = Column(Float)
    # comment from the observer
    comment = deferred(Column(Unicode), group='extras')
    # relations
    observation = relationship('Observation', back_populates='dslr_data')
    # foreign keys
    observation_id = Column(Integer, ForeignKey('observations.id'))

    def recalc(self):
        pass

    def __unicode__(self):
        return u'DSLR observation in field %d with result %0.2f' \
            % ( self.field_nr, self.magnitude )

    def __str__(self):
        return self.__unicode__().encode('utf-8')

# entries for meteor (limiting magniude) method
class MeteorData(Base):
    __tablename__ = 'meteor_data'
    id = Column(Integer, primary_key=True)
    # number of field
    field_nr = Column(Integer)
    # user measurement
    num_stars = Column(Integer)
    # result: limiting magnitude
    magnitude = Column(Float)
    # comment from the observer
    comment = deferred(Column(Unicode), group='extras')
    # relations
    observation = relationship('Observation', back_populates='meteor_data')
    # foreign keys
    observation_id = Column(Integer, ForeignKey('observations.id'))

    def recalc(self):
        pass

    def __unicode__(self):
        return u'%d stars in field %d which yields limiting magnitude %0.2f' \
            % ( self.num_stars, self.field_nr, self.magnitude )

    def __str__(self):
        return self.__unicode__().encode('utf-8')


# SQM measurments
class SQMData(Base):
    __tablename__ = 'sqm_data'
    id = Column(Integer, primary_key=True)
    sqm_model = Column(String(45))
    sqm_serial = Column(String(45))
    # all values entered by the user in json/csv format
    data = deferred(Column(String(500)), group='raw')
    # results obtained for zenith and all directions
    magnitude_z = Column(Float)
    magnitude_n = Column(Float)
    magnitude_e = Column(Float)
    magnitude_s = Column(Float)
    magnitude_w = Column(Float)
    # comment from the observer
    comment = deferred(Column(Unicode), group='extras')
    # relations
    observation = relationship('Observation', back_populates='sqm_data')
    # foreign keys
    observation_id = Column(Integer, ForeignKey('observations.id'))

    def recalc(self):
        pass

    def __unicode__(self):
        return u'SQM results: zenith %0.2f, N %0.2f, E %0.2f, S %0.2f, W %0.2f' \
            % ( self.magnitude_z, self.magnitude_n, self.magnitude_e,
                self.magnitude_s, self.magnitude_w )

    def __str__(self):
        return self.__unicode__().encode('utf-8')


# Tube measurments
class TubeData(Base):
    __tablename__ = 'tube_data'
    id = Column(Integer, primary_key=True)
    # additional parameters of the tube
    tube_diam = Column(Float)
    tube_length = Column(Float)
    tube_type = Column(String(6))
    tube_glasses = Column(Boolean)
    # results from tube pointings as csv string
    data = deferred(Column(String(500)), group='raw')
    # result: stars visible in the sky
    num_stars = Column(Integer)
    # comment from the observer
    comment = deferred(Column(Unicode), group='extras')
    # relations
    observation = relationship('Observation', back_populates='tube_data')
    # foreign keys
    observation_id = Column(Integer, ForeignKey('observations.id'))

    def recalc(self):
        pass

    def __unicode__(self):
        return u'total of %d stars in the sky' % self.num_stars

    def __str__(self):
        return self.__unicode__().encode('utf-8')
