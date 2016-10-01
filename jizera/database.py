
from sqlalchemy import create_engine, Column, DateTime, Integer, String, \
    Unicode, Boolean, deferred, relationship
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime,timedelta

db_location = '/tmp/jizera-testing.db'

engine = create_engine('sqlite:///' + db_location, convert_unicode=True, echo=True)
dbsession = scoped_session(sessionmaker(autocommit=False))

Base = declarative_base()
Base.query = dbsession.query_property()

def init_db():
    Base.metadata.create_all(bind=engine)

def destroy_db():
    dbsession.remove()



# table for registered observers
class Observer(Base):

    __tablename__ = 'observers'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime)
    modified = Column(DateTime)
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
class Location(Base):

    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime)
    modified = Column(DateTime)
    # name of the observing spot -- entered by the user or
    # taken from google geolocalization
    name = Column(Unicode(200))
    # location and altitude
    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(Float)
    # optional place for code used for google synchronization -- not neccesary?
    googlecode = Column(String(45))
    # relationships
    reviews = relationship('Review', back_populates='location')
    observations = relationship('Observation', back_populates='location')

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
class Review(Base):

    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime)
    modified = Column(DateTime)
    # survey about the observation spot
    has_current = Column(Boolean)
    has_sleeping = Column(Boolean)
    has_horizon = Column(Boolean)
    # comment where user can put additional notes
    comment = Column(Unicode)
    # relations
    location = relationship('Location', back_populates='reviews')
    observer = relationship('Observer', back_populates='reviews')
    # foreign keys
    location_id = Column(Integer, ForeignKey('locations.id'))
    observer_id = Column(Integer, ForeignKey('observers.id'))


    def __init__(self, location, observer, comment):
        self.location = location
        self.observer = observer
        self.comment = comment

    def __unicode__(self):
        return u'%s commented on location %s: %s' % (self.observer, self.location, self.comment)

    def __str__(self):
        return self.__unicode__().encode('utf-8')


# class for observations (1 filled form = 1 observation)
class Observation(Base):

    __tablename__ = 'observations'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime)
    modified = Column(DateTime)
    # date of begin and end
    date_start = Column(DateTime)
    date_end = Column(DateTime)
    # conditions: clouds, moon and milky way
    cond_clouds = Column(Boolean)
    cond_moon = Column(Boolean)
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
    location_id = Column(Integer, ForeignKey('locations.id'))
    observer_id = Column(Integer, ForeignKey('observers.id'))

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
class BortleData(Base):
    __tablename__ = 'bortle_data'
    id = Column(Integer, primary_key=True)
    # bortle degree of sky darkness
    bortle = Column(Integer)
    # comment from the observer
    comment = Column(Unicode)
    # relations
    observation = relationship('Observation', back_populates='bortle_data')
    # foreign keys
    observation_id = Column(Integer, ForeignKey('observations.id'))

    def __init__(self, observation, bortle):
        self.observation = observation
        self.bortle = bortle

    def recalc(self):
        pass

    def __unicode__(self):
        return u'%d in Bortle scale' % self.bortle

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
    data = Column(String(400))
    # result: DSLR magnitude of background glow
    dlsr_mag = Column(Float)
    # comment from the observer
    comment = Column(Unicode)
    # relations
    observation = relationship('Observation', back_populates='dslr_data')
    # foreign keys
    observation_id = Column(Integer, ForeignKey('observations.id'))

    def __init__(self, observation, field_nr, dslr_mag):
        self.observation = observation
        self.field_nr = field_nr
        self.dslr_mag = dslr_mag

    def recalc(self):
        pass

    def __unicode__(self):
        return u'DSLR observation in field %d with result %0.2f' \
            % ( self.field_nr, self.dslr_mag )

    def __str__(self):
        return self.__unicode__().encode('utf-8')

def yfun(x1,y1,x2,y2,x):
    return float(x - x1) * (y2-y1)/float(x2-x1) + y1

# entries for meteor (limiting magniude) method
class MeteorData(Base):
    __tablename__ = 'meteor_data'
    id = Column(Integer, primary_key=True)
    # number of field
    field_nr = Column(Integer)
    # user measurement
    stars = Column(Integer)
    # result: limiting magnitude
    lim_mag = Column(Float)
    # comment from the observer
    comment = Column(Unicode)
    # relations
    observation = relationship('Observation', back_populates='meteor_data')
    # foreign keys
    observation_id = Column(Integer, ForeignKey('observations.id'))

    def __init__(self, observation, field_nr, stars):
        self.observation = observation
        self.field_nr = field_nr
        self.stars = stars
        self.lim_mag = yfun(10,3.5,60,7.5,stars)

    def recalc(self):
        pass

    def __unicode__(self):
        return u'%d stars in field %d which yields limiting magnitude %0.2f' \
            % ( self.stars, self.field_nr, self.lim_mag )

    def __str__(self):
        return self.__unicode__().encode('utf-8')


# SQM measurments
class SQMData(Base):
    __tablename__ = 'sqm_data'
    id = Column(Integer, primary_key=True)
    sqm_model = Column(String(45))
    sqm_serial = Column(String(45))
    # all values entered by the user in json/csv format
    data = Column(String(500))
    # results obtained for zenith and all directions
    sqm_mag = Column(Float)
    sqm_mag_n = Column(Float)
    sqm_mag_s = Column(Float)
    sqm_mag_w = Column(Float)
    sqm_mag_e = Column(Float)
    # comment from the observer
    comment = Column(Unicode)
    # relations
    observation = relationship('Observation', back_populates='sqm_data')
    # foreign keys
    observation_id = Column(Integer, ForeignKey('observations.id'))

    def __init__(self, observation, sqm_mag_tuple):
        ( self.sqm_mag, self.sqm_mag_n, self.sqm_mag_e, self.sqm_mag_s, \
            self.sqm_mag_w ) = sqm_mag_tuple
        self.observation = observation

    def recalc(self):
        pass

    def __unicode__(self):
        return u'SQM results: zenith %0.2f, N %0.2f, E %0.2f, S %0.2f, W %0.2f' \
            % ( self.sqm_mag, self.sqm_mag_n, self.sqm_mag_e, self.sqm_mag_s, \
                self.sqm_mag_w )

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
    data = Column(String(500))
    # result: stars visible in the sky
    sky_stars = Column(Integer)
    # comment from the observer
    comment = Column(Unicode)
    # relations
    observation = relationship('Observation', back_populates='tube_data')
    # foreign keys
    observation_id = Column(Integer, ForeignKey('observations.id'))

    def __init__(self, observation, sky_stars):
        self.observation = observation
        self.sky_stars = sky_stars

    def recalc(self):
        pass

    def __unicode__(self):
        return u'total of %d stars in the sky' % self.sky_stars

    def __str__(self):
        return self.__unicode__().encode('utf-8')
