__author__ = 'Valery'

class user(object):
    def __init__(self, id, uuname, uname):
        self.id=id
        self.username=uuname
        self.first_name=uname


class chat(object):
    def __init__(self, id, cname):
        self.id=id
        self.title=cname


class message(object):
    def __init__(self, cht, usr):
        self.chat=cht
        self.user=usr
