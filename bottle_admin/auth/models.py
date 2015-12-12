# coding: utf-8
import datetime
from sqlalchemy import Column, DateTime, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AbstractUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(50))
    hash = Column(String(20))
    role = Column(String(20))
    creation_date = Column(DateTime, default=datetime.datetime.now)

    class Meta:
        abstract = True


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    role = Column(String(20))
    level = Column(Integer)


class User(AbstractUser):
    fullname = Column(String(100))
    email_addr = Column(String(100))
    desc = Column(String(100))
    last_login = Column(DateTime)
