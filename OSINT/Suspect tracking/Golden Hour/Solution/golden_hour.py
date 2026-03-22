from datetime import date, timedelta, time, datetime

import pytz
from astral import LocationInfo
from astral.sun import sun, azimuth as sun_azimuth

loc = LocationInfo(timezone="CET", latitude=36.04865, longitude=14.19105)

print(loc.timezone)

d = date(2025, 1, 1)
while d.year == 2025:
    s = sun(loc.observer, date=d, tzinfo=pytz.timezone(loc.timezone))['sunset']
    # if s.hour == 17 and s.minute == 14:
    #     print(d)
    if s.hour == 17:
        date_time = pytz.timezone(loc.timezone).localize(datetime.combine(d, time(17, 14)))
        azimuth = sun_azimuth(loc.observer, date_time)
        print(f'date {d} - sunset at {s.hour}:{s.minute}, azimuth at 17:14 is {azimuth:.3f}')
    d += timedelta(days=1)
