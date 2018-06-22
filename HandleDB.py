__author__ = 'Valery'

import psycopg2
from DBconfData import DBconf

class DB(object):

    def __init__(self):
        self.__conn=psycopg2.connect(**DBconf.db_params)
        self.__curs=self.__conn.cursor()

    def HandleMsg(self,msg):
        try:
            self.__curs.execute('''
                insert into cht values ({0:d}, '{1:s}');
            '''.format(msg.chat.id, msg.chat.title))
        except:
            print('failed cht')

        try:
            self.__curs.execute('''
                insert into usr values ({0:d}, '{1:s}', '{2:s}');
            '''.format(msg.user.id, msg.user.username, msg.user.first_name))
        except:
            print('failed usr')

        try:
            self.__curs.execute('''
                insert into chtusr values ('{0:d}_{1:d}', {2:d}, {3:d});
            '''.format(msg.chat.id, msg.user.id, msg.chat.id, msg.user.id))
        except:
            print('failed chtusr')

        self.__conn.commit()


    def SaveBDay(self, bday):
        self.__curs.execute('select uid from usr where uid={0:d}'.format(bday.uid))
        if self.__curs.fetchall()[0][0]>0:
            self.__curs.execute('''
               update usr set bd={0:d}, bm={1:d}, by={2:d}
                where uid={3:d}
            '''.format(bday.bd, bday.bm, bday.by, bday.uid))
        else:
            self.__curs.execute('''
                insert into usr values ({0:d}, '{1:s}', '{2:s}', {3:d}, {4:d}, {5:d});
            '''.format(bday.uid, bday.uuname, bday.uname, bday.bd, bday.bm, bday.by))

        self.__conn.commit()

    def __del__(self):
        self.__conn.close()