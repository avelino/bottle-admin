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

    def __init__(self, app=None, engine=None):
        self.app = app or Bottle()
        self.engine = engine
        self._registry = []

    def register(self, model=None):
        if model in self._registry:
            message = u'Model {} has already beeen registered'.format(model)
            raise AlreadyRegistered(message)
        self._registry.append(model)

    def setup_routing(self, app):
        from .controllers.main import (home_view, add_model_get_view, 
                                       add_model_post_view, list_model_view)
        self.app.route(
            '/',
            ['GET'],
            home_view)

        self.app.route(
            '/<model_name>/add',
            ['GET'],
            add_model_get_view)

        self.app.route(
            '/<model_name>/add',
            ['POST'],
            add_model_post_view)

        self.app.route(
            '/<model_name>',
            ['GET'],
            list_model_view)

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

            mapper = inspect(model)
            attrs = [prop.columns[0] for prop in mapper.attrs]
            model_data['columns'] = [prop.name for prop in attrs
                                     if prop.name != 'id']

            model_data['add_url'] = '{}/{}/add'.format(self.url_prefix, model_name)
            model_data['list_url'] = '{}/{}'.format(self.url_prefix, model_name)
            model_data['change_url'] = '{}/{}/change'.format(self.url_prefix, model_name)
            model_data['delete'] = '{}/{}/delete'.format(self.url_prefix, model_name)

            models_dict[model] = model_data
        return models_dict

    def get_model_meta_list(self):
        models_dict = self._build_models_dict()
        return sorted(models_dict.values(), key=lambda x: x['name'].lower())

    def get_model_class(self, model_name):
        for model_class in self._registry:
            if model_class.__name__.lower() == model_name:
                return model_class
        raise NotRegistered(u'Model {} has not been registered'.format(model_name))

    def get_model_meta(self, model_name):
        models_meta = self.get_model_meta_list()
        for meta in models_meta:
            if meta['name'] == model_name:
                return meta
        raise NotRegistered(u'Model {} has not been registered'.format(model_name))
        


site = AdminSite()
