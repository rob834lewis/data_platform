# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------------------------
  Written by      : Rob Lewis

  Date            : 11SEP2025

  Purpose         : Create working day variables

  Dependencies    :

  Module name    : wdays

  Modifications
  -------------
  11SEP2025   RLEWIS  Initial Version
----------------------------------------------------------------------------------------------------------------------:
"""

# ---------------
# --- Imports ---
# ---------------

from globals import *
from .bank_hol   import bank_hol
from .intnx      import intnx

# ----------------
# --- Function ---
# ----------------

def wdays(seeddate=None,prt="No"):

    # set seeddate to current day if blank
    if not seeddate:
        seeddate = datetime.now().date()
   
    # ----------------------------------------------------
    # --- Working with Seeddate being day passed / today
    # ----------------------------------------------------

    xrun_date = seeddate - timedelta(days=1) # previous day

    today = seeddate.strftime('%Y%m%d') # today in yyyymmdd format
    todays_date = seeddate # today variable stored
    is_bank_hol = bank_hol(todays_date) # flag if today is a bank holiday

    if seeddate.weekday() == 0: # If Monday
        yesterday = xrun_date - timedelta(days=2)
        is_yesterday_bank_hol = bank_hol(yesterday)
        monday = "Y" # is it Monday?
        wrun_date = seeddate # start of week
    else: # If not Monday
        yesterday = xrun_date  
        is_yesterday_bank_hol = bank_hol(yesterday)
        monday = "N" # is it Monday?
        wrun_date = seeddate - timedelta(days=seeddate.weekday()) # start of week

    while (bank_hol(yesterday) == "Y") | (yesterday.weekday() in (5,6)):
        yesterday = yesterday - timedelta(days=1)
       
    next_date = yesterday + timedelta(days=1)
    while (next_date.weekday() in (5,6)):
        next_date = next_date + timedelta(days=1)  

    previousday = yesterday - timedelta(days=1)
    while (bank_hol(previousday) == "Y") | (previousday.weekday() in (5,6)):
        previousday = previousday - timedelta(days=1)

    yesterdays_date = yesterday    
    yesterday       = yesterday.strftime('%Y%m%d')
    previousday     = previousday.strftime('%Y%m%d')

    # ------------------------------------------------------
    # --- Working with Seeddate being previous working day
    # ------------------------------------------------------

    # update seeddate to 'yesterday'
    seeddate = seeddate - timedelta(days=1)

    # find last non Saturday/Sunday/Bank Holiday
    done = 0

    while done == 0:
        if seeddate.weekday() >= 0 and seeddate.weekday() <= 4 and bank_hol(seeddate) == 'N':
            done = 1
        else:
            seeddate = seeddate - timedelta(days=1)

    # beginning of run month
    strt = intnx('month',seeddate,0,'beginning')
   
    # end of run month
    end = intnx('month',seeddate,0,'end')

    # ------------------------------------------------------
    # --- Initial Date Variables
    # ------------------------------------------------------

    # Daily

    # store rundate variable
    rundate = seeddate
    # date variables for use in reporting output
    monyr  = seeddate.strftime("%b %Y")
    rptdat = seeddate.strftime("%d%b%Y").upper()

    # Yearly

    # beginning of year variable
    runyr = intnx('year',seeddate,0,'beginning')

    # Monthly

    runmth       = intnx('month',seeddate,0,'beginning')
    runmthsql    = "'" + runmth.strftime("%Y-%m-%d") + "'"
    runmthdsn    = runmth.strftime("%Y%m") # this was curmon in SAS world
    runmthend    = intnx('month',seeddate,0,'end')
    runmthendsql = "'" + runmthend.strftime("%Y-%m-%d") + "'"
    nextmth      = intnx('month',seeddate,1,'beginning')
    nextmthsql   = "'" + nextmth.strftime("%Y-%m-%d") + "'"
    nextmthdsn   = nextmth.strftime("%Y%m%d")
    nextmthend   = intnx('month',seeddate,1,'end')

    # Weekly

    runweek     = intnx('week',seeddate,0,'beginning')
    runweeksql  = "'" + runweek.strftime("%Y-%m-%d") + "'"
    runweekdat  = runweek.strftime("%d%b%Y").upper()
    runweekdsn  = runweek.strftime("%Y%m%d")
    nextweek    = intnx('week',seeddate,1,'beginning')
    nextweeksql = "'" + nextweek.strftime("%Y-%m-%d") + "'"
    nextweekdat = nextweek.strftime("%d%b%Y").upper() # this was wrptdat in SAS world
    nextweekdsn = nextweek.strftime("%Y%m%d")

    # ------------------------------------------------------
    # --- Loop back through x iterations
    # ------------------------------------------------------
       
    # Monthly
    dict={}
    for k in range(16):
        key1 = str("runmth"+str(k))
        key2 = str("runmthsql"+str(k))
        key3 = str("runmthend"+str(k))
        key4 = str("runmthendsql"+str(k))
        key5 = str("runweek"+str(k))
        key6 = str("runweeksql"+str(k))
        key7 = str("runweekdat"+str(k))
        key8 = str("runweekdsn"+str(k))
        key9 = str("runmthdsn"+str(k))
        value1 = intnx('month',seeddate,-k,'beginning')
        value2 = intnx('month',seeddate,-k,'end')
        value3 = intnx('week',seeddate,-k,'beginning')
        dict_val1 = value1
        dict_val2 = "'" + str(value1) + "'"
        dict_val3 = value2
        dict_val4 = "'" + str(value2) + "'"
        dict_val5 = value3
        dict_val6 = "'" + str(value3) + "'"
        dict_val7 = value3.strftime("%d%b%Y").upper()
        dict_val8 = value3.strftime("%Y%m%d")
        dict_val9 = value1.strftime("%Y%m")
        dict[key1]=dict_val1
        dict[key2]=dict_val2
        dict[key3]=dict_val3
        dict[key4]=dict_val4
        dict[key5]=dict_val5
        dict[key6]=dict_val6
        dict[key7]=dict_val7
        dict[key8]=dict_val8
        dict[key9]=dict_val9

    # working days in month calculation
    date_in_month = strt
    firstday      = strt
    lastday       = strt
    m             = 0
    while date_in_month <= end:
        if date_in_month.weekday() >= 0 and date_in_month.weekday() <= 4 and bank_hol(date_in_month) == 'N':
            if m == 0:
                firstday = date_in_month
            lastday = date_in_month
            m+=1
        date_in_month = date_in_month + timedelta(days=1)
       
    #global eom, fnam, fnamlast, fnamst

    eom = 'N'
    if lastday == seeddate:
        eom = 'Y'

    fnam = seeddate.strftime("%Y%m%d")

    # find last non Saturday/Sunday/Bank Holiday
    ldone = 0
    lastrd = seeddate - timedelta(days=1)

    while ldone == 0:
        if lastrd.weekday() >= 0 and lastrd.weekday() <= 4 and bank_hol(lastrd) == 'N':
            ldone = 1
        else:
            lastrd = lastrd - timedelta(days=1)

    fnamlast = lastrd.strftime("%Y%m%d")
    fnamst   = firstday.strftime("%Y%m%d")

    reutrn_dict = {'today':today, 'todays_date':todays_date, 'yesterday':yesterday, 'yesterdays_date':yesterdays_date, 'next_date':next_date, 'previousday':previousday, 'xrun_date':xrun_date, 'wrun_date':wrun_date,
            'monday':monday, 'is_bank_hol':is_bank_hol, 'is_yesterday_bank_hol':is_yesterday_bank_hol, 'rundate':rundate, 'monyr':monyr, 'rptdat':rptdat, 'runyr':runyr, 'runmth':runmth,
            'runmthsql':runmthsql, 'runmthdsn':runmthdsn, 'runmthend':runmthend, 'runmthendsql':runmthendsql, 'nextmth':nextmth, 'nextmthsql':nextmthsql, 'nextmthdsn':nextmthdsn, 'nextmthend':nextmthend,
            'runweek':runweek, 'runweeksql':runweeksql, 'runweekdat':runweekdat, 'runweekdsn':runweekdsn, 'nextweek':nextweek, 'nextweeksql':nextweeksql, 'nextweekdsn':nextweekdsn, 'nextweekdat':nextweekdat,
            'eom':eom, 'fnam':fnam, 'fnamlast':fnamlast, 'fnamst':fnamst}
   
    reutrn_dict.update(dict)

    return reutrn_dict