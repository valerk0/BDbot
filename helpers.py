__author__ = 'Valery'
from confData import confData
import telegram

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