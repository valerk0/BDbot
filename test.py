__author__ = 'Valery'

from HandleDB import DB
from BDayObj import BDayObj
from tstobj import message, chat, user

cht=chat(12345678,'some chat')
usr=user(98765432, 'uname', 'name')
msg=message(chat,user)

bdy=BDayObj(usr)
bdy.SetDate('/setdate 25.05.1987')

db=DB()
db.HandleMsg(msg)
db.SaveBDay(bdy)
