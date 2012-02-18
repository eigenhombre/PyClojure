#!/usr/bin/env python
from os.path import exists
try:
    # Use setup() from setuptools(/distribute) if available
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from pyclojure import __version__

setup(
    name='PyClojure',
    version=__version__,
    # Your name & email here
    author='John Jacobsen',
    author_email='john@mail.npxdesigns.com',
    # If you had pyclojure.tests, you would also include that in this list
    packages=['pyclojure'],
    # Any executable scripts, typically in 'bin'. E.g 'bin/do-something.py'
    scripts=[],
    url='https://github.com/eigenhombre/PyClojure',
    license='',
    description='Clojure implemented on top of Python',
    long_description=open('README').read() if exists("README") else "",
    entry_points=dict(console_scripts=['pyclojure=pyclojure.repl:main']),
    install_requires=[
        'ply>=3.4',
        'funktown>=0.4.4'
    ],
)
