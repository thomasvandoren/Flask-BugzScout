#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name            ='Flask-BugzScout',
    version         =open('VERSION', 'r').read(),
    description     ='BugzScout extension for Flask.',
    long_description=open('README.rst').read(),
    author          ='Thomas Van Doren',
    author_email    ='thomas@thomasvandoren.com',
    maintainer      ='Thomas Van Doren',
    maintainer_email='thomas@thomasvandoren.com',
    url             ='https://github.com/thomasvandoren/Flask-BugzScout',
    keywords        =['BugzScout', 'Flask', 'FogBugz'],
    license         ='BSD',
    packages        =find_packages(exclude=('test',)),
    install_requires=[
        'requests',
        ],
    classifiers     =[
        'Development Status :: 3 - Alpha',
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
        ],
    entry_points    ={
        'console_scripts': [
            ]
        }
    )
