# -*- coding: utf-8 -*-

from re import match
from re import compile
from flask import request, Markup
from datetime import datetime

rexp_email = compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
rexp_date_ddmmyyyy = compile(r"^([0-9]{2})\.([0-9]{2})\.([0-9]{4})$")
rexp_time_hhmm = compile(r"^([0-9]{2})\:([0-9]{2})$")

def validate(validation, what, field):
    value = request.form[field]
    value_print = Markup.escape(value)
    if 'required' in what:
        if value == '':
            validation[field] = u'To pole nie może być puste.'
            return
    if 'email' in what:
        if not match(rexp_email,value):
            validation[field] = u'To nie wygląda mi na poprawny adres e-mail :('
            return
    if 'date' in what:
        m = match(rexp_date_ddmmyyyy,value)
        if m:
            if  int(m.group(1)) == 0 or int(m.group(1)) > 31 \
                or int(m.group(2)) == 0 or int(m.group(2)) > 12 \
                or int(m.group(3)) < 1950 or int(m.group(2)) > datetime.now().year:
                validation[field] = u"Nie sądzisz, że coś jest nie tak z tą datą?";
                return
        else:
            validation[field] = u'Najbardziej lubię datę w formacie: %s, ' \
                u'niestety powyższa mi na taką nie wygląda :(' % datetime.now().strftime('%d.%m.%Y')
            return
    if 'time' in what:
        m = match(rexp_time_hhmm,value)
        if m:
            if  int(m.group(1)) > 23 or int(m.group(2)) > 59:
                validation[field] = u"W moim kraju nie ma takiej godziny...";
                return
        else:
            validation[field] = u"W San Escobar zapisujemy czas w formacie %s." % datetime.now().strftime('%H:%M')
            return
