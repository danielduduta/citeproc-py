#!/usr/bin/env python

"""
Setup script for citeproc-py
"""

import os
import re
import sys

from datetime import datetime
from subprocess import Popen, PIPE
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop


PACKAGE = 'citeproc'
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
PACKAGE_ABSPATH = os.path.join(BASE_PATH, PACKAGE)

# All external commands are relative to BASE_PATH
os.chdir(BASE_PATH)


def long_description():
    with open(os.path.join(BASE_PATH, 'README.rst')) as readme:
        result = readme.read()
    result += '\n\n'
    with open(os.path.join(BASE_PATH, 'CHANGES.rst')) as changes:
        result += changes.read()
    return result


CSL_SCHEMA_RNC = 'citeproc/data/schema/csl.rnc'

def convert_rnc():
    import rnc2rng

    filename_root, _ = os.path.splitext(CSL_SCHEMA_RNC)
    with open(CSL_SCHEMA_RNC, 'r') as rnc:
        root = rnc2rng.load(rnc)
    with open(filename_root + '.rng', 'w') as rng:
        rnc2rng.dump(root, rng)


class custom_build_py(build_py):
    def run(self):
        convert_rnc()
        build_py.run(self)


class custom_develop(develop):
    def run(self):
        convert_rnc()
        develop.run(self)


setup(
    name='citeproc-py',
    version='0.5.5',
    cmdclass = dict(build_py=custom_build_py, develop=custom_develop),
    packages=find_packages(),
    package_data={PACKAGE: ['data/locales/*.xml',
                            'data/locales/locales.json',
                            'data/schema/*.rng',
                            'data/styles/*.csl',
                            'data/styles/dependent/*.csl']},
    scripts=['bin/csl_unsorted'],
    setup_requires=['rnc2rng==2.6'],
    install_requires=['lxml'],
    provides=[PACKAGE],
    #test_suite='nose.collector',

    author='Brecht Machiels',
    author_email='brecht@mos6581.org',
    description='Citations and bibliography formatter',
    long_description=long_description(),
    url='https://github.com/brechtm/citeproc-py',
    keywords='csl citation html rst bibtex xml',
    license='2-clause BSD License',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Other Environment',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Legal Industry',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Documentation',
        'Topic :: Printing',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
