# -*- coding: utf-8 -*-

from re import match
from re import compile
from flask import request

rexp_email = compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

def validate_empty(validation, field, message=u'To pole nie może być puste.'):
    if request.form[field] == '':
        validation[field] = message

def validate_email(validation, field, message=u'To nie wygląda mi na poprawny adres e-mail :('):
    if not match(rexp_email,request.form[field]):
        validation[field] = message
