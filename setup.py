#!/usr/bin/env python

from setuptools import setup, find_packages
setup(
    name="HelloWorld",
    version="0.1",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'flask',
        'flask-wtf',
        'flask-sqlalchemy',
        'flask-migrate',
        'flask-login',
        'flask-mail',
        'flask-bootstrap',
        'pyjwt',
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-spec'
    ]
)
