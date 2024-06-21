import numpy as np
import pandas as pd
import os
import datetime as dt

#https://www.portalkadrowy.pl/czas-pracy/ustawa-z-18-stycznia-1951-r.-o-dniach-wolnych-od-pracy-tekst-jedn.-dz.u.-z-2020-r.-poz.-1920-6882.html

#https://en.wikipedia.org/wiki/Date_of_Easter#Algorithms
#Gauss's Easter algorithm
def calculate_easterG(year):
    a = year % 19
    b = year % 4
    c = year % 7
    k = np.floor_divide(year, 100)
    p = np.floor_divide(13 + 8*k, 25)
    q = np.floor_divide(k, 4)
    M = (15 - p + k - q) % 30
    N = (4 + k - q) % 7
    d = (19*a + M) % 30
    e = (2*b + 4*c + 6*d + N) % 7
    march_day = 22 + d + e
    if march_day <= 31:
        return dt.date(year, 3, march_day)
    april_day = d + e - 9
    if d == 28 and e == 6 and (11*M + 11) % 30 < 19:
        april_day = 18
    elif d == 29 and e == 6:
        april_day = 19
    return dt.date(year, 4, april_day)

#Anonymous Gregorian algorithm
def calculate_easterA(year):
    a = year % 19
    b = np.floor_divide(year, 100)
    c = year % 100
    d = np.floor_divide(b, 4)
    e = b % 4
    f = np.floor_divide(b + 8, 25)
    g = np.floor_divide(b - f + 1, 3)
    h = (19*a + b - d - g + 15) % 30
    i = np.floor_divide(c, 4)
    k = c % 4
    l = (32 + 2*e + 2*i - h - k) % 7
    m = np.floor_divide(a + 11*h + 22*l, 451)
    n = np.floor_divide(h + l - 7*m + 114, 31)
    o = (h + l - 7*m + 114) % 31
    return dt.date(year, n, o + 1)

def calculate_easter_monday(year, algorithm = calculate_easterA):
    easter = algorithm(year)
    if easter.day == 31:
        return dt.date(year, 4, 1)
    else:
        return easter + dt.timedelta(days=1)

# zielone świątki = wielkanoc + 49dni; i tak wypadają w niedziele zawsze
# boże ciało = wielkanoc + 60dni

def valid_dates(first_date, last_date):
    dates = pd.date_range(first_date, last_date, freq='d').to_list()
    old = 0
    print(len(dates))
    for date in dates:
        year = date.year
        month = date.month
        day = date.day
        dow = date.day_of_week
        if dow == 0: # sundays
            dates.remove(date)
            continue
        if month == 1: # new year, 3 kings
            if day == 1 or day == 6:
                dates.remove(date)
                continue
        if month == 5: # 1 may and 3 may
            if day == 1 or day == 3:
                dates.remove(date)
                continue
        if month == 8 and day == 15: # wniebowzięcie najświętszej Maryii panny
            dates.remove(date)
            continue
        if month == 11: # wszystkich swietych i dzien niepodleglosci
            if day == 1 or day == 11:
                dates.remove(date)
                continue
        if month == 12: # boże narodzenie
            if day == 25 or day == 26:
                dates.remove(date)
                continue

        if year != old:
            easter_monday = calculate_easter_monday(year)
            corpus_cristi = easter_monday + dt.timedelta(days=59)
            old = year
        if month == easter_monday.month and day == easter_monday.day:
            dates.remove(date)
            continue
        if month == corpus_cristi.month and day == corpus_cristi.day:
            dates.remove(date)
            continue

    return pd.DatetimeIndex(dates).strftime("%Y-%m-%d").to_numpy()
        

def random_transaction_dates(first_date, last_date, n):
    dates = valid_dates(first_date, last_date)
    return sorted(np.random.choice(dates, n))


if __name__ == "__main__":
    print(random_transaction_dates("2014-01-01", "2020-12-31", 2000))