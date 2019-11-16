import threading
from confData import confData
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime
import os
from model import Base, User, Chat, UserChat, BirthDay

class DB(object):
    def __init__(self):
        self.lock=threading.Lock()
        self.lock.acquire()
        DATABASE_URL='postgresql://postgres:12345@localhost/bddb'
        engine=create_engine(os.environ.get('DATABASE_URL') or DATABASE_URL or 'sqlite:///')
        session=sessionmaker()
        session.configure(bind=engine)
        Base.metadata.create_all(engine)
        self.s=session()

    def __del__(self):
        self.lock.release()


    def HandleMsg(self,upd):
        s=self.s
        
        ef_usr=upd.effective_user
        ef_cht=upd.effective_chat
        usr=User(id=ef_usr.id, name=ef_usr.first_name, lname=ef_usr.last_name, uname=ef_usr.username)
        cht=Chat(id=ef_cht.id, name=ef_cht.first_name if ef_cht.type=='private' else ef_cht.title)
        
        if not (s.query(User).filter(User.id==usr.id).first() and s.query(Chat).filter(Chat.id==cht.id).first() \
            and s.query(UserChat).filter(UserChat.user_id==usr.id, UserChat.chat_id==cht.id).first()):
            if not s.query(User).filter(User.id==usr.id).first():
                cht.user.append(usr)
                if not s.query(Chat).filter(Chat.id==cht.id).first():
                    s.add(cht)
                else:
                    for x in s.query(Chat).filter(Chat.id==cht.id).first().user:
                        cht.user.append(x)
                    s.merge(cht)
            else:
                for x in s.query(User).filter(User.id==usr.id).first().chat:
                    usr.chat.append(x)
                if s.query(Chat).filter(Chat.id==cht.id).first():
                    for x in s.query(Chat).filter(Chat.id==cht.id).first().user:
                        cht.user.append(x)
                usr.chat.append(cht)
                s.merge(usr)
        else:
            if not s.query(User).filter(User.id==usr.id,User.name==usr.name,User.lname==usr.lname,User.uname==usr.uname).first():
                for x in s.query(User).filter(User.id==usr.id).first().chat:
                    usr.chat.append(x)
                s.merge(usr)
        
        s.commit()


    def SaveBDay(self, bday):
        s=self.s
        usr=User(id=bday.id, name=bday.name, lname=bday.lname, uname=bday.uname)
        bd=BirthDay(user_id=bday.id, by=bday.by, bm=bday.bm, bd=bday.bd)
        usr.bday.append(bd)

        if s.query(User).filter(User.id==usr.id).first():
            for x in s.query(User).filter(User.id==usr.id).first().chat:
                usr.chat.append(x)
            s.merge(usr)
        else:
            s.add(usr)

        s.commit()


    def getDateByUN(self, UN):
        s=self.s
        usr=s.query(User).filter(User.uname==UN).first()
        if usr:
            if not usr.bday==[]:
                return date(usr.bday[0].by,usr.bday[0].bm,usr.bday[0].bd)
        return


    def getUsersBDay(self):
        s=self.s
        return s.query(User).join(User.bday).filter(BirthDay.bm==datetime.now().month,BirthDay.bd==datetime.now().day).all()


    def delBDay(self,upd):
        s=self.s
        bd=s.query(BirthDay).filter(BirthDay.user_id==upd.effective_user.id)
        if bd.first():
            bd.delete()
            s.commit()
            return True
        return False


    def get10(self,upd, bot):
        s=self.s
        bot.send_message(chat_id=upd.effective_user.id, text='enter db')
        curChat=select([User.id]).where(User.chat.any(Chat.id==upd.effective_chat.id))
        users=s.query(User).filter(User.id.in_(curChat)).join(User.bday).order_by(BirthDay.bm,BirthDay.bd).all()
        bot.send_message(chat_id=upd.effective_user.id, text='1')
        if users:
            l=[]
            curd=datetime.now().day
            curm=datetime.now().month
            for usr in users:
                tx=f'{usr.name if usr.name else ""} {usr.bday[0].by} {usr.bday[0].bm} {usr.bday[0].bd}'
                bot.send_message(chat_id=upd.effective_user.id, text=tx)
                l.append([usr.bday[0].bd+100*(usr.bday[0].bm+\
                (0 if (usr.bday[0].bm>curm or (usr.bday[0].bm==curm and usr.bday[0].bd>=curd)) else 12)),usr])
                bot.send_message(chat_id=upd.effective_user.id, text='done')
            bot.send_message(chat_id=upd.effective_user.id, text='done all')
            return sorted(l)[:10]
        return False


    def stat(self,upd):
    	s=self.s
    	curChat=select([User.id]).where(User.chat.any(Chat.id==upd.effective_chat.id))
    	chatUsers=s.query(User).filter(User.id.in_(curChat)).count()
    	allUsers=s.query(User).count()
    	allChats=s.query(Chat).filter(Chat.id<0).count()
    	chatBDays=s.query(BirthDay).filter(BirthDay.user_id.in_(curChat)).count()
    	allBDays=s.query(BirthDay).count()
    	return {'allUsers':allUsers,'allChats':allChats,'allBDays':allBDays,'chatUsers':chatUsers,'chatBDays':chatBDays}
