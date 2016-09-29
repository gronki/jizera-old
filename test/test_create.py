#!/usr/bin/env python
# coding=utf8

from jizera import *
from random import seed, gauss, uniform, randrange, randint
from mbox import *
from os import remove, path
from loremipsum import get_sentences
from datetime import datetime
from time import time as timestamp
from math import cos

# wywalamy stara baze
if path.isfile(testdb_location):
    remove(testdb_location)


# zasiewamy ziarno generatora liczb losowych
seed()

# tworzymy silnik i sesje
db.create_all()

# tworzymy obserwatorow
print hh1('OBSERWATORZY')

observers = [   Observer(u'Łukasz',u'Kowalski',u'lukaszek@abc.com'), \
                Observer(u'Mariola',u'Kiepska',u'mariola@polsat.pl'), \
                Observer(u'Donutella',u'Versace',u'donut@versace.it'), \
                Observer(u'Linus',u'Torvalds',u'linus@kernel.org') ]
for t in observers:
    print t
db.session.add_all(observers)
db.session.commit()

# tworzymy miejsca
print hh1(u'LOKALIZACJE')

locations = []
loc_names_a = [ u'Przyłęcze', u'Zadupie', u'Ostrowo', u'Konolipie', u'Nietopie', \
        u'Durniewo', u'Gajowo', u'Koniowo', u'Świniarowo', u'Kozłowo', u'Kurowo', \
        u'Zabrodzie', u'Sarniewo' ]
loc_names_b = [ u'Dolnośląskie', u'Łódzkie', u'Górne', u'Dolne', u'Wielkie', u'Małe', \
                u'Wielkopolskie', u'Mazowieckie', u'Wiślańskie', u'Rządowe',    \
                u'Pierwsze', u'Drugie' ]
for i in range(50):
    name = u'%s %s' % (  loc_names_a[randrange(len(loc_names_a))],    \
                        loc_names_b[randrange(len(loc_names_b))])
    l = Location(uniform(49.5,54.5), uniform(14.7,23.7), name)
    locations.append(l)
    print l
db.session.add_all(locations)
db.session.commit()

# dodajemy jakies recenzje
print hh1('RECENZJE')

for i in range(100):
    print hh3('Recenzja %d' % (i+1))
    rev = Review(   locations[randrange(len(locations))], \
                    observers[randrange(len(observers))], \
                    (u' '.join(get_sentences(randrange(1,9)))) )
    print rev
    db.session.add(rev)

db.session.commit()

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
    obs = Observation(  locations[randrange(len(locations))], \
                        observers[randrange(len(observers))], \
                        datetime.fromtimestamp(time) )
    print obs

    db.session.add(obs)
    db.session.commit()

    ss = (1 + cos(obs.location.latitude * 2 * m_pi / 2)) \
        + (1 + cos(obs.location.longitude * 2 * m_pi / 1))
    data_base = 0.25 * ss * (22.8-16) + gauss(16,0.1) \
        - 1.2 * (5 - yrsback) / 5

    print u'Jasność bazowa: %.2f' % data_base

    if uniform(0,1) < 0.5:
        dat = DSLRData(obs, randint(1,10), data_base + gauss(0,0.1))
        print dat
        db.session.add(dat)
    if uniform(0,1) < 0.95:
        dat = BortleData(obs, round(yfun(16,7,23.5,1,data_base)))
        print dat
        db.session.add(dat)
    if uniform(0,1) < 0.3:
        dat = TubeData(obs, round(yfun(16,300,22.5,2800,data_base + gauss(0,1.0))))
        print dat
        db.session.add(dat)
    if uniform(0,1) < 0.4:
        dat = MeteorData(obs, randint(1,10), \
            round(yfun(16,10,22.5,60,data_base + gauss(0,0.4))))
        print dat
        db.session.add(dat)
    if uniform(0,1) < 0.7:
        dat = SQMData(obs, (data_base + gauss(0,0.1),    \
            data_base + gauss(-0.8,0.3), data_base + gauss(-0.8,0.3),   \
            data_base + gauss(-0.8,0.3), data_base + gauss(-0.8,0.3)) )
        print dat
        db.session.add(dat)


    db.session.commit()


print hh1('KONIEC')

db.session.close_all()
