__author__ = 'Valery'

class BDayObj(object):

    def __init__(self, usr):
        self.__uid=usr.id
        self.__uuname=usr.username
        self.__uname=usr.first_name

    def SetDate(self, command):
        FullDate=command.split()[1].split('.')
        self.__bd=FullDate[0]
        self.__bm=FullDate[1]
        self.__by=FullDate[2]

    @property
    def uid(self):
        return self.__uid

    @property
    def uuname(self):
        return self.__uuname

    @property
    def uname(self):
        return self.__uname

    @property
    def bd(self):
        return self.__bd

    @property
    def bm(self):
        return self.__bm

    @property
    def by(self):
        return self.__by