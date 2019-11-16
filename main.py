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

# @private
def help(bot, update):
    update.message.reply_text(emojize('''
        Бот поздравит Вас с днем рождения:bouquet: в чатах, которых вы состоите.
        \nПожалуйста, задайте дату рождения в формате:
        \n/bday dd.mm.yyyy
        \n\nПосмотреть чью-либо дату рождения:
        \n/get @username
        \nПосмотреть ближайшие дни рождения участников чата (максимум 10):
        \n/get10 
        \nУдалить дату рождения из базы (только в личке):
        \n/del
        '''))
    print('help')

def setBDay(bot, update, args):
    try:
        datetime.strptime(args[0],'%d.%m.%Y')
    except:
        update.message.reply_text(emojize('''
            Неверный формат даты!
            \nПравильный формат:
            \n/bday dd.mm.yyyy
            '''))
        return
    bday=BDayObj(update.message.from_user)
    bday.SetDate(args[0])
    db=DB()
    db.SaveBDay(bday)
    update.message.reply_text(emojize(''':memo: Сохранил Вашу дату рождения ({}) '''.format(args[0])))
    print('saved bday ', args[0], ' of user @', update.message.from_user.username)

def getBDay(bot,update,args):
    try:
        UN=args[0].split('@')[1]
        print(UN)
    except:
        update.message.reply_text(emojize('''
            :no_entry_sign: Неверный формат запроса!
            \nПравильный формат:
            \n/get @username
            '''))
        return
    db=DB()
    bday=db.getDateByUN(UN)
    if isinstance(bday,(date,datetime)):
        update.message.reply_text(emojize('Дата рождения пользователя @{} - {}'.
        	format(UN,bday.strftime('%d.%m.%Y'))), reply_markup=RplMrkup())
    else:
        update.message.reply_text(emojize('Мне неизвестна дата рождения пользователя @{}'.
        	format(UN)), reply_markup=RplMrkup())
    print('showed bday: @{} - {}'.format(UN,bday))    

def get10(bot,update):
	db=DB()
        bot.send_message('@BabaR0bot', 'get10')
	usrs=db.get10(update)
	if usrs:
		txt='Ближайшие дни рождения:\n'
		for n,x in usrs:
			txt=txt+'{} - {} {} {}\n'.\
                format(date(x.bday[0].by, x.bday[0].bm, x.bday[0].bd).strftime('%d.%m'), \
                    x.name, x.lname if x.lname else '', '(@ '+x.uname+')' if x.uname else '')
	else:
		txt=emojize('У меня нет данных о днях рождениях пользователей этого чата')
	update.message.reply_text(txt, reply_markup=RplMrkup())
	print(txt)

def stat(bot,update):
    db=DB()
    sDic=db.stat(update)
    update.message.reply_text(emojize('''Статистика чата "{}":
        \nИзвестных пользователей чата: {}
        \nИзвестных дней рождений чата: {}
        \n\nВсего чатов: {}
        \nВсего пользователей: {}
        \nВсего дней рождений: {}'''.
        format(update.effective_chat.title, sDic['chatUsers'], sDic['chatBDays'], sDic['allChats'], \
            sDic['allUsers'], sDic['allBDays'])), reply_markup=RplMrkup())

@private
def delBDay(bot, update):
    db=DB()
    if db.delBDay(update):
    	update.message.reply_text(emojize('Дата рождения пользователя @{} удалена из базы'.
    		format(update.effective_user.username)))
    else:
    	update.message.reply_text(emojize('Пользователь @{} не записан в базу'.
    		format(update.effective_user.username)))
    print('del @{}'.format(update.effective_user.username))

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
        for cht in usr.chat:
            uname=usr.name if not usr.name==None else ''
            ulname=usr.lname if not usr.lname==None else ''
            uuname='(@' + usr.uname + ')' if not usr.uname==None else ''
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
    dp.add_handler(CommandHandler('get10', get10),1)
    dp.add_handler(CommandHandler('stat', stat),1)
    dp.add_handler(CommandHandler('del', delBDay),1)
    print('handlers added')

    dJob=jq.run_repeating(DaylyJob, DayInterval(), FirstDay())
    print('jobs added')

    updater.start_polling()
    updater.idle()
    print('exit program')

main()
