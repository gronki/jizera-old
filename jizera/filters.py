
from jizera import app
from datetime import datetime

@app.template_filter('sql_datetime')
def parse_sql_datetime(s):
    return datetime.strptime(s, r'%Y-%m-%d %H:%M:%S')

@app.template_filter('sql_timestamp')
def parse_sql_timestamp(s):
    return datetime.strptime(s, r'%Y-%m-%d %H:%M:%S.%f')

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

@app.template_filter('latlng')
def filter_latlong(latlng):
    lat,lng = latlng
    return u"@%0.3f,%0.3f" % (lat,lng)
