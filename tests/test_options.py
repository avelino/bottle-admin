# coding: utf-8
from bottle_admin import site
from bottle_admin.options import ModelAdmin
from bottle_admin.sites import AdminSite
# from sqlalchemy.orm import sessionmaker

from bottle_application import app, Product, User
from testutils import VerboseTestApp, WebFunctionalTest


class TestAdminOptions(WebFunctionalTest):
    app_test = VerboseTestApp(app)

    @classmethod
    def assert_model_meta(cls, model, columns):
        assert set(model.columns) == columns
        assert model.add_url == '{0}/{1}/add'.format(AdminSite.url_prefix, model.name)
        assert model.list_url == '{0}/{1}'.format(AdminSite.url_prefix, model.name)
        edit_url = '{0}/{1}/edit'.format(AdminSite.url_prefix, model.name)
        assert model.edit_url == edit_url
        delete_url = '{0}/{1}/delete'.format(AdminSite.url_prefix, model.name)
        assert model.delete_url == delete_url

    def test_object(self):
        user_model = ModelAdmin(User, site)
        columns = set(('username', 'fullname', 'hash', 'creation_date',
                       'role', 'email_addr', 'desc', 'last_login'))
        TestAdminOptions.assert_model_meta(user_model, columns)

        product_model = ModelAdmin(Product, site)
        columns = set(('name', 'description', 'price'))
        TestAdminOptions.assert_model_meta(product_model, columns)
