__author__ = 'Valery'

class BDayObj(object):

    def __init__(self, usr):
        self.uid=usr.id
        self.uuname=usr.username
        self.uname=usr.first_name

    def SetDate(self, command):
        FullDate=command.split()[1].split('.')
        self.bd=int(FullDate[0])
        self.bm=int(FullDate[1])
        self.by=int(FullDate[2])

    print(bd)
