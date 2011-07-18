**********************
Installation procedure
**********************

Here is a quick and dirty guide, that will help you to install system in different cases.


.. _dependencies:

Dependencies
============
..
Following names of package are called so in debian package system::
..
  sudo apt-get install python git-core python-dev python-setuptools gettext


.. _development-environment:..

Development environment
=======================

Change directory to project's root.

Specific settings
-----------------

Create local settings (./src/settings/local.py)::

    AWS_ACCESS_KEY_ID = "PLACE YOUR KEY ID HERE"
    AWS_SECRET_ACCESS_KEY = "PLACE YOUR SECRET ACCESS EY"
    AWS_STORAGE_BUCKET_NAME = "zojax"
    DEBUG = True # For test purposes

    DATABASES = {
      'default': {
          'NAME': 'zojax',
          'ENGINE': 'django.db.backends.postgresql_psycopg2', #'django.db.backends.sqlite3',
          'USER': 'user',
          'PASSWORD': 'password',
      },
    }

   # For gmail account
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_HOST_USER = 'yourname@gmail.com'
   EMAIL_HOST_PASSWORD = 'your password'
   EMAIL_USE_TLS = True
   EMAIL_PORT = 587

   # Publicauth settings
   TWITTER_CONSUMER_KEY = "YOUR KEY"
   TWITTER_CONSUMER_SECRET = "YOUR SECRET"

Build project
-------------

Build project using buildout and run it::

  python ./bootstrap.py; ./bin/buildout; sudo ./bin/instance runserver 80


Test environment
----------------

Place "127.0.0.1    local.zojax.com" in your /etc/hosts file.

Go to http://local.zojax.com/admin/ to get into admin account:

- Default Admin account

  username/e-mail: admin
..
  password: admin

Go to  http://local.zojax.com/ for site functionality.


Production server
=================

Change directory to project's root.

For example: /opt/www/zojax/

Specific settings
-----------------

Create local settings (./src/settings/local.py)::

    AWS_ACCESS_KEY_ID = "PLACE YOUR KEY ID HERE"
    AWS_SECRET_ACCESS_KEY = "PLACE YOUR SECRET ACCESS EY"
    AWS_STORAGE_BUCKET_NAME = "zojax"

    DATABASES = {
      'default': {
          'NAME': 'zojax',
          'ENGINE': 'django.db.backends.postgresql_psycopg2', #'django.db.backends.sqlite3',
          'USER': 'user',
          'PASSWORD': 'password',
      },
    }

    DEBUG = False
    DEBUG_PROPAGATE_EXCEPTIONS = False
    SERVE_MEDIA = False

    # Appropriate email settings here

    MEDIA_URL = 'http://media.example.com/'

    ADMINS = (('admin', 'your@email.here'),)

Build project
-------------

Build project using buildout::

  python ./bootstrap.py; ./bin/buildout -c ./production.cfg

Admin account
-------------
..
Execute following command::
..
  ./bin/instance createsuperuser --email=your@email.here --username=admin

Enter password twice.


File system
-----------

Change permissions::
..
  $ chown -R  root:www-data zojax

Extra Information
=================

Testing application
-------------------
./bin/test test zojax

Tested in:
 - IE7,8
 - Opera 11.10
 - Mozilla Firefox 3.6
 - Google Chrome 12 (Windows, Linux)

3rd party dependencies
----------------------

- django - Web framework http://www.djangoproject.com/
- django-storages - support for dofferent django filestorage backends http://bitbucket.org/david/django-storages/wiki/Home
- django-debug-toolbar - A configurable set of panels that display various debug information http://pypi.python.org/pypi/django-debug-toolbar/0.8.4
- django-annoying - Django application that try to eliminate annoying things in Django framework https://bitbucket.org/offline/django-annoying/wiki/Home
- python-openid - OpenID support for servers and consumers http://pypi.python.org/pypi/python-openid/
- oauth - A python implementation of the signature logic associated with the OAuth 1.0 protocol http://code.daaku.org/python-oauth/
- django-publicauth - Django application that allows authenticate users through OpenID/OAuth https://bitbucket.org/offline/django-publicauth/wiki/Home
- jQuery - Javascript framework http://jquery.com/
- jQuery.form - AJAX form plugin http://jquery.malsup.com/form/
- Modernizr - open-source JavaScript library that helps you build the next generation of HTML5 and CSS3-powered websites. http://www.modernizr.com/