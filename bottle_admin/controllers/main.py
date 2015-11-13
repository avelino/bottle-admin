# coding: utf-8
from bottle import jinja2_view
import bottle_admin


@jinja2_view('admin/index.html')
def home_view():
    return {'models': bottle_admin.site.get_model_list()}


@jinja2_view('admin/add.html')
def add_model_view(model_name):
    models = bottle_admin.site.get_model_list()
    for model in models:
        if model['name'] == model_name:
            return {'model': model}

    raise Exception(u'Requested model not found')
