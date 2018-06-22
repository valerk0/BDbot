__author__ = 'Valery'

class user(object):
    def __init__(self, id, uuname, uname):
        self.__id=id
        self.__uuname=uuname
        self.__uname=uname

    id= int(self.__id)

    username= str(self.__uuname)

    first_name= str(self.__uname)

class chat(object):
    def __init__(self, id, cname):
        self.__id=id
        self.__cname=cname

    id= int(self.__id)

    title= str(self.__cname)

class message(object):
    def __init__(self, cht, usr):
        self.__cht=cht
        self.__usr=usr

    chat= self.__cht

    user= self.__usr