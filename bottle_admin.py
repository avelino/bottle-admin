# coding: utf-8


def admin_home():
    return 'Home do admin'


def admin_view(model_name, id_=None):
    return model_name, id_


class Admin(object):
    """
    Creates an admin interface for models
    """

    url_prefix = '/admin'

    def __init__(self, app=None):
        self.app = app
        self._models = []

    def register(self, model=None, modeladmin=None):
        self._models.append((model, modeladmin))

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
