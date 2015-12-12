bottle-admin
============
[![Build Status](https://travis-ci.org/avelino/bottle-admin.svg?branch=master)](https://travis-ci.org/avelino/bottle-admin) [![Coverage Status](https://coveralls.io/repos/avelino/bottle-admin/badge.svg?branch=master&service=github)](https://coveralls.io/github/avelino/bottle-admin?branch=master)

Simple and extensible administrative interface framework for Bottle, based on the bottle-boilerplate. Bottle-admin uses the project and app structures from bottle-boilerplate.

## How to use
Install bottle-admin
```
pip install git+git://github.com/avelino/bottle-admin.git@master
```
Start your project and app with [bottle-boilerplate](https://github.com/avelino/bottle-boilerplate)
```
bottle-boilerplate startproject YOUR-PROJECT
cd YOUR-PROJECT
python manage.py startapp YOUR-APP
```
Edit the manage.py file and add the following line:
```python
from bottle_admin import site
site.setup(engine)
```
To register your SQLAlchemy models for using inside admin:
```python
site.register(YourModel)
```
