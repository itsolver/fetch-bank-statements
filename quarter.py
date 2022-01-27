from datetime import date
import datetime

today = date.today()


def previous_quarter_end(ref):
    if ref.month < 4:
        return datetime.date(ref.year - 1, 12, 31)
    elif ref.month < 7:
        return datetime.date(ref.year, 3, 31)
    elif ref.month < 10:
        return datetime.date(ref.year, 6, 30)
    return datetime.date(ref.year, 9, 30)


def previous_quarter_start(ref):
    if ref.month < 4:
        return datetime.date(ref.year - 1, 10, 1)
    elif ref.month < 7:
        return datetime.date(ref.year, 1, 1)
    elif ref.month < 10:
        return datetime.date(ref.year, 4, 1)
    return datetime.date(ref.year, 7, 1)


print(previous_quarter_start(today))
print(previous_quarter_end(today))
