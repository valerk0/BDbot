__author__ = 'Valery'
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from helpers import private, RplMrkup, DayInterval, FirstDay, admin
from HandleDB import DB
from BDayObj import BDayObj
from datetime import datetime, date
import os
from random import randint
 

@private
def start(update, context):
    update.message.reply_text('Пожалуйста, задайте дату рождения в формате:\n/bday dd.mm.yyyy')
    print('start')

# @private
def help(update, context):
    print('help command')
    update.message.reply_text('''
        Бот поздравит Вас с днем рождения в чатах, которых вы состоите.
        \nПожалуйста, задайте дату рождения в формате:
        \n/bday dd.mm.yyyy
        \n\nПосмотреть чью-либо дату рождения:
        \n/get @username
        \nПосмотреть ближайшие дни рождения участников чата (максимум 10):
        \n/get10
        \nУдалить дату рождения из базы (только в личке):
        \n/del
        ''')
    print('help')
 
def setBDay(update, context):
    print('setBDay command')
    args = context.args
    try:
        datetime.strptime(args[0],'%d.%m.%Y')
    except:
        update.message.reply_text('''
            \u26D4 Неверный формат даты!
            \nПравильный формат:
            \n/bday dd.mm.yyyy
            ''')
        return
    bday = BDayObj(update.message.from_user)
    bday.SetDate(args[0])
    db = DB()
    db.SaveBDay(bday)
    update.message.reply_text('''\u270D Сохранил Вашу дату рождения ({}) '''.format(args[0]))
    print('saved bday ', args[0], ' of user @', update.message.from_user.username)
 
def getBDay(update, context):
    print('getBDay command')
    args = context.args
    try:
        UN = args[0].split('@')[1]
        print(UN)
    except:
        update.message.reply_text('''
            \u26D4 Неверный формат запроса!
            \nПравильный формат:
            \n/get @username
            ''')
        return
    db = DB()
    bday = db.getDateByUN(UN)
    if isinstance(bday,(date,datetime)):
        update.message.reply_text('Дата рождения пользователя @{} - {}'.
               format(UN,bday.strftime('%d.%m.%Y')), reply_markup=RplMrkup())
    else:
        update.message.reply_text(('Мне неизвестна дата рождения пользователя @{} \U0001F937'.
               format(UN)), reply_markup=RplMrkup())
    print('showed bday: @{} - {}'.format(UN,bday))   
 
def get10(update, context):
    print('get10 command')
    db = DB()
    ordered_bdays = db.get_ordered_bdays()
    nodata_txt = 'У меня нет данных о днях рождениях пользователей этого чата \U0001F937'
    if ordered_bdays and ordered_bdays[0]:
        cht_id = update.effective_chat.id
        context.bot.send_chat_action(cht_id, 'typing')
        cht_bdays = []
        for usr_bday in ordered_bdays:
            if is_usr_in_cht(context.bot, usr_bday[0], cht_id): 
                cht_bdays.append(usr_bday)
            if len(cht_bdays) >= 10: break
        txt='\U0001F4DD Ближайшие дни рождения:\n'
        for bday in cht_bdays:
            txt = (txt + '{} - {} {}\n'.
                format(date(bday[5], bday[4], bday[3]).strftime('%d.%m'), 
                bday[2] if bday[2] else '', '(@ '+bday[1]+')' if bday[1] else ''))
        if not cht_bdays:
            txt = nodata_txt
    else:
        txt = nodata_txt
    update.message.reply_text(txt, reply_markup=RplMrkup())
    print(txt)
 
def is_usr_in_cht(bot, usr_id, cht_id):
    cht_member = None
    try:
        cht_member = bot.get_chat_member(cht_id, usr_id)
    except:
        return False
    if cht_member and cht_member.status not in ['left', 'kicked']: return True
    return False
 
def is_usr_not_in_cht(bot, usr_id, cht_id):
    cht_member = None
    try:
        cht_member = bot.get_chat_member(cht_id, usr_id)
    except:
        return False
    if cht_member and cht_member.status in ['left', 'kicked']: return True
    return False
 
def stat(update, context):
    print('stat command')
    db = DB()
    sDic = db.stat()
    update.message.reply_text('''Всего чатов: {}
        \nВсего дней рождений: {}'''.
        format(sDic['allChats'], sDic['allBDays']), reply_markup=RplMrkup())
 
@private
def delBDay(update, context):
    print('delBDay command')
    db = DB()
    if db.del_bday(update):
        update.message.reply_text('Дата рождения пользователя @{} удалена из базы'.
                        format(update.effective_user.username))
    else:
        update.message.reply_text('Пользователь @{} не записан в базу'.
                        format(update.effective_user.username))
    print('del @{}'.format(update.effective_user.username))
 
@admin
def chatlist(update, context):
    print('chatlist command')
    db = DB()
    chts = db.get_chat_list()
    if not chts: return
    txt = 'Количество чатов: {}'.format(len(chts))
    for cht in chts:
        txt += '\n{}: {}'.format(cht[0], cht[1])
    update.message.reply_text(txt)

@admin
def delleftchats(update, context):
    print('delleftchats command')
    del_left_chats(context)

def del_left_chats(context):
    db = DB()
    chts = db.get_chat_list()
    for cht in chts:
        if is_usr_not_in_cht(context.bot, 607758927, cht[0]):
            db.del_cht(cht[0])

def ProcessMsg(update, context):
    db = DB()
    db.HandleMsg(update)
    print('updated/save data of @', update.effective_user.username, ' for chat ', update.effective_chat.title)

def DaylyJob(context):
    bot = context.bot
    db = DB()
    usrsList = db.GetUserBDayList()
    chtsList = db.GetChatsList()
    emoji = ['\U0001F490', '\U0001F382', '\U0001F388', '\U0001F389', '\U0001F38A', '\U0001F381']
    for usr in usrsList:
        for cht in chtsList:
            if not is_usr_in_cht(bot, usr[0], cht[0]): continue
            uname = usr[2]
            uuname = '(@' + usr[1] + ')' if usr[1] else ''
            msg = ('Поздравляем с днем рождения пользователя {} {}\nУра! {}'
                        .format(uname, uuname, emoji[randint(0, 5)]))
            bot.send_message(cht[0], msg, reply_markup=RplMrkup())

def main():
    print('start program') 

    updater = Updater(os.environ['TOKEN'])
    dp = updater.dispatcher
    jq = updater.job_queue 

    dp.add_handler(MessageHandler(None, ProcessMsg),0)
    dp.add_handler(CommandHandler('start', start), 1)
    dp.add_handler(CommandHandler('help', help), 1)
    dp.add_handler(CommandHandler('bday', setBDay, pass_args=True), 1)
    dp.add_handler(CommandHandler('get', getBDay, pass_args=True), 1)
    dp.add_handler(CommandHandler('get10', get10), 1)
    dp.add_handler(CommandHandler('stat', stat), 1)
    dp.add_handler(CommandHandler('del', delBDay), 1)
    dp.add_handler(CommandHandler('chatlist', chatlist), 1)
    dp.add_handler(CommandHandler('delleftchats', delleftchats), 1)
    print('handlers added') 

    dJob = jq.run_repeating(DaylyJob, DayInterval(), FirstDay())
    print('jobs added') 

    updater.start_polling()
    updater.idle()
    print('exit program') 

main()
