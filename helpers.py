__author__ = 'Valery'
from confData import confData
import telegram, datetime

def private(func):
    def wrapped(bot,update, *args, **kwargs):
        if update.message.chat.type=='private':
            return func(bot,update, *args, **kwargs)
        return
    return wrapped

def RplMrkup():
    conf=confData('botconf.ini','BOT')
    BT=telegram.InlineKeyboardButton('Задать дату рождения',url='https://t.me/{0:s}?start'.format(conf.params['username']))
    RM=telegram.InlineKeyboardMarkup([[BT]])
    return RM

def DayInterval():
    return datetime.timedelta(days=1)

def FirstDay():
    CurTime=datetime.datetime.utcnow()
    TargetTime=datetime.datetime(CurTime.year,CurTime.month,CurTime.day,6)
    if ~CurTime.hour<6:
        TargetTime=TargetTime+datetime.timedelta(days=1)
    return TargetTime-CurTime

def NextMonth():
    CurTime=datetime.datetime.utcnow()
    TargetTime=datetime.datetime(CurTime.year,CurTime.month,1,6)
    if ~(CurTime.hour<6&CurTime.day==1):
        if CurTime.month==12:
            TargetTime=datetime.datetime(CurTime.year+1,1,1,6)
        else:
            TargetTime=datetime.datetime(CurTime.year,CurTime.month+1,1,6)
    return TargetTime-CurTime