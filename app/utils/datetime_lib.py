import datetime


def has_time_passed(target_datetime, minutes):
    if target_datetime is None:
        return True
    current_datetime = datetime.datetime.now()
    time_difference = current_datetime - target_datetime
    return time_difference.total_seconds() >= minutes * 60