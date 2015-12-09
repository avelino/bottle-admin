# coding: utf-8
from bottle import jinja2_view, redirect, request
from bottle_admin import site
from bottle_admin.helpers import get_object_as_list, get_objects_as_list

from sqlalchemy.orm import sessionmaker


@jinja2_view('admin/index.html')
def home_controller():
    return {'models': site.get_model_meta_list()}


@jinja2_view('admin/add.html')
def add_model_get_controller(model_name):
    meta = site.get_model_meta(model_name)
    return {'model': meta}


def add_model_post_controller(model_name):
    fields = dict(request.forms)
    model_class = site.get_model_class(model_name)
    session = sessionmaker(bind=site.engine)()
    session.add(model_class(**fields))
    session.commit()
    return redirect('/admin/{0}'.format(model_name))


def delete_model_controller(model_name, model_id):
    model_class = site.get_model_class(model_name)
    session = sessionmaker(bind=site.engine)()
    obj = session.query(model_class).get(model_id)
    if not obj:
        return u'{0}: {1} not found'.format(model_class.__name__, model_id)
    session.delete(obj)
    session.commit()
    return redirect('/admin/{0}'.format(model_name))


@jinja2_view('admin/edit.html')
def edit_model_get_controller(model_name, model_id):
    meta = site.get_model_meta(model_name)
    session = sessionmaker(bind=site.engine)()
    obj = session.query(meta['model_class']).get(model_id)
    if not obj:
        return u'{0} {1} not found'.format(meta['model_class'].__name__, model_id)
    obj.as_list = get_object_as_list(obj)
    return {
        'meta': meta,
        'model': obj
    }


@jinja2_view('admin/edit.html')
def edit_model_post_controller(model_name, model_id):
    model_class = site.get_model_class(model_name)
    session = sessionmaker(bind=site.engine)()
    obj = session.query(model_class).get(model_id)
    fields = dict(request.forms)
    for column, value in fields.items():
        setattr(obj, column, value)
    session.add(obj)
    session.commit()
    return redirect('/admin/{0}'.format(model_name))


@jinja2_view('admin/list.html')
def list_model_controller(model_name):
    model_class = site.get_model_class(model_name)
    session = sessionmaker(bind=site.engine)()
    objects = list(session.query(model_class).all())

    return {
        'model_meta': site.get_model_meta(model_name),
        'results': get_objects_as_list(objects),
    }
