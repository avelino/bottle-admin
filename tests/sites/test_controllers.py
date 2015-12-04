# coding: utf-8
import pytest
from sqlalchemy.orm import sessionmaker
from webtest import TestApp

from bottle_application import app, engine, User


@pytest.fixture(scope="function")
def session(request):
    return sessionmaker(bind=engine)()


@pytest.fixture(scope="function")
def app_test(request):
    app_test = TestApp(app)
    return app_test


def test_routes(session, app_test):
    assert app_test.get('/admin').status == '200 OK'
    assert app_test.get('/admin/user').status == '200 OK'
    assert app_test.get('/admin/user/add').status == '200 OK'
    assert app_test.get('/admin/user/delete/1').status == '200 OK'
    assert app_test.get('/admin/product').status == '200 OK'
    assert app_test.get('/admin/product/add').status == '200 OK'
    assert app_test.get('/admin/product/delete/1').status == '200 OK'


def test_delete_model_controller(session, app_test):
    app_test.get('/admin/user/delete/1').mustcontain('has not been found')

    user1 = User(name='name', fullname='full', password='pass')
    session.add(user1)
    user2 = User(name='name2', fullname='full', password='pass')
    session.add(user2)
    session.commit()

    status = app_test.get('/admin/user/delete/{0}'.format(user1.id)).status
    assert status == '302 Found'
    request = app_test.get('/admin/user/delete/{0}'.format(user1.id))
    request.mustcontain('has not been found')

    status = app_test.get('/admin/user/delete/{0}'.format(user2.id)).status
    assert status == '302 Found'
    request = app_test.get('/admin/user/delete/{0}'.format(user2.id))
    request.mustcontain('has not been found')
