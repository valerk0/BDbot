from sqlalchemy import Column, ForeignKey, BigInteger, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base=declarative_base()

class User(Base):
    print('u1')
    __tablename__='tuser'
    print('u2')
    id=Column(BigInteger,primary_key=True)
    print('u3')
    name=Column(String(250))
    lname=Column(String(250))
    uname=Column(String(250))
    chat=relationship('Chat',secondary='user_chat')
    bday=relationship('BirthDay')
    print('u4')

class Chat(Base):
    __tablename__='chat'
    id=Column(BigInteger,primary_key=True)
    name=Column(String(250))
    user=relationship('User',secondary='user_chat')

class UserChat(Base):
    __tablename__='user_chat'
    user_id=Column(BigInteger,ForeignKey('tuser.id'),primary_key=True)
    chat_id=Column(BigInteger,ForeignKey('chat.id'),primary_key=True)

class BirthDay(Base):
    print('b1')
    __tablename__='birth_day'
    print('b2')
    user_id=Column(BigInteger,ForeignKey('tuser.id'),primary_key=True)
    print('b3')
    by=Column(Integer)
    bm=Column(Integer)
    bd=Column(Integer)
    user=relationship('User')
    print('b4')
