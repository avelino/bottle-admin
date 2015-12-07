# coding: utf-8


def get_object_as_list(obj):
    row_list = []
    for col in obj.__table__.columns:
        row_list.append((col.name, getattr(obj, col.name)))
    return row_list


def get_objects_as_list(objs):
    results = []
    for obj in objs:
        obj = get_object_as_list(obj)
        results.append(obj)
    return results
