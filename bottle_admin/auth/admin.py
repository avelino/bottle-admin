# coding: utf-8
from bottle_admin.options import ModelAdmin


class RoleAdmin(ModelAdmin):
    list_display = ('role', 'level')


class UserAdmin(ModelAdmin):
    list_display = ('username', 'role', 'email_addr', 'creation_date', 'last_login')
