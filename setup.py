#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Flask-BugzScout
===============

`BugzScout <https://pypi.python.org/pypi/bugzscout>`_ extension for Flask.
"""

from setuptools import find_packages, setup

setup(
    name                ='Flask-BugzScout',
    version             =open('VERSION', 'r').read(),
    description         ='BugzScout extension for Flask.',
    long_description    =open('README.rst').read(),
    author              ='Thomas Van Doren',
    author_email        ='thomas@thomasvandoren.com',
    maintainer          ='Thomas Van Doren',
    maintainer_email    ='thomas@thomasvandoren.com',
    url                 ='https://github.com/thomasvandoren/Flask-BugzScout',
    keywords            =['BugzScout', 'Flask', 'FogBugz'],
    license             ='BSD',
    packages            =find_packages(exclude=('test',)),
    zip_safe            =False,
    include_package_data=True,
    platforms           ='any',
    install_requires    =[
        'bugzscout',
        'Flask',
        ],
    classifiers         =[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # 'Programming Language :: Python :: 2.6',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3.1',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ]
    )
