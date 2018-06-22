__author__ = 'Valery'

class BDayObj(object):

    def __init__(self, usr):
        self.uid=usr.id
        self.uuname=usr.username
        self.uname=usr.first_name

    def SetDate(self, command):
        FullDate=command.split()[1].split('.')
        self.bd=FullDate[0]
        self.bm=FullDate[1]
        self.by=FullDate[2]
