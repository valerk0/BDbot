__author__ = 'Valery'
 

import psycopg2, datetime, threading
from datetime import datetime, date
from urllib.parse import urlparse
import os 

class DB(object): 

    def __init__(self):
        db_config = urlparse(os.environ['DATABASE_URL'])
        self.__conn=psycopg2.connect(user=db_config.username,
                                     password=db_config.password,
                                     database=db_config.path[1:],
                                     host=db_config.hostname) 

    def __del__(self):
        self.__conn.close()
 

    def HandleMsg(self,upd):
        usr=upd.effective_user
        cht=upd.effective_chat 

        with threading.Lock():
            try:
                with self.__conn as conn:
                    with conn.cursor() as curs:
                        curs.execute('''
                        select uid from usr where uid={0:d};
                    '''.format(usr.id))
                    isexist = curs.fetchall()
                    if isexist and isexist[0] and isexist[0][0]:
                        isexist = True
                    else:
                        isexist = False
                if isexist:
                    with self.__conn as conn:
                        with conn.cursor() as curs:
                            fname = usr.first_name.strip()
                            lname = usr.last_name.strip()
                            if fname and lname:
                                fulln = '{} {}'.format(fname, lname)
                            else:
                                fulln = fname or lname
                            curs.execute('''
                                update usr set uuname={1:d}, uname={2:d} where uid={0:d};
                            '''.format(usr.id, usr.username.strip(), fulln))
            except:
                pass 

            if cht.id==usr.id:
                return 

            try:
                with self.__conn as conn:
                    with conn.cursor() as curs:
                        curs.execute('''
                            insert into cht values ({0:d}, '{1:s}');
                        '''.format(cht.id, cht.title.strip())) 
            except:
                pass 

    def SaveBDay(self, bday):
        with threading.Lock():
            with self.__conn as conn:
                with conn.cursor() as curs:
                    curs.execute('''
                        select uid from usr where uid={0:d};
                    '''.format(bday.id))
                    isexist=curs.fetchall() 
                    if isexist and isexist[0] and isexist[0][0]:
                        isexist = True
                    else:
                        isexist = False

            try:
                if isexist:
                    with self.__conn as conn:
                        with conn.cursor() as curs:
                            curs.execute('''
                                update usr set bd={0:d}, bm={1:d}, by={2:d} where uid={3:d};
                            '''.format(bday.bd, bday.bm, bday.by, bday.id))
                else:
                    with self.__conn as conn:
                        with conn.cursor() as curs:
                            curs.execute('''
                                insert into usr values ({0:d}, '{1:s}', '{2:s}', {3:d}, {4:d}, {5:d});
                            '''.format(bday.id, bday.uname, bday.name, bday.bd, bday.bm, bday.by))
            except:
                pass 

    def getDateByUN(self, UN):
        with threading.Lock():
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
                print(records)
                return date(year=records[5], month=records[4], day=records[3])
        else:
            return False 

    def GetUserBDayList(self):
        with threading.Lock():
            with self.__conn as conn:
                with conn.cursor() as curs:
                    curs.execute('''
                        select uid, uuname, uname from usr where bd={0:d} and bm={1:d};
                    '''.format(datetime.now().day, datetime.now().month))
                    return curs.fetchall() 

    def GetChatsList(self):
        with threading.Lock():
            with self.__conn as conn:
                with conn.cursor() as curs:
                    curs.execute('''
                        select cid from cht;
                    ''')
                    return curs.fetchall() 

    def get_ordered_bdays(self):
        curd=datetime.now().day
        curm=datetime.now().month
        with threading.Lock():
            with self.__conn as conn:
                with conn.cursor() as curs:
                    curs.execute('''
                        select * from usr order by bm, bd;
                    ''')
                    userrows=curs.fetchall()
        i = 0
        for i,urow in enumerate(userrows):
            if  urow[4] * 100 + urow[3] >= curm * 100 + curd: 
                print(urow[3], curd, urow[4], curm)
                break
        ordered_bdays = []
        ordered_bdays = userrows[i:]
        if i > 0:
            for j in range(i):
                ordered_bdays.append(userrows[j])
        return ordered_bdays 

    def stat(self):
        with threading.Lock():
            with self.__conn as conn:
                with conn.cursor() as curs:
                    curs.execute('''
                        select count(cid) from cht;
                    ''')
                    chats_num=curs.fetchall()[0][0]
                    curs.execute('''
                        select count(uid) from usr;
                    ''')
                    usrs_num=curs.fetchall()[0][0]
        return {'allChats': chats_num, 'allBDays': usrs_num} 

    def del_bday(self, upd):
        uid = None
        with threading.Lock():
            with self.__conn as conn:
                with conn.cursor() as curs:
                    curs.execute('''
                        select uid from usr where uid={};
                    '''.format(upd.effective_user.id))
                    uid = curs.fetchall()
        if uid and uid[0] and uid[0][0]:
            with threading.Lock():
                with self.__conn as conn:
                    with conn.cursor() as curs:
                        curs.execute('''
                            delete from usr where uid={};
                        '''.format(upd.effective_user.id))
            return True
        return False

    def get_chat_list(self):
        chts = None
        with threading.Lock():
            with self.__conn as conn:
                with conn.cursor() as curs:
                    curs.execute('''
                        select * from cht;
                    ''')
                    chts = curs.fetchall()
        return chts

    def del_cht(self, cht):
        print('deleting chat {}'.format(cht))
        with threading.Lock():
            with self.__conn as conn:
                with conn.cursor() as curs:
                    curs.execute('''
                        delete from cht where cid={};
                    '''.format(cht))
