# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------------------------
  Written by      : Rob Lewis

  Date            : 11SEP2025

  Purpose         : Create version of SAS intnx function, moving date through set period

  Dependencies    :

  Module name    : intnx

  Modifications
  -------------
  11SEP2025   RLEWIS  Initial Version
----------------------------------------------------------------------------------------------------------------------:
"""

# ---------------
# --- Imports ---
# ---------------

from globals import *

# -----------------
# --- Functions ---
# -----------------

def intnx(unit, date_series, value, position):
    if any(type(var) == pd.Series for var in [date_series]):
        return intnx_vectorised(unit, date_series, value, position)
       
    else:
        return intnx_per_row(unit, date_series, value, position)

def intnx_vectorised(unit, date_series, value, position):
    date_series = date_series.astype('datetime64[ns]')  # Cast to datetime

    if unit == 'day':
        result_date = date_series + pd.to_timedelta(value, unit='D')
    elif unit == 'week':
        if position == 'same':
            result_date = date_series + pd.to_timedelta(value, unit='W')
        else:
            if (date_series.dt.weekday == 6).any(): # Sunday points to Monday
                date_series = date_series + pd.to_timedelta(1, unit='D')
            result_date = date_series + pd.to_timedelta(value, unit='W')

        if position == 'beginning':
            result_date -= pd.to_timedelta(result_date.dt.weekday, unit='D')
        elif position == 'end':
            result_date += pd.to_timedelta(6 - result_date.dt.weekday, unit='D')
    elif unit == 'month':
        if type(value) == pd.Series and value.size == date_series.size:
            total_months = date_series.dt.year * 12 + date_series.dt.month
            adjusted_months = total_months + value - 1
           
            prep = pd.DataFrame()
            prep['year'] = np.floor(adjusted_months/12).astype(int)
            prep['month'] = (adjusted_months + 1 - prep['year'] * 12).astype(int)
            prep['day'] = date_series.dt.day

            stage = pd.DataFrame()
            stage['result_date'] = pd.to_datetime(prep[['year', 'month', 'day']], errors="coerce")

            prep['day'] = 1
            stage['max_days'] = pd.to_datetime(prep[['year', 'month', 'day']], errors="coerce")
            stage['max_days'] += pd.DateOffset(days=31)
            stage['max_days'] -= pd.to_timedelta(stage['max_days'].dt.day, unit = 'D')
            stage['result_date'] = stage['result_date'].fillna(stage['max_days'])
            result_date = stage['result_date']

        elif type(value) == int:
            result_date = date_series + pd.DateOffset(months=value)
        else:
            raise Exception("Value not int or series of matching length")


        if position == 'beginning':
            result_date = pd.to_datetime(result_date.dt.strftime('%Y-%m-01'))
        elif position == 'end':
            result_date += pd.offsets.MonthEnd(0)

    elif unit == 'year':
        if type(value) == pd.Series and value.size == date_series.size:
            total_months = date_series.dt.year * 12 + date_series.dt.month
            adjusted_months = total_months + (value * 12) - 1
           
            prep = pd.DataFrame()
            prep['year'] = np.floor(adjusted_months/12).astype(int)
            prep['month'] = (adjusted_months + 1 - prep['year'] * 12).astype(int)
            prep['day'] = date_series.dt.day

            stage = pd.DataFrame()
            stage['result_date'] = pd.to_datetime(prep[['year', 'month', 'day']], errors="coerce")

            prep['day'] = 1
            stage['max_days'] = pd.to_datetime(prep[['year', 'month', 'day']], errors="coerce")
            stage['max_days'] += pd.DateOffset(days=31)
            stage['max_days'] -= pd.to_timedelta(stage['max_days'].dt.day, unit = 'D')
            stage['result_date'] = stage['result_date'].fillna(stage['max_days'])
            result_date = stage['result_date']

        elif type(value) == int:
            result_date = date_series + pd.DateOffset(years=value)
        else:
            raise Exception("Value not int or series of matching length")

        if position == 'beginning':
            result_date = pd.to_datetime(result_date.dt.strftime('%Y-01-01'))
        elif position == 'end':
            result_date += pd.DateOffset(years=1)
            result_date = result_date - pd.to_timedelta(result_date.dt.dayofyear, unit='D')
   
    result_date = result_date.astype('date32[pyarrow]')

    return result_date

def intnx_per_row(unit, date, value, position):
    if pd.isnull(date):
        return np.nan

    if unit == 'day':
        return date + timedelta(days=value)
    elif unit == 'week':
        if position == 'same':
            moved_date = date + relativedelta(weeks=value)
        else:
            if date.weekday() == 6:
                date = date + timedelta(days=1)
            moved_date = date + relativedelta(weeks=value)
        if position == 'beginning':
            return moved_date - timedelta(days=moved_date.weekday())
        elif position == 'end':
            return moved_date + timedelta(days=(6 - moved_date.weekday()))
        elif position == 'same':
            return moved_date
    elif unit == 'month':
        moved_date = date + relativedelta(months=value)
        if position == 'beginning':
            return moved_date.replace(day=1)
        elif position == 'end':
            next_month = moved_date.replace(day=28) + timedelta(days=4)
            return next_month - timedelta(days=next_month.day)
        elif position == 'same':
            if date.day > 28:
                # Handle cases where the original date is in the last week of the month
                return moved_date.replace(day=28) + timedelta(days=date.day - 28)
            else:
                return moved_date.replace(day=date.day)
    elif unit == 'year':
        moved_date = date + relativedelta(years=value)
        if position == 'beginning':
            return moved_date.replace(month=1, day=1)
        elif position == 'end':
            next_month = moved_date.replace(month=12, day=28) + timedelta(days=4)
            return next_month - timedelta(days=next_month.day)
        elif position == 'same':
            return moved_date.replace(month=date.month, day=date.day)