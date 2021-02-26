import calendar
import datetime


def generate_utc_epoch():
    return calendar.timegm(datetime.datetime.now().timetuple())
