__author__ = 'Valery'
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from JobHelpers import DayInterval, FirstDay, NextMonth
from confData import confData
from helpers import private
from HandleDB import DB
from BDayObj import BDayObj
from emoji import emojize

@private
def start(bot, update):
    update.message.reply_text('Пожалуйста, задайте дату рождения в формате:\n/bday dd.mm.yyyy')

@private
def help(bot, update):
    update.message.reply_text(emojize('''
        Бот поздравит Вас с днем рождения:bouquet: в чатах, которых вы состоите.\n\n
        Пожалуйста, задайте дату рождения в формате:\n
        /bday dd.mm.yyyy
        '''))

def setBDay(bot, update, args):
    if ~len(args)==1|(len(args)==1&~len(args[0].split('.'))==3):
        update.message.reply_text(emojize('''
            Неверный формат даты!:see-no-evil monkey:\n
            Правильный формат:\n
            /bday dd.mm.yyyy
            '''))
        return
    bday=BDayObj(update.message.from_user)
    bday.SetDate(args[0])
    db=DB()
    db.SaveBDay(bday)
    update.message.reply_text(emojize('Сохранил:thumbs up:'))

def ProcessMsg(bot, update):
    db=DB()
    db.HandleMsg(update)

def DaylyJob(bot, job):
    pass

def MonthlyJob(bot, job):
    pass

def main():
    conf=confData('botconf.ini','BOT')

    updater=Updater(**conf.params)
    dp=updater.dispatcher
    jq=updater.job_queue

    dp.add_handler(MessageHandler(~Filters.status_update, ProcessMsg),0)
    dp.add_handler(CommandHandler('start', start),1)
    dp.add_handler(CommandHandler('help', help),1)
    dp.add_handler(CommandHandler('bday', setBDay, pass_args=True),1)

    dJob=jq.run_repeating(DaylyJob, DayInterval, FirstDay)
    mJob=jq.run_once(MonthlyJob, NextMonth)

    updater.start_polling()
    updater.idle()

