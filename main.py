import calendar

from dateutil.rrule import rrule, MONTHLY, WEEKLY, DAILY, rrulestr
from dateutil.parser import parse
from dateutil.tz import gettz
from datetime import datetime

event2 = {
    "start": datetime(2014, 12, 31),
    "repeat": {
        "freq": MONTHLY,
        "count": 3,
    }
}

event = {
  'summary': 'Appointment',
  'location': 'Somewhere',
  'start': {
    'dateTime': '2011-06-03T10:00:00.000-07:00',
    'timeZone': 'America/Los_Angeles'
  },
  'end': {
    'dateTime': '2011-06-03T10:25:00.000-07:00',
    'timeZone': 'America/Los_Angeles'
  },
  'recurrence': [
    'RRULE:FREQ=WEEKLY;UNTIL=20110701T170000Z',
  ],
  'attendees': [
    {
      'email': 'andre.lersveen@nrk.no',
    },
  ],
}

if event['recurrence']:
    event_list = list(rrulestr(event['recurrence'][0], dtstart=parse(event['start']['dateTime'])))
    for item in event_list:
        print(item.strftime('%l:%M%p %Z on %b %d, %Y'))

tc = calendar.HTMLCalendar(firstweekday=0)
print(tc.formatmonth(2016, 5))

my_calendar = calendar.Calendar()

for weekday in my_calendar.iterweekdays():
    if weekday:
        print(weekday)
