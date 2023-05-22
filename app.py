from flask import Flask, render_template, jsonify, request
from dateutil import rrule, parser
from datetime import datetime, timedelta
import json

app = Flask(__name__)


@app.route('/')
def calendar():
    return render_template('calendar.html')


@app.route('/events')
def events():
    with open('events.json') as json_file:
        events = json.load(json_file)
        expanded_events = expand_recurring_events(events)

        time_range = request.args.get('range', 'day')
        start_date = datetime.now()
        end_date = datetime.now()

        if time_range == 'day':
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif time_range == 'week':
            start_date = start_date - timedelta(days=start_date.weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=6, hours=23, minutes=59, seconds=59, microseconds=999999)
        elif time_range == 'month':
            start_date = start_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date.replace(day=1, month=start_date.month + 1) - timedelta(days=1, microseconds=1)
            end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif time_range == 'year':
            start_date = start_date.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)

        filtered_events = [
            event for event in expanded_events
            if parser.isoparse(event["start"]) >= start_date and parser.isoparse(event["end"]) <= end_date
        ]

        return jsonify(filtered_events)


def expand_recurring_events(events):
    expanded_events = []
    for event in events:
        if "recurrence" in event:
            start = parser.isoparse(event["start"])
            end = parser.isoparse(event["end"])
            recurrence_rule = event["recurrence"]
            recurring_events = list(rrule.rrulestr(recurrence_rule, dtstart=start))
            for recurring_event in recurring_events:
                recurring_event = recurring_event.isoformat()
                expanded_event = event.copy()
                expanded_event["start"] = recurring_event
                expanded_event["end"] = recurring_event
                expanded_events.append(expanded_event)
        else:
            expanded_events.append(event)
    return expanded_events


if __name__ == '__main__':
    app.run()
