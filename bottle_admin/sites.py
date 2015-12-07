# coding: utf-8

from bottle import Bottle
from sqlalchemy import inspect


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

    def __init__(self, app=None, engine=None):
        self.app = app or Bottle()
        self.engine = engine
        self._registry = []

    def register(self, model=None):
        if model in self._registry:
            message = u'Model {0} has already beeen registered'.format(model)
            raise AlreadyRegistered(message)
        self._registry.append(model)

    def setup_routing(self, app):
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
            '/<model_name>',
            ['GET'],
            list_model_controller)

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

        app.mount(self.url_prefix, self.app)

    def _build_models_dict(self):
        """
        Build the models dict containing the URLs for each action and model
        """

        models_dict = {}
        for model in self._registry:
            model_data = {}

            model_name = model.__name__.lower()
            model_data['name'] = model_name
            model_data['model_class'] = model

            mapper = inspect(model)
            attrs = [prop.columns[0] for prop in mapper.attrs]
            model_data['columns'] = (prop.name for prop in attrs
                                     if prop.name != 'id')

            model_data['add_url'] = '{0}/{1}/add'.format(self.url_prefix, model_name)
            model_data['list_url'] = '{0}/{1}'.format(self.url_prefix, model_name)
            model_data['edit_url'] = '{0}/{1}/edit'.format(self.url_prefix, model_name)
            model_data['delete_url'] = '{0}/{1}/delete'.format(self.url_prefix, model_name)

            models_dict[model] = model_data
        return models_dict

    def get_model_meta_list(self):
        models_dict = self._build_models_dict()
        return sorted(models_dict.values(), key=lambda x: x['name'].lower())

    def get_model_class(self, model_name):
        for model_class in self._registry:
            if model_class.__name__.lower() == model_name:
                return model_class
        raise NotRegistered(u'Model {0} has not been registered'.format(model_name))

    def get_model_meta(self, model_name):
        models_meta = self.get_model_meta_list()
        for meta in models_meta:
            if meta['name'] == model_name:
                return meta
        raise NotRegistered(u'Model {0} has not been registered'.format(model_name))


site = AdminSite()
