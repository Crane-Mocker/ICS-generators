#This is an ICS file generator for weekly courses
#See the schedule.txt for input format
#ref https://datatracker.ietf.org/doc/html/rfc5545

from datetime import datetime, timedelta
from icalendar import Calendar, Event
import pytz
import re
from calendar import month_abbr

#change this part
COURSE_NAME = "CS 798"
COURSE_TIME = "10:00AM-11:20AM"
INPUT_FILE = "schedule.txt"

timezone = pytz.timezone("US/Eastern")

def parse_schedule(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    event_lines = []
    for line in lines[1:]:
        if not line.startswith("Module"):
            event_lines.append(line)
    return event_lines

def gen_event(summary, start_time, end_time, transp_flag):
    event = Event()
    event.add('summary', summary)
    event.add('dtstart', start_time)
    event.add('dtend', end_time)
    event.add('dtstamp', datetime.now(timezone))
    if transp_flag:
        event.add('transp', 'TRANSPARENT')
    return event

def gen_ics(event_lines):
    cal = Calendar()
    cal.add('prodid', '-//C0CO//NUT//')
    cal.add('version', '2.0')
    fmt = "%I:%M%p %b %d %Y"
    year = datetime.now().year

    for line in event_lines:
        #print(line)
        month, day, *event = line.split()
        #print(month, day, event)
        if not event:
            #print(f"{month} {day} {COURSE_TIME.split('-')[0]} {year}")
            start_time = datetime.strptime(f"{COURSE_TIME.split('-')[0]} {month} {day} {year}", fmt)
            end_time = datetime.strptime(f"{COURSE_TIME.split('-')[1]} {month} {day} {year}", fmt)
            cal.add_component(gen_event(COURSE_NAME, timezone.localize(start_time), timezone.localize(end_time), False))
        else:
            event_str = " ".join(event)
            if "no class" in event_str:
                pass
            elif re.match(r"Assignment \d+ due", event_str):
                summary = event_str
                all_day_date = datetime.strptime(f"{month} {day} {year}", "%b %d %Y")
                cal.add_component(gen_event(event_str, all_day_date.date(), all_day_date.date() + timedelta(days=1), True))
            else:
                start_time = datetime.strptime(f"{COURSE_TIME.split('-')[0]} {month} {day} {year}", fmt)
                end_time = datetime.strptime(f"{COURSE_TIME.split('-')[1]} {month} {day} {year}", fmt)
                cal.add_component(gen_event(event_str, timezone.localize(start_time), timezone.localize(end_time), False))

    return cal.to_ical()

def save_ics(ical_data, file_path):
    with open(file_path, 'wb') as f:
        f.write(ical_data)

event_lines = parse_schedule(INPUT_FILE)
ical_data = gen_ics(event_lines)
file_path = f"{COURSE_NAME}.ics"
save_ics(ical_data, file_path)
print(f"iCalendar file: {file_path}")


