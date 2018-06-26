__author__ = 'Valery'

import psycopg2, datetime
from confData import confData

class DB(object):

    def __init__(self):
        __connect()

    def __connect(self):
        conf=confData('dbconfig.ini','DATABASE')
        self.__conn=psycopg2.connect(**conf.params)
        self.__curs=self.__conn.cursor()

    def __del__(self):
        self.__conn.close()


    def HandleMsg(self,upd):
        usr=upd.effective_user
        cht=upd.effective_chat

        try:
            self.__curs.execute('''
                insert into usr values ({0:d}, '{1:s}', '{2:s}');
            '''.format(usr.id, usr.username.strip(), usr.first_name.strip()))
            self.__conn.commit()
        except:
            pass

        if cht.id==usr.id:
            return

        self.__conn.close()
        __connect()
        try:
            print('1')
            self.__curs.execute(u"insert into cht values ({0:d}, '{1:s}');".format(cht.id, cht.title.strip()))
            self.__conn.commit()
            print('2')
        except:
            pass

        try:
            self.__curs.execute('''
                insert into chtusr values ('{0:d}_{1:d}', {2:d}, {3:d});
            '''.format(cht.id, usr.id, cht.id, usr.id))
            self.__conn.commit()
        except:
            pass



    def SaveBDay(self, bday):
        self.__curs.execute('select uid from usr where uid={0:d}'.format(bday.uid))
        if self.__curs.fetchall().__len__()>0:
            self.__curs.execute('''
               update usr set bd={0:d}, bm={1:d}, by={2:d}
                where uid={3:d}
            '''.format(bday.bd, bday.bm, bday.by, bday.uid))
        else:
            self.__curs.execute('''
                insert into usr values ({0:d}, '{1:s}', '{2:s}', {3:d}, {4:d}, {5:d});
            '''.format(bday.uid, bday.uuname, bday.uname, bday.bd, bday.bm, bday.by))

        self.__conn.commit()

    def getDateByUN(self, UN):
        self.__curs.execute('''
                select * from usr where uuname='{0:s}'
            '''.format(UN))
        rows=self.__curs.fetchall()
        if rows.__len__()>0:
            records=rows[0]
            if not records[3]:
                return False
            else:
                return datetime.date(year=records[5], month=records[4], day=records[3])
        else:
            return 

    def GetUserBDayList(self):
        now=datetime.datetime.now()
        self.__curs.execute('select uid, uuname, uname from usr where bd={0:d} and bm={1:d}' \
                            .format(now.day, now.month))
        return self.__curs.fetchall()

    def GetChatsList(self,userList):
        results=[]
        for user in userList:
            self.__curs.execute('select cid from chtusr where uid={0:d}'.format(user[0]))
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

