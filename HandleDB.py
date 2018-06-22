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
            self.__conn.commit()
        except:
            print('failed cht')

        try:
            self.__curs.execute('''
                insert into usr values ({0:d}, '{1:s}', '{2:s}');
            '''.format(msg.user.id, msg.user.username, msg.user.first_name))
            self.__conn.commit()
        except:
            print('failed usr',msg.user.id, msg.user.username, msg.user.first_name)

        try:
            self.__curs.execute('''
                insert into chtusr values ('{0:d}_{1:d}', {2:d}, {3:d});
            '''.format(msg.chat.id, msg.user.id, msg.chat.id, msg.user.id))
            self.__conn.commit()
        except:
            print('failed chtusr')


    def SaveBDay(self, bday):
        try:
            self.__curs.execute('select uid from usr where uid={0:d}'.format(bday.uid))
            f=True
        except:
            print('select failed')
            f=False
        if f:
            self.__curs.execute('''
               update usr set bd={0:d}, bm={1:d}, by={2:d}
                where uid={3:d}
            '''.format(bday.bd, bday.bm, bday.by, bday.uid))
            print('success upd usr')
        else:
            self.__curs.execute('''
                insert into usr values ({0:d}, '{1:s}', '{2:s}', {3:d}, {4:d}, {5:d});
            '''.format(bday.uid, bday.uuname, bday.uname, bday.bd, bday.bm, bday.by))
            print('success ins usr')

        self.__conn.commit

    def __del__(self):
        self.__conn.close()