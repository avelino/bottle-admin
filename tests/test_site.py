# coding: utf-8
import pytest
from bottle_admin.auth.models import User
from bottle_admin.options import ModelAdmin
from bottle_admin.sites import AdminSite, AlreadyRegistered, NotRegistered

from bottle_application import Product
from testutils import VerboseTestApp
from test_options import TestAdminOptions


@pytest.fixture(scope="function")
def site(request):
    site = AdminSite()
    return site


class TestAdminSite(VerboseTestApp):
    def test_register(self, site):
        assert len(site._registry) == 0

        site.register(Product)
        assert len(site._registry) == 1

        with pytest.raises(AlreadyRegistered):
            site.register(User)
            site.register(Product)

    def test_is_registered(self, site):
        assert site.is_registered(ModelAdmin(Product, site))
        site.register(Product)
        product = site._registry[0]
        assert site.is_registered(product)

    def test_get_model(self, site):
        with pytest.raises(NotRegistered):
            site.get_model('user')

        with pytest.raises(NotRegistered):
            site.get_model('product')

        site.register(User)
        model = site.get_model('user')
        assert model.model_cls == User
        columns = set(('username', 'fullname', 'hash', 'creation_date',
                       'role', 'email_addr', 'desc', 'last_login'))
        TestAdminOptions.assert_model_meta(model, columns)

        site.register(Product)
        model = site.get_model('product')
        assert model.model_cls == Product
        columns = set(('name', 'description', 'price'))
        TestAdminOptions.assert_model_meta(model, columns)

    def test_get_models(self, site):
        assert len(site.get_models()) == 0
        site.register(Product)
        site.register(User)
        assert len(site.get_models()) == 2
