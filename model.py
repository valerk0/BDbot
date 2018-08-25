from sqlalchemy import Column, ForeignKey, BigInteger, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base=declarative_base()

class User(Base):
    __tablename__='tuser'
    id=Column(BigInteger,primary_key=True)
    name=Column(String(250))
    lname=Column(String(250))
    uname=Column(String(250))
    chat=relationship('Chat',secondary='user_chat')
    bday=relationship('BirthDay')

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
    __tablename__='birth_day'
    user_id=Column(BigInteger,ForeignKey('tuser.id'),primary_key=True)
    by=Column(Integer)
    bm=Column(Integer)
    bd=Column(Integer)
    user=relationship('User')
