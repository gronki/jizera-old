#!/usr/bin/env python
# coding=utf8

# from jizera.database import *

from random import seed, gauss, uniform, randrange, randint
from mbox import *
from os import remove, path
from loremipsum import get_sentences
from datetime import datetime
from time import time as timestamp
from math import cos

db_location = '/tmp/jizera-testing.db'

# wywalamy stara baze
if path.isfile(db_location):
    remove(db_location)


# zasiewamy ziarno generatora liczb losowych
seed()

# tworzymy silnik i sesje
# init_db()
# import jizera.models
from jizera.database import *
# from jizera.models import *
# Base.metadata.create_all(bind=engine)

# tworzymy obserwatorow
print hh1('OBSERWATORZY')

observers = [  \
    Observer(name=u'Łukasz',lastname=u'Kowalski',email=u'lukaszek@abc.com'), \
    Observer(name=u'Mariola',lastname=u'Kiepska',email=u'mariola@polsat.pl'), \
    Observer(name=u'Linus',lastname=u'Torvalds',email=u'linus@kernel.org'), \
    Observer(name=u'Donutella',lastname=u'Versace',email=u'donutella@versace.com'), \
    ]
for t in observers:
    print t
dbsession.add_all(observers)
dbsession.commit()

# tworzymy miejsca
print hh1(u'LOKALIZACJE')

locations = []
loc_names_a = [ u'Przyłęcze', u'Zadupie', u'Ostrowo', u'Konolipie', u'Nietopie',
        u'Durniewo', u'Gajowo', u'Koniowo', u'Świniarowo', u'Kozłowo', u'Kurowo',
        u'Zabrodzie', u'Sarniewo' ]
loc_names_b = [ u'Dolnośląskie', u'Łódzkie', u'Górne', u'Dolne', u'Wielkie', u'Małe',
                u'Wielkopolskie', u'Mazowieckie', u'Wiślańskie', u'Rządowe',
                u'Pierwsze', u'Drugie' ]
for i in range(25):
    name = u'%s %s' % (  loc_names_a[randrange(len(loc_names_a))],
                        loc_names_b[randrange(len(loc_names_b))])
    l = Location(latitude = uniform(49.5,54.5), longitude = uniform(14.7,23.7), \
            name = name)
    locations.append(l)
    print l
dbsession.add_all(locations)
dbsession.commit()

# dodajemy jakies recenzje
print hh1('RECENZJE')

for i in range(200):
    print hh3('Recenzja %d' % (i+1))
    rev = Review(   location_id = locations[randrange(len(locations))].id, \
                    observer_id = observers[randrange(len(observers))].id, \
                    comment = (u' '.join(get_sentences(randrange(1,9)))) )
    print rev
    dbsession.add(rev)

dbsession.commit()

# obserwacje
print hh1('OBSERWACJE')

def yfun(x1,y1,x2,y2,x):
    return float(x - x1) * (y2-y1)/float(x2-x1) + y1

time0 = timestamp()

m_pi = 3.1415

for i in range(250):
    print hh3('Obserwacja %d' % (i+1))
    yrsback = uniform(0,5)
    time = time0 - (yrsback * 365) * 24 * 3600
    # self.date_start = (datetime.now() + timedelta(days=-1)) \
    #     .replace(hour=22,minute=0,second=0,microsecond=0)
    date_start = datetime.fromtimestamp(time) \
          .replace(hour=22,minute=0,second=0,microsecond=0)
    loc0 = locations[randrange(len(locations))]
    obs = Observation(  location_id = loc0.id,
                        observer_id = observers[randrange(len(observers))].id,
                        date_start = date_start,
                        date_end = date_start + timedelta(hours=1) )
    print obs

    dbsession.add(obs)

    ss = (1 + cos(loc0.latitude * 2 * m_pi / 2)) \
        + (1 + cos(loc0.longitude * 2 * m_pi / 1))
    data_base = 0.25 * ss * (22.8-16) + gauss(16,0.1) \
        - 1.2 * (5 - yrsback) / 5

    print u'Jasność bazowa: %.2f' % data_base

    if uniform(0,1) < 0.5:
        dat = DSLRData(observation=obs,
                field_nr=randint(1,10),
                magnitude=data_base + gauss(0,0.1))
        print dat
        dbsession.add(dat)
    if uniform(0,1) < 0.95:
        dat = BortleData(observation=obs,
                degrees=round(yfun(16,7,23.5,1,data_base)))
        print dat
        dbsession.add(dat)
    if uniform(0,1) < 0.3:
        dat = TubeData(observation=obs,
                num_stars = round(yfun(16,300,22.5,2800,data_base + gauss(0,1.0))))
        print dat
        dbsession.add(dat)
    if uniform(0,1) < 0.4:
        dat = MeteorData(   observation = obs,
                            field_nr = randint(1,10),
                            num_stars = round(yfun(16,10,22.5,60,data_base + gauss(0,0.4))),
                            magnitude = yfun(16,3.5,22.5,7.5,data_base + gauss(0,0.4))
                        )
        print dat
        dbsession.add(dat)
    if uniform(0,1) < 0.7:
        dat = SQMData(  observation = obs,
                magnitude_z = data_base + gauss(0,0.1),
                magnitude_n = data_base + gauss(-0.8,0.3),
                magnitude_e = data_base + gauss(-0.8,0.3),
                magnitude_s = data_base + gauss(-0.8,0.3),
                magnitude_w = data_base + gauss(-0.8,0.3),
            )
        print dat
        dbsession.add(dat)


    dbsession.commit()


print hh1('KONIEC')

destroy_db()
