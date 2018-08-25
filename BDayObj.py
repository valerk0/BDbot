__author__ = 'Valery'

class BDayObj(object):

    def __init__(self, usr):
        self.id=usr.id
        self.uname=usr.username
        self.name=usr.first_name
        self.lname=usr.last_name

    def SetDate(self, command):
        FullDate=command.split('.')
        self.bd=int(FullDate[0])
        self.bm=int(FullDate[1])
        self.by=int(FullDate[2])
        
