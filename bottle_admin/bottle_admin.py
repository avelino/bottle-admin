# coding: utf-8

from bottle import Bottle
from sqlalchemy import inspect

from .controllers.main import home_view, add_model_view


class AlreadyRegistered(Exception):
    pass


class AdminSite(object):
    """
    Creates an admin site for models
    """

    url_prefix = '/admin'

    def __init__(self, app=None):
        self.app = Bottle()
        self._registry = []

    def register(self, model=None):
        if model in self._registry:
            raise AlreadyRegistered(u'Model {} has already beeen registered'.format(model))
        self._registry.append(model)

    def setup_routing(self, app):
        self.app.route(
            '/',
            ['GET'],
            home_view)

        self.app.route(
            '/<model_name>/add'.format(prefix=self.url_prefix),
            ['GET'],
            add_model_view)

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
            model_data['columns'] = [{'name': prop.name} for prop in attrs
                                     if prop.name != 'id']

            model_data['add_url'] = '{}/{}/add'.format(self.url_prefix, model_name)
            model_data['list_url'] = '{}/{}'.format(self.url_prefix, model_name)
            model_data['change_url'] = '{}/{}/change'.format(self.url_prefix, model_name)
            model_data['delete'] = '{}/{}/delete'.format(self.url_prefix, model_name)

            models_dict[model] = model_data
        return models_dict

    def get_model_list(self):
        models_dict = self._build_models_dict()
        return sorted(models_dict.values(), key=lambda x: x['name'].lower())


site = AdminSite()
