# coding: utf-8

from bottle import Bottle

from bottle_admin import auth
from bottle_admin.options import ModelAdmin


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class AdminSite(object):
    """
    Creates an admin site for models
    """

    url_prefix = '/admin'

    def __repr__(self):
        return "<AdminSite('{0}', '{1}')>".format(self.app, self._registry)

    def __init__(self, app=None, engine=None, auth=None):
        self.app = app or Bottle()
        self.engine = engine
        self.auth = auth
        self._registry = []

    def setup(self, engine, app):
        self.engine = engine
        self.setup_routing(app)
        self.setup_models()
        auth.setup(self.engine)

    def setup_models(self):
        from auth.admin import RoleAdmin, UserAdmin
        self.register(auth.Role, RoleAdmin)
        self.register(auth.User, UserAdmin)

    def setup_routing(self, app):
        from .auth.controllers import (login_get_controller, login_post_controller,
                                       logout_controller)
        from .controllers.main import (add_model_get_controller,
                                       add_model_post_controller,
                                       edit_model_get_controller,
                                       edit_model_post_controller,
                                       delete_model_controller, home_controller,
                                       list_model_controller)
        self.app.route(
            '/',
            ['GET'],
            home_controller)

        self.app.route(
            '/<model_name>/add',
            ['GET'],
            add_model_get_controller)

        self.app.route(
            '/<model_name>/add',
            ['POST'],
            add_model_post_controller)

        self.app.route(
            '/<model_name>/delete/<model_id>',
            ['GET'],
            delete_model_controller)

        self.app.route(
            '/<model_name>/edit/<model_id>',
            ['GET'],
            edit_model_get_controller)

        self.app.route(
            '/<model_name>/edit/<model_id>',
            ['POST'],
            edit_model_post_controller)

        self.app.route(
            '/login',
            ['GET'],
            login_get_controller)

        self.app.route(
            '/login',
            ['POST'],
            login_post_controller)

        self.app.route(
            '/logout',
            ['GET'],
            logout_controller)

        self.app.route(
            '/<model_name>',
            ['GET'],
            list_model_controller)

        app.mount(self.url_prefix, self.app)

    def register(self, model, admin_class=None):
        if not admin_class:
            admin_class = ModelAdmin
        admin_obj = admin_class(model, self)

        if self.is_registered(admin_obj):
            message = u'Model {0} has already beeen registered'.format(model)
            raise AlreadyRegistered(message)

        self._registry.append(admin_obj)

    def is_registered(self, model):
        if type(model) is ModelAdmin:
            return model in self._registry

        for model_admin in self._registry:
            if model == model_admin.model_cls:
                return True
        return False

    def get_models(self):
        return self._registry

    def get_model(self, model_name):
        for model_admin in self._registry:
            if model_admin.name == model_name:
                return model_admin
        raise NotRegistered(u'Model {0} has not been registered'.format(model_name))


site = AdminSite()
