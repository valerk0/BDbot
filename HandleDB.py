__author__ = 'Valery'

import psycopg2, datetime
from confData import confData

class DB(object):

    def __init__(self):
        conf=confData('dbconfig.ini','DATABASE')
        self.__conn=psycopg2.connect(**conf.params)

    def __del__(self):
        self.__conn.close()


    def HandleMsg(self,upd):
        usr=upd.effective_user
        cht=upd.effective_chat

        with self.__conn as conn:
            with conn.cursor() as curs:
                print('''
                    insert into usr values ({0:d}, '{1:s}', '{2:s}');
                '''.format(usr.id, usr.username.strip(), usr.first_name.strip()))
                curs.execute('''
                    insert into usr values ({0:d}, '{1:s}', '{2:s}');
                '''.format(usr.id, usr.username.strip(), usr.first_name.strip()))

        if cht.id==usr.id:
            return

        with self.__conn as conn:
            with conn.cursor() as curs:
                curs.execute('''
                    insert into cht values ({0:d}, '{1:s}');
                '''.format(cht.id, cht.title.strip()))

        with self.__conn as conn:
            with conn.cursor() as curs:
                curs.execute('''
                    insert into chtusr values ('{0:d}_{1:d}', {2:d}, {3:d});
                '''.format(cht.id, usr.id, cht.id, usr.id))


    def SaveBDay(self, bday):
        with self.__conn as conn:
            with conn.cursor() as curs:
                curs.execute('''
                    select uid from usr where uid={0:d};
                '''.format(bday.uid))
                isexist=curs.fetchall()

        if isexist.__len__()>0:
            with self.__conn as conn:
                with conn.cursor() as curs:
                    curs.execute('''
                        update usr set bd={0:d}, bm={1:d}, by={2:d} where uid={3:d};
                    '''.format(bday.bd, bday.bm, bday.by, bday.uid))
        else:
            with self.__conn as conn:
                with conn.cursor() as curs:
                    curs.execute('''
                        insert into usr values ({0:d}, '{1:s}', '{2:s}', {3:d}, {4:d}, {5:d});
                    '''.format(bday.uid, bday.uuname, bday.uname, bday.bd, bday.bm, bday.by))


    def getDateByUN(self, UN):
        with self.__conn as conn:
            with conn.cursor() as curs:
                curs.execute('''
                    select * from usr where uuname='{0:s}';
                '''.format(UN))
                rows=curs.fetchall()

        if rows.__len__()>0:
            records=rows[0]
            if not records[3]:
                return False
            else:
                return datetime.date(year=records[5], month=records[4], day=records[3])
        else:
            return False


    def GetUserBDayList(self):
        with self.__conn as conn:
            with conn.cursor() as curs:
                curs.execute('''
                    select uid, uuname, uname from usr where bd={0:d} and bm={1:d};
                '''.format(now.day, now.month))
                return curs.fetchall()


    def GetChatsList(self,userList):
        results=[]
        for user in userList:
            with self.__conn as conn:
                with conn.cursor() as curs:
                    curs.execute('''
                        select cid from chtusr where uid={0:d};
                    '''.format(user[0]))
                    chatsrows=self.__curs.fetchall()

            result=[]
            if len(chatsrows)>0:
                for chats in chatsrows:
                    for chat in chats:
                        result.append(chat)
            else:
                result.append(user[0])
            results.append(result)
        return results