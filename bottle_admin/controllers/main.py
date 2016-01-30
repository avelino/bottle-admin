# coding: utf-8
from bottle import jinja2_view, redirect, request
from bottle_admin import site
from bottle_admin.auth import get_aaa
from bottle_admin.helpers import get_object_as_list, get_objects_as_list

from sqlalchemy.orm import sessionmaker


@jinja2_view('admin/index.html')
def home_controller():
    aaa = get_aaa()
    aaa.require(fail_redirect='/admin/login')
    return {'models': site.get_models()}


@jinja2_view('admin/add.html')
def add_model_get_controller(model_name):
    aaa = get_aaa()
    aaa.require(fail_redirect='/admin/login')

    model = site.get_model(model_name)
    return {'model': model}


def add_model_post_controller(model_name):
    aaa = get_aaa()
    aaa.require(fail_redirect='/admin/login')

    fields = dict(request.forms)
    model = site.get_model(model_name)
    session = sessionmaker(bind=site.engine)()
    try:
        obj = model.model_cls(**fields)
    except TypeError:
        return u'{0} object not created. Not enough data'.format(model_name)
    session.add(obj)
    session.commit()
    return redirect('/admin/{0}'.format(model.name))


def delete_model_controller(model_name, model_id):
    aaa = get_aaa()
    aaa.require(fail_redirect='/admin/login')

    model = site.get_model(model_name)
    session = sessionmaker(bind=site.engine)()
    obj = session.query(model.model_cls).get(model_id)
    if not obj:
        return u'{0}: {1} not found'.format(model.name, model_id)
    session.delete(obj)
    session.commit()
    return redirect('/admin/{0}'.format(model.name))


@jinja2_view('admin/edit.html')
def edit_model_get_controller(model_name, model_id):
    aaa = get_aaa()
    aaa.require(fail_redirect='/admin/login')

    model = site.get_model(model_name)
    session = sessionmaker(bind=site.engine)()
    obj = session.query(model.model_cls).get(model_id)
    if not obj:
        return u'{0} {1} not found'.format(model.name, model_id)
    obj.as_list = get_object_as_list(model, obj)
    return {
        'model': model,
        'obj': obj
    }


@jinja2_view('admin/edit.html')
def edit_model_post_controller(model_name, model_id):
    aaa = get_aaa()
    aaa.require(fail_redirect='/admin/login')

    model = site.get_model(model_name)
    session = sessionmaker(bind=site.engine)()
    obj = session.query(model.model_cls).get(model_id)
    fields = dict(request.forms)
    for column, value in fields.items():
        setattr(obj, column, value)
    if not obj:
        return u'{0} {1} object not found'.format(model_name, model_id)
    session.add(obj)
    session.commit()
    session.close()
    return redirect('/admin/{0}'.format(model_name))


@jinja2_view('admin/list.html')
def list_model_controller(model_name):
    aaa = get_aaa()
    aaa.require(fail_redirect='/admin/login')

    model = site.get_model(model_name)
    session = sessionmaker(bind=site.engine)()
    fields = model.get_select_fields()
    objects = list(session.query(model.model_cls.id, *fields).all())

    return {
        'model': model,
        'results': get_objects_as_list(model, objects),
    }
