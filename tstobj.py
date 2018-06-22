__author__ = 'Valery'

class user(object):
    def __init__(self, id, uuname, uname):
        self.__id=id
        self.__uuname=uuname
        self.__uname=uname

    @property
    def id(self):
        return self.__id

    @property
    def username(self):
        return self.__uuname

    @property
    def first_name(self):
        return self.__uname

class chat(object):
    def __init__(self, id, cname):
        self.__id=id
        self.__cname=cname

    @property
    def id(self):
        return self.__id

    @property
    def title(self):
        return self.__cname

class message(object):
    def __init__(self, cht, usr):
        self.__cht=cht
        self.__usr=usr

    @property
    def chat(self):
        return self.__cht

    @property
    def user(self):
        return self.__usr