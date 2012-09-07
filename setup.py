#!/usr/bin/env python
# coding: utf-8
import os
from sys import version_info

from setuptools import setup, find_packages

from makesite import __version__, __project__, __license__


PACKAGE_DATA = ['*.ini', '*.sh']

for folder in ['templates', 'modules']:
    for root, dirs, files in os.walk(os.path.join(__project__, folder)):
        for filename in files:
            PACKAGE_DATA.append("%s/%s" % (root[len(__project__) + 1:], filename))


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


install_requires = ['INITools==0.3.1', 'Tempita==0.5.1', 'ssh==1.7.14']
if version_info < (2, 7):
    install_requires.append('argparse')


META_DATA = dict(
    name=__project__,
    version=__version__,
    license=__license__,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    platforms=('Any'),

    author='Kirill Klenov',
    author_email='horneds@gmail.com',
    url=' http://github.com/klen/makesite',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: Russian',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Programming Language :: Python',
        'Environment :: Console',
        'Topic :: Software Development :: Code Generators',
    ],

    packages=find_packages(),
    package_data={'': PACKAGE_DATA},

    entry_points={
        'console_scripts': [
            'makesite = makesite.main:console',
        ]
    },

    install_requires=install_requires,
    test_suite='tests',
)


if __name__ == "__main__":
    setup(**META_DATA)
