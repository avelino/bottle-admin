# coding: utf-8
from decimal import Decimal
import pytest
from sqlalchemy.orm import sessionmaker

from bottle_application import app, engine, Product
from testutils import VerboseTestApp, WebFunctionalTest


@pytest.fixture(scope="function")
def session(request):
    session = sessionmaker(bind=engine)()
    return session


class TestControllers(WebFunctionalTest):
    app_test = VerboseTestApp(app)

    def test_add_model_get_controller(self, session):
        # TODO: tests with selenium or similar tool
        self.assert_302('/admin/product/add', '/admin/login')

        self.login('admin', '123')
        response = self.app_test.get('/admin/product/add')
        assert response.status == '200 OK'
        inputs = response.html.find_all('input')
        assert inputs[0].attrs['name'] == 'name'
        assert inputs[1].attrs['name'] == 'description'
        assert inputs[2].attrs['name'] == 'price'

        self.logout()

    def test_add_model_post_controller(self, session):
        self.assert_302('/admin/product/add', '/admin/login', 'POST')

        self.login('admin', '123')
        response = self.app_test.post('/admin/product/add')
        assert response.status == '200 OK'
        response.mustcontain('not created')

        self.assert_200('/admin/product/add')

        post = {'name': 'pp', 'description': 'des', 'price': 44.44}
        response = self.app_test.post('/admin/product/add', post)
        assert response.status == '302 Found'
        assert '/admin/product' in response.location

        product = session.query(Product).filter_by(name='pp').first()
        assert product.name == 'pp'
        assert product.description == 'des'
        assert product.price == Decimal('44.44')

        self.logout()

    def test_delete_model_controller(self, session):
        self.assert_302('/admin/product/delete/1', '/admin/login')

        self.login('admin', '123')
        session.query(Product).delete()
        session.commit()

        self.app_test.get('/admin/product/delete/1').mustcontain('not found')

        product1 = Product(name='p1', description='desc', price=1.1)
        session.add(product1)
        product2 = Product(name='p2', description='desc', price=2.2)
        session.add(product2)
        session.commit()

        url = '/admin/product/delete/{0}'.format(product1.id)
        response = self.app_test.get(url)
        assert response.status == '302 Found'
        assert '/admin/product' in response.location
        response = self.app_test.get(url)
        response.mustcontain('not found')

        url = '/admin/product/delete/{0}'.format(product2.id)
        response = self.app_test.get(url)
        assert response.status == '302 Found'
        assert '/admin/product' in response.location
        response = self.app_test.get(url)
        response.mustcontain('not found')

        self.logout()

    def test_edit_model_get_controller(self, session):
        self.assert_302('/admin/product/edit/1', '/admin/login')

        self.login('admin', '123')

        # TODO: tests with selenium or similar tool
        response = self.app_test.get('/admin/product/edit/1')
        assert response.status == '200 OK'
        response.mustcontain('not found')

        product1 = Product(name='p1', description='desc', price=1.1)
        session.add(product1)
        session.commit()

        url = '/admin/product/edit/{0}'.format(product1.id)
        response = self.app_test.get(url)
        assert response.status == '200 OK'
        inputs = response.html.find_all('input')
        assert inputs[0].attrs['name'] == 'name'
        assert inputs[1].attrs['name'] == 'description'
        assert inputs[2].attrs['name'] == 'price'

        self.logout()

    def test_edit_model_post_controller(self, session):
        self.assert_302('/admin/product/edit/1', '/admin/login', 'POST')

        self.login('admin', '123')

        session.query(Product).delete()
        session.commit()
        response = self.app_test.post('/admin/product/edit/1')
        assert response.status == '200 OK'
        response.mustcontain('not found')

        product1 = Product(name='p1', description='desc', price=1.1)
        session.add(product1)
        session.commit()

        url = '/admin/product/edit/{0}'.format(product1.id)
        assert self.app_test.get(url).status == '200 OK'
        session.close()

        post = {'name': 'pe', 'description': 'de', 'price': 1.5}
        response = self.app_test.post(url, post)
        assert response.status == '302 Found'

        session = sessionmaker(bind=engine)()
        p = session.query(Product).get(1)
        assert p.name == 'pe'
        assert p.description == 'de'
        assert p.price == 1.5

        self.logout()
        session.close()

    def test_list_model_controller(self, session):
        self.assert_302('/admin/product', '/admin/login')

        self.login('admin', '123')
        session.query(Product).delete()
        session.commit()

        response = self.app_test.get('/admin/product')
        response.mustcontain('not found')

        product1 = Product(name='p1', description='desc', price=1.1)
        session.add(product1)
        session.commit()

        response = self.app_test.get('/admin/product')
        rows = len(response.html.find_all('tr'))
        assert rows == 2

        product2 = Product(name='p2', description='desc', price=2.2)
        session.add(product2)
        session.commit()

        response = self.app_test.get('/admin/product')
        rows = len(response.html.find_all('tr'))
        assert rows == 3

        self.logout()

    def test_routes(self, session):
        self.assert_302('/admin', '/admin/login')

        self.login('admin', '123')
        self.assert_200('/admin')
        self.logout()
