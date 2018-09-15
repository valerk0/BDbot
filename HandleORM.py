import threading
from confData import confData
from sqlalchemy import create_engine
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
        cht=Chat(id=ef_cht.id, name=ef_cht.title)
        
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
        return s.query(User).filter(BirthDay.bm==datetime.now().month,BirthDay.bd==datetime.now().day).all()