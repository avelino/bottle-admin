# coding: utf-8


def get_object_as_list(model, obj):
    """Get the SQLAlchemy query result as a list of tuples"""

    list_display = model.get_list_display()
    result = [('id', obj.id)]
    result += [(col, getattr(obj, col)) for col in list_display]
    print(result)
    return result


def get_objects_as_list(model, objs):
    """Get a list of SQLAlchemy queries as a list of list of tuples"""
    return [get_object_as_list(model, obj) for obj in objs]
