from bottle import TEMPLATE_PATH
import os

from .sites import site

__all__ = ['site', 'AdminSite']


ADMIN_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)))
TEMPLATE_PATH.insert(1, os.path.join(ADMIN_PATH, 'views'))
