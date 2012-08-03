import requests
import json
import icalendar
from datetime import datetime
import pytz

BASE = "https://graph.facebook.com/%s"
DEFAULT_TIMEZONE = "America/Los_Angeles"
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'

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


    

if __name__=="__main__":
    events = get_events()['data']
    import pprint
    calendar = prepare_calendar()
    for event in events:
        calendar.add_component(parse_event(event))
    open('output.ics','w').write(calendar.to_ical())

