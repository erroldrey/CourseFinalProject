import datetime


class Period:
    def __init__(self, start_p):
        self.start_p = start_p
        self.end_p = minus_months(start_p,-3)- datetime.timedelta(1)
        self.now_p = start_p + datetime.timedelta(14)
        self.end = False

    def __iter__(self):
        return self

    def __next__(self):
        period_start = self.start_p
        period_end = self.now_p

        if self.end:
            raise StopIteration
        if period_end >= self.end_p:
            self.end = True

        self.start_p = period_end + datetime.timedelta(1)
        self.now_p = period_end + datetime.timedelta(14)
        if self.now_p >= self.end_p:
            self.now_p = self.end_p
        return period_start, period_end

def get_date_p():
    now = datetime.datetime.now()
    date_p = minus_months(now, 3)

    month_num = date_p.month
    if month_num in (2, 5, 8, 11):
        date_p = minus_months(date_p, 1)
    elif month_num in (3, 6, 9, 12):
        date_p = minus_months(date_p, 2)

    return date_p


def minus_months(sourcedate, months):
    month = sourcedate.month - 1 - months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = 1
    return datetime.date(year, month, day)