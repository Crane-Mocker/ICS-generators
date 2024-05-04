#This is an ICS file generator for the calendar event
#ref https://datatracker.ietf.org/doc/html/rfc5545

from datetime import datetime, timedelta
from icalendar import Calendar, Event
import pytz
import re
from calendar import month_abbr

#edit this part according to your needs
EVENT_NAME = "My Meeting"
EVENT_WEEKDAYS = ["Thu"] #["Mon", "Wed", "Fri"]
OUTPUT = "my_meetings.ics"
START_DATE = "2024-05-06"
END_DATE = "2024-07-30"
EVENT_START_TIME = "3:00PM"
EVENT_END_TIME = "4:00PM"
timezone = pytz.timezone("US/Eastern")

# calculate the dates for events, from SRART_DATE to END_DATE
def get_dates():
    start_date = datetime.strptime(START_DATE, "%Y-%m-%d")
    end_date = datetime.strptime(END_DATE, "%Y-%m-%d")
    dates = []
    while start_date <= end_date:
        #print(start_date.strftime("%a"))
        if start_date.strftime("%a") in EVENT_WEEKDAYS:
            dates.append(start_date)
        start_date += timedelta(days=1)
    return dates

# generate the start time and end time for the event of a date
def gen_time(date):
    start_time = datetime.strptime(f"{date.strftime('%Y-%m-%d')} {EVENT_START_TIME}", "%Y-%m-%d %I:%M%p")
    start_time = timezone.localize(start_time)
    end_time = datetime.strptime(f"{date.strftime('%Y-%m-%d')} {EVENT_END_TIME}", "%Y-%m-%d %I:%M%p")
    end_time = timezone.localize(end_time)
    return start_time, end_time

# generate the event for a date
def gen_event(date, start_time, end_time):
    event = Event()
    event.add('summary', EVENT_NAME)
    event.add('dtstart', start_time)
    event.add('dtend', end_time)
    event.add('dtstamp', datetime.now(timezone))
    return event

def gen_ics(dates):
    cal = Calendar()
    cal.add('prodid', '-//C0CO//NUT//')
    cal.add('version', '2.0')
    for date in dates:
        start_time, end_time = gen_time(date)
        event = gen_event(date, start_time, end_time)
        cal.add_component(event)
    return cal

def save_ics(cal):
    with open(OUTPUT, 'wb') as f:
        f.write(cal.to_ical())

#test
dates = get_dates()
cal = gen_ics(dates)
save_ics(cal)

