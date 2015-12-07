# coding: utf-8
from bottle import Bottle, TEMPLATE_PATH
import datetime
import os
from sqlalchemy import (create_engine, Column, DateTime, Integer, Numeric,
                        Sequence, String)
from sqlalchemy.ext.declarative import declarative_base

import bottle_admin
from bottle_admin import site

ADMIN_TEMPLATE_PATH = os.path.join(os.path.dirname(bottle_admin.__path__[0]),
                                   'bottle_admin',
                                   'views')

TEMPLATE_PATH.insert(1, ADMIN_TEMPLATE_PATH)

engine = create_engine('sqlite:///:memory:', echo=True)

app = Bottle()

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


Product.metadata.create_all(engine)

site.setup_routing(app)
site.register(User)
site.register(Product)
site.engine = engine
