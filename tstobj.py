__author__ = 'Valery'

class user(object):
    def __init__(self, id, uuname, uname):
        self.__id=id
        self.__uuname=uuname
        self.__uname=uname

    id= int(__id)

    username= str(__uuname)

    first_name= str(__uname)

class chat(object):
    def __init__(self, id, cname):
        self.__id=id
        self.__cname=cname

    id= int(__id)

    title= str(__cname)

class message(object):
    def __init__(self, cht, usr):
        self.__cht=cht
        self.__usr=usr

    chat= __cht

    user= __usr