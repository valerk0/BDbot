__author__ = 'Valery'
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from JobHelpers import DayInterval, FirstDay, NextMonth
from confData import confData
from helpers import private
from HandleDB import DB
from BDayObj import BDayObj
from emoji import emojize
import re
from datetime import datetime

@private
def start(bot, update):
    update.message.reply_text('Пожалуйста, задайте дату рождения в формате:\n/bday dd.mm.yyyy')
    print('start')

@private
def help(bot, update):
    update.message.reply_text(emojize('''
    Бот поздравит Вас с днем рождения:bouquet: в чатах, которых вы состоите.\n\n
    Пожалуйста, задайте дату рождения в формате:\n
    /bday dd.mm.yyyy
    '''))
    print('help')

def setBDay(bot, update, args):
    form=re.compile('^\d{1,2}\.\d{1,2}\.\d{4}$')
    WrongDate=False
    if ~form.match(args[0])==None:
        WrongDate=True
    else:
        try:
            datetime.strptime(args[0],'%d.%m.%Y')
        except:
            WrongDate=True
    if WrongDate:
        update.message.reply_text(emojize('''
        Неверный формат даты!:see-no-evil monkey:\n
        Правильный формат:\n
        /bday dd.mm.yyyy
        '''))
        print('bday fail')
        return
    bday=BDayObj(update.message.from_user)
    bday.SetDate(args[0])
    db=DB()
    db.SaveBDay(bday)
    update.message.reply_text(emojize('''Сохранил Вашу дату рождения({}) :thumbs up:'''.format(args[0])))
    print('bday success')

def ProcessMsg(bot, update):
    db=DB()
    db.HandleMsg(update)
    print('process msg')

def DaylyJob(bot, job):
    pass

def MonthlyJob(bot, job):
    pass

def main():
    print('start program')
    conf=confData('botconf.ini','BOT')

    updater=Updater(**conf.params)
    dp=updater.dispatcher
    jq=updater.job_queue

    dp.add_handler(MessageHandler(~Filters.status_update, ProcessMsg),0)
    dp.add_handler(CommandHandler('start', start),1)
    dp.add_handler(CommandHandler('help', help),1)
    dp.add_handler(CommandHandler('bday', setBDay, pass_args=True),1)
    print('handlers added')

    dJob=jq.run_repeating(DaylyJob, DayInterval(), FirstDay())
    mJob=jq.run_once(MonthlyJob, NextMonth())
    print('jobs added')

    updater.start_polling()
    updater.idle()
    print('-1')

main()