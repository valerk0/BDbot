__author__ = 'Valery'
import telegram, datetime, os

def private(func):
    def wrapped(update, context, *args, **kwargs):
        if update.message.chat.type == 'private':
            return func(update, context, *args, **kwargs)
        return
    return wrapped

def RplMrkup():
    BT = telegram.InlineKeyboardButton('Задать дату рождения',
        url='https://t.me/{0:s}?start'.format(os.environ['USERNAME']))
    RM = telegram.InlineKeyboardMarkup([[BT]])
    return RM

def DayInterval():
    return datetime.timedelta(days=1)

def FirstDay():
    CurTime = datetime.datetime.utcnow()
    TargetTime = datetime.datetime(CurTime.year, CurTime.month, CurTime.day, 6)
    if not CurTime.hour < 6:
        TargetTime = TargetTime+datetime.timedelta(days=1)
    return TargetTime - CurTime

def NextMonth():
    CurTime = datetime.datetime.utcnow()
    TargetTime = datetime.datetime(CurTime.year,CurTime.month, 1, 6)
    if not (CurTime.hour < 6 and CurTime.day == 1):
        if CurTime.month == 12:
            TargetTime = datetime.datetime(CurTime.year+1, 1, 1, 6)
        else:
            TargetTime = datetime.datetime(CurTime.year,CurTime.month+1, 1, 6)
    return TargetTime - CurTime
