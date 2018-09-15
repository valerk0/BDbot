__author__ = 'Valery'
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from confData import confData
from helpers import private, RplMrkup, DayInterval, FirstDay
from HandleORM import DB
# from HandleDB import DB
from BDayObj import BDayObj
from emoji import emojize
from datetime import datetime, date

@private
def start(bot, update):
    update.message.reply_text('Пожалуйста, задайте дату рождения в формате:\n/bday dd.mm.yyyy')
    print('start')

@private
def help(bot, update):
    update.message.reply_text(emojize('''
        Бот поздравит Вас с днем рождения:bouquet: в чатах, которых вы состоите.
        \n\nПожалуйста, задайте дату рождения в формате:
        \n/bday dd.mm.yyyy
        \n\nПосмотреть чью-либо дату рождения можно командой:
        \n/get @username
        '''))
    print('help')

def setBDay(bot, update, args):
    try:
        datetime.strptime(args[0],'%d.%m.%Y')
    except:
        update.message.reply_text('''
            Неверный формат даты!
            \nПравильный формат:
            \n/bday dd.mm.yyyy
            ''')
        return
    bday=BDayObj(update.message.from_user)
    bday.SetDate(args[0])
    db=DB()
    db.SaveBDay(bday)
    update.message.reply_text('''Сохранил Вашу дату рождения ({}) '''.format(args[0]))
    print('saved bday ', args[0], ' of user @', update.message.from_user.username)

def getBDay(bot,update,args):
    try:
        UN=args[0].split('@')[1]
        print(UN)
    except:
        update.message.reply_text('''
            Неверный формат запроса!
            \nПравильный формат:
            \n/get @username
            ''')
        return
    db=DB()
    bday=db.getDateByUN(UN)
    if isinstance(bday,(date,datetime)):
        update.message.reply_text('Дата рождения пользователя @{} - {}'.format(UN,bday.strftime('%d.%m.%Y')), reply_markup=RplMrkup())
    else:
        update.message.reply_text('Мне неизвестна дата рождения пользователя @{}'.format(UN), reply_markup=RplMrkup())
    print('showed bday: @{} - {}'.format(UN,bday))    

def ProcessMsg(bot, update):
    db=DB()
    db.HandleMsg(update)
    print('updated/save data of @', update.effective_user.username, ' for chat ', update.effective_chat.title)

# def DaylyJob(bot, job):
#     db=DB()
#     userList=db.GetUserBDayList()
#     if len(userList)<1:
#         return
#     chatsList=db.GetChatsList(userList)
#     if len(chatsList)<1:
#         return
#     for user, chats in zip(userList, chatsList):
#         for chat in chats:
#             msg=emojize('Поздравляем с днем рождения пользователя {} (@{})\nУра! :bouquet:'.format(user[2],user[1]))
#             bot.send_message(chat, msg, reply_markup=RplMrkup())

def DaylyJob(bot, job):
    db=DB()
    usersList=db.getUsersBDay()
    for usr in usersList:
        print(usr.name)
        for cht in usr.chat:
            print(cht.name)
            uname=usr.name if not usr.name=='None' else ''
            ulname=usr.lname if not usr.lname=='None' else ''
            uuname='(@' + usr.uname + ')' if not usr.uname=='None' else ''
            msg=emojize('Поздравляем с днем рождения пользователя {} {} {}\nУра! :bouquet:'
                        .format(uname, ulname, uuname))
            bot.send_message(cht.id, msg, reply_markup=RplMrkup())


def main():
    print('start program')
    conf=confData('botconf.ini','BOT')

    updater=Updater(conf.params['token'])
    dp=updater.dispatcher
    jq=updater.job_queue

    dp.add_handler(MessageHandler(not Filters.status_update, ProcessMsg),0)
    dp.add_handler(CommandHandler('start', start),1)
    dp.add_handler(CommandHandler('help', help),1)
    dp.add_handler(CommandHandler('bday', setBDay, pass_args=True),1)
    dp.add_handler(CommandHandler('get', getBDay, pass_args=True),1)
    print('handlers added')

    dJob=jq.run_repeating(DaylyJob, DayInterval(), FirstDay())
    print('jobs added')

    updater.start_polling()
    updater.idle()
    print('exit program')

print('before main')
main()