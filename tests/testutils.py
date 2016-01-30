# coding: utf-8
from webtest import TestApp


class VerboseTestApp(TestApp):

    """A testapp that prints the traceback when it exists."""

    def _check_status(self, status, res):
        print(res.errors)
        super(VerboseTestApp, self)._check_status(status, res)


class WebFunctionalTest(object):
    def login(self, username, password):
        post = {'username': username, 'password': password}
        response = self.app_test.post('/admin/login', post)
        assert response.status == '302 Found'
        assert '/admin' in response.location

    def logout(self):
        response = self.app_test.get('/admin/logout')
        assert response.status == '302 Found'
        assert '/admin/login' in response.location

    def assert_302(self, request_url, redirect_url, method='GET'):
        if method == 'GET':
            response = self.app_test.get(request_url)
        elif method == 'POST':
            response = self.app_test.post(request_url)
        else:
            raise Exception(u'Invalid HTTP method')
        assert response.status == '302 Found'
        assert redirect_url in response.location

    def assert_200(self, request_url):
        assert self.app_test.get(request_url).status == '200 OK'
