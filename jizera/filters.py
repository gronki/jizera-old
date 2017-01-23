# -*- coding: utf-8 -*-

from jizera import app
from datetime import datetime

@app.template_filter('timeago')
def filter_timeago(d):
    td = datetime.now() - d
    if td.days == 0:
        return u"%d godzin(y) temu" % (td.seconds/3600)
    elif td.days == 1:
        return u"wczoraj"
    elif td.days == 2:
        return u"przedwczoraj"
    else:
        return u"%d dni temu" % td.days

@app.template_filter('onlydate')
def filter_onlydate(d):
    return d.strftime('%y-%m-%d')
