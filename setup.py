#!/usr/bin/env python3

from distutils.core import setup
from corpus import __version__

setup(
    name='corpus',
    version=__version__,
    author='Thomas Weigel',
    author_email='thomas.weigel@chantofwaves.com',
    url='https://github.com/github-te/core-utilities',
    description='toy project to reproduce core UNIX-like utilities in python'
    packages=['corpus', ],
    scripts=['bin/cat', ],
)
