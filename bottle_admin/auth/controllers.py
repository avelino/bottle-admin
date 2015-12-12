# coding: utf-8
from bottle import jinja2_view, request
from bottle_admin.auth import get_aaa


@jinja2_view('admin/login.html')
def login_get_controller():
    return {}


def login_post_controller():
    username = request.forms.get('username')
    password = request.forms.get('password')
    aaa = get_aaa()
    aaa.login(username, password, success_redirect='/admin',
              fail_redirect='/admin/login')


def logout_controller():
    aaa = get_aaa()
    aaa.logout(success_redirect='/admin/login')
