from sqlalchemy import Column, Integer, String, Sequence, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, backref

from database import connector

class User(connector.Manager.Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id'), primary_key=True)
    fullname = Column(String(50))
    password = Column(String(12))
    username = Column(String(12))
    email = Column(String(25))
    celular = Column(Integer)

class Message(connector.Manager.Base):
    __tablename__ = 'messages'
    id = Column(Integer, Sequence('message_id'), primary_key=True)
    content = Column(String(500))
    sent_on = Column(DateTime(timezone=True))
    user_from_id = Column(Integer, ForeignKey('users.id'))
    user_to_id = Column(Integer, ForeignKey('users.id'))

    user_from = relationship(User, foreign_keys=[user_from_id])
    user_to = relationship(User, foreign_keys=[user_to_id])

class Ingresos(connector.Manager.Base):
    __tablename__ = 'ingresos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre=Column(String(30))
    cant=Column(Integer) #Cambiar por decimal