### -*- coding: utf-8 -*- ####################################################
"""
Configuration file used by setuptools. It creates 'egg', install all dependencies.

$Id$
"""

import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# Dependencies - python eggs
install_requires = [
        'setuptools',
        'Django == 1.3',
        'django-storages'
]

# Extra dependencies for test purposes
extras_require = dict(
    test=[
        'coverage', #checks code coverage by tests 
        #'windmill', #browser tests
    ]
)

install_requires.extend(extras_require['test'])

# Execute function to handle setuptools functionality
setup(name="zojax",
    version="1.0",
    description="Zojax test task",
    author="blw0rm",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points="""
      # -*- Entry points: -*-
      """
)
