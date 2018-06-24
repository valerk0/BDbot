__author__ = 'Valery'
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from JobHelpers import DayInterval, FirstDay, NextMonth
from confData import confData

def start(bot, update):
    update.message.reply_text('Пожалуйста, задайте дату рождения в формате:\n/bday dd.mm.yyyy')

def setBDay(bot, update, args):
    pass

def ProcessMsg(bot, update):
    pass

def DaylyJob(bot, job):
    pass

def MonthlyJob(bot, job):
    pass

def main():
    conf=confData('botconf.ini','BOT')

    updater=Updater(**conf.params)
    dp=updater.dispatcher
    jq=updater.job_queue

    dp.add_handler(MessageHandler(~Filters.status_update, ProcessMsg))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('bday', setBDay, pass_args=True))

    dJob=jq.run_repeating(DaylyJob, DayInterval, FirstDay)
    mJob=jq.run_once(MonthlyJob, NextMonth)

    updater.start_polling()
    updater.idle()

