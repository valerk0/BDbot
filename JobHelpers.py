__author__ = 'Valery'

import datetime

def DayInterval():
    return datetime.timedelta(days=1)

def FirstDay():
    CurTime=datetime.datetime.utcnow()
    TargetTime=datetime.datetime(CurTime.year,CurTime.month,CurTime.day,6)
    if ~CurTime.hour<6:
        TargetTime=TargetTime+datetime.timedelta(days=1)
    return datetime.timedelta(TargetTime-CurTime)

def NextMonth():
    CurTime=datetime.datetime.utcnow()
    TargetTime=datetime.datetime(CurTime.year,CurTime.month,1,6)
    if ~(CurTime.hour<6&CurTime.day==1):
        if CurTime.month==12:
            TargetTime=datetime.datetime(CurTime.year+1,1,1,6)
        else:
            TargetTime=datetime.datetime(CurTime.year,CurTime.month+1,1,6)
    return datetime.timedelta(TargetTime-CurTime)