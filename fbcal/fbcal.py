from flask import Flask, request, session, Response, render_template, json, jsonify

import requests
import icalendar
from datetime import datetime
import pytz
import os
from redis import Redis
from redis import from_url as redis_from_url

if os.path.exists('/home/dotcloud/environment.json'):
    with open('/home/dotcloud/environment.json') as f:
        env = json.load(f)
else:
    env = None

from local_vars import *

BASE = "https://graph.facebook.com/%s"
DEFAULT_TIMEZONE = "America/Los_Angeles"
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'

app = Flask(__name__)
if env:
    #redis = Redis(host=env["DOTCLOUD_CALENDRICS_REDIS_HOST"],port=env['DOTCLOUD_CALENDARICS_REDIS_PORT'],password=env["DOTCLOUD_CALENDARICS_REDIS_PASSWORD"],)
    redis = redis_from_url(env["DOTCLOUD_CALENDRICS_REDIS_URL"]) 
else:
    redis = Redis()

def get_events(access_token=ACCESS_TOKEN,limit=50):
    response = requests.get(BASE%'me/events?limit=%(limit)s&access_token=%(access_token)s'%locals())
    return json.loads(response.text)

def localize_date_str(datestr,date_fmt,timezone):
    return timezone.localize(datetime.strptime(datestr,date_fmt))

def parse_event(fbevent,default_timezone=DEFAULT_TIMEZONE,date_fmt=DATE_FORMAT):
    event = icalendar.Event()
    event.add('summary',fbevent['name'])
    timezone = pytz.timezone(fbevent['timezone'] if fbevent.has_key('timezone') else default_timezone)
    event.add('dtstart',localize_date_str(fbevent['start_time'],date_fmt,timezone))
    event.add('dtend',localize_date_str(fbevent['end_time'],date_fmt,timezone))
    if fbevent.has_key('location'):
        event.add('location',fbevent['location'])
    event.add('uid','e%s@facebook.com'%fbevent['id'])
    event.add('status','confirmed')
    event.add('partstat','accepted' if fbevent['rsvp_status'] == 'attending' else 'tentative')
    event.add('url','http://www.facebook.com/events/%s/'%fbevent['id'])
    return event

def prepare_calendar():
    cal = icalendar.Calendar()
    cal.add('version','2.0')
    cal.add('calscale','gregorian')
    return cal

def generate_ics(events):
    calendar = prepare_calendar()
    for event in events:
        calendar.add_component(parse_event(event))
    return calendar.to_ical()


    
@app.route('/')
def index():
    return 'Good News Everyone!'

def get_cached_calendar(calid):
    return redis.get('cached_cal_%s'%calid)

def set_cached_calendar(calid,ics,expiration = 15*60*60):
    return redis.setex('cached_cal_%s'%calid,ics,expiration)

def get_access_token(calid):
    return redis.get('access_token_%s'%calid)

@app.route('/cal/<calid>.ics')
def get_cal(calid):
    # TODO: sanitize calid
    # see if we have a cached calendar for this id
    cached_calendar = get_cached_calendar(calid)
    if cached_calendar:
        return cached_calendar
    else:
        # if we don't, see if we have an access token for this id
        access_token = get_access_token(calid)
        if access_token:
            # if we have an access token grab new events, parse and cache them!
            events_response = get_events(access_token=access_token)
            if events_response.has_key('error') or not events_response.has_key('data'):
                resp = jsonify(status = 403, message = 'Invalid access token')
                resp.status_code = 403
                return resp
            else:
                events = events_response['data']
                ics = generate_ics(events)
                set_cached_calendar(calid,ics)
                return Response(ics, status=200, mimetype='text/calendar')
        else: # if we don't have a cache or a token... we don't have anything on that calid!
            resp = jsonify(status = 404, message = "Don't know about that calendar")
            resp.status_code = 404
            return resp

if __name__=="__main__":
    app.run(debug=True)
    comment = """
    events = get_events()['data']
    import pprint
    calendar = prepare_calendar()
    for event in events:
        calendar.add_component(parse_event(event))
    open('output.ics','w').write(calendar.to_ical())"""

