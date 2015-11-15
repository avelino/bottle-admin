# coding: utf-8
from bottle import jinja2_view, redirect, request
from bottle_admin import site

from sqlalchemy.orm import sessionmaker


@jinja2_view('admin/index.html')
def home_view():
    return {'models': site.get_model_meta_list()}


@jinja2_view('admin/add.html')
def add_model_get_view(model_name):
    models = site.get_model_meta_list()
    for model in models:
        if model['name'] == model_name:
            return {'model': model}

    raise Exception(u'Requested model not found')


def add_model_post_view(model_name):
    fields = dict(request.forms)
    model_class = site.get_model_class(model_name)
    session = sessionmaker(bind=site.engine)()
    session.add(model_class(**fields))
    session.commit()
    return redirect('/admin/{}'.format(model_name))


@jinja2_view('admin/list.html')
def list_model_view(model_name):
    model_class = site.get_model_class(model_name)
    session = sessionmaker(bind=site.engine)()
    objects = list(session.query(model_class).all())
    def get_objects_as_list(objects):
        results = []
        for row in objects:
            row_list = []
            for col in row.__table__.columns:
                if col.name == 'id':
                    continue
                row_list.append((col.name, getattr(row, col.name)))
            results.append(row_list)
        return results
    return {
        'model_meta': site.get_model_meta(model_name),
        'results': get_objects_as_list(objects),
    }
