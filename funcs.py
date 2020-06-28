#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from datetime import timedelta, datetime

# transpose
def T(rows_or_cols): return list(zip(*rows_or_cols))

def period_to_hours_minutes(period):
    # 1 -> 0, 30
    # 2 -> 1, 0
    # 48 -> 24, 0
    assert 1 <= period <= 48
    assert int(period) == period
    return period // 2, (period % 2) * 30
    
assert period_to_hours_minutes(1) == (0, 30)
assert period_to_hours_minutes(2) == (1, 0)
assert period_to_hours_minutes(3) == (1, 30)
assert period_to_hours_minutes(48) == (24, 0)


def hours_minutes_to_time(hm):
    # (hours, minutes) -> "hours:minutes:00"
    # (0, 30) -> "00:30:00"
    hours, minutes = hm
    return f"{hours:02}:{minutes:02}:00"
    
assert hours_minutes_to_time((0, 30)) == '00:30:00'
assert hours_minutes_to_time((5, 30)) == '05:30:00'
assert hours_minutes_to_time((23, 0)) == '23:00:00'


def period_to_time(period): 
    return hours_minutes_to_time(period_to_hours_minutes(period))
    
assert period_to_time(1) == '00:30:00'
assert period_to_time(11) == '05:30:00'
assert period_to_time(48) == '24:00:00'





MIN_DATE = datetime(2020, 1, 1)



# Convenience method to get date from date time
def S(dt): return str(dt.date())

def AssertException(exc, f, *args, **kwargs):
    try:
        f(*args, **kwargs)
    except exc:
        return True
    
    return False


def validate_date(d):
    try:
        year, month, day = map(int, d.split("-"))
    except ValueError:
        raise ValueError(f'Erroneous Date "{d}" must be of the format yyyy-mm-dd')
    date = datetime(year, month, day)
    
    if MIN_DATE - timedelta(days=1) >= date:
        raise ValueError(f'We only accept dates from {MIN_DATE}. You asked for {date}')
        
    if date >= datetime.now():
        raise ValueError(f'We do not accept future dates. You asked for {date}')
        
        
    return date


def get_dates_between(start, end=datetime.now()):
    
    while start <= end:
        yield S(start)
        start += timedelta(days=1)
        
        

def get_dates_from_strings(start, end=None):
    
    start = validate_date(start)
    
    if not end:
        return get_dates_between(start)
    
    
    end = validate_date(end)
    
    if start > end: 
        start, end = end, start
        
    return get_dates_between(start, end)


def generate_df(dates, period=48):

    date, time, period = T(
        [
            (date, period_to_time(i), i)
            for date in dates
            for i in range(1, period+1)
        ]
    ) 


    return pd.DataFrame(data={
        "Date": date,
        "Time": time,
        "Period": period,
    })



def get_json_from_strings(start, end=None, period=48):

    try:
    
        dates = get_dates_from_strings(start, end)
        df = generate_df(dates, period)
        
        data = [
            {
                key: row[key]
                for key in df
            }

            for _, row in df.iterrows()
        ]
        
    except ValueError as ve:
        return str(ve)
    
    return data









