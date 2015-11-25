# coding: utf-8
from bottle import Bottle
import datetime
from sqlalchemy import (create_engine, Column, DateTime, Integer, Numeric,
                        Sequence, String)
from sqlalchemy.ext.declarative import declarative_base

from bottle_admin import site

engine = create_engine('sqlite:///:memory:', echo=True)

app = Bottle()
site.setup_routing(app)
site.engne = engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))
    registration_date = Column(DateTime, default=datetime.datetime.now)

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.fullname,
                                            self.password)


User.metadata.create_all(engine)


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    description = Column(String(50))
    price = Column(Numeric(10, 2))

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.fullname,
                                            self.password)
