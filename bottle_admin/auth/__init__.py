# coding: utf-8

from cork import Cork
from cork.backends import SqlAlchemyBackend

from .models import Role, User

__all__ = ['Role', 'User']


def get_aaa():
    return getattr(__import__(__name__), 'aaa')


def setup(engine):
    Role.metadata.create_all(engine)
    User.metadata.create_all(engine)

    # setup cork auth
    backend = SqlAlchemyBackend(engine.url)
    aaa = Cork(backend=backend)
    setattr(__import__(__name__), 'aaa', aaa)
