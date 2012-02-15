#!/usr/bin/env python
from os.path import exists
from setuptools import setup
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
    # Any requirements here, e.g. "Django >= 1.1.1"
    install_requires=[
        'ply>=3.4',
    ],
)
