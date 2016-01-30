# coding: utf-8
from bottle import Bottle, TEMPLATE_PATH
from beaker.middleware import SessionMiddleware
import os
from sqlalchemy import create_engine, Column, Integer, Numeric, Sequence, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import bottle_admin
from bottle_admin import site
from bottle_admin.auth import get_aaa
from bottle_admin.auth.models import Role, User
from bottle_admin.options import ModelAdmin

ADMIN_TEMPLATE_PATH = os.path.join(os.path.dirname(bottle_admin.__path__[0]),
                                   'bottle_admin',
                                   'views')

TEMPLATE_PATH.insert(1, ADMIN_TEMPLATE_PATH)

engine = create_engine('sqlite:///test.db', echo=True)

Base = declarative_base()
Base.metadata.drop_all(bind=engine)


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    description = Column(String(50))
    price = Column(Numeric(10, 2))

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.fullname,
                                            self.password)


Product.metadata.create_all(engine)

app = Bottle()


class ProductAdmin(ModelAdmin):
    list_display = ('name', 'description', 'price')


site.setup(engine, app)
site.register(Product, ProductAdmin)

session_opts = {
    'session.type': 'file',
    'session.auto': True,
    'session.data_dir': './test_data'
}
app = SessionMiddleware(app, session_opts)

session = sessionmaker(bind=engine)()
role_user = Role(role='user', level=50)
session.add(role_user)
role_admin = Role(role='admin', level=500)
session.add(role_admin)
session.commit()

aaa = get_aaa()
hash = aaa._hash('user', '123')
session.add(User(username='user', hash=hash, role='user',
                 fullname='full', email_addr='e@e.com'))
hash = aaa._hash('admin', '123')
session.add(User(username='admin', hash=hash, role='admin',
                 fullname='admin', email_addr='a@a.com'))
session.commit()
