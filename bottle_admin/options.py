# coding: utf-8
from sqlalchemy import inspect


class ModelAdmin(object):
    """
    Extends the model to have admin functionalities
    """

    list_display = tuple()

    def __repr__(self):
        return "<ModelAdmin('{0}')>".format(self.name)

    def __init__(self, model, site):
        from .sites import site
        self.model_cls = model  # the model class
        self.site = site
        self.name = self.model_cls.__name__.lower()
        self.add_url = '{0}/{1}/add'.format(site.url_prefix, self.name)
        self.list_url = '{0}/{1}'.format(site.url_prefix, self.name)
        self.edit_url = '{0}/{1}/edit'.format(site.url_prefix, self.name)
        self.delete_url = '{0}/{1}/delete'.format(site.url_prefix, self.name)

    @property
    def columns(self):
        mapper = inspect(self.model_cls)
        attrs = [prop.columns[0] for prop in mapper.attrs]
        return (prop.name for prop in attrs if prop.name != 'id')

    def get_list_display(self):
        return self.list_display

    def get_select_fields(self):
        list_display = self.get_list_display()
        fields = []
        for field in list_display:
            attr = getattr(self.model_cls, field)
            try:
                attr = attr()
            except:
                pass
            fields.append(attr)
        return fields
