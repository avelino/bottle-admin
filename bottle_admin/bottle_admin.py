# coding: utf-8
from .views import admin_home, admin_view


class Admin(object):
    """
    Creates an admin interface for models
    """

    url_prefix = '/admin'

    def __init__(self, app=None):
        self.app = app
        self._models = []

    def register(self, model=None):
        self._models.append(model)

    def setup_routing(self, app):
        app.route(
            '{prefix}'.format(prefix=self.url_prefix),
            ['GET'],
            admin_home)

        for model in self._models:
            app.route(
                '{prefix}/{model_name}/'.format(
                    model_name=model.__tablename__,
                    prefix=self.url_prefix),
                ['GET'],
                admin_view)

admin = Admin()
