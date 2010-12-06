#!/usr/bin/env python
import os

from setuptools import setup, find_packages

from sitegen import VERSION, PROJECT


MODULE_NAME = 'sitegen'
PACKAGE_DATA = [ '*.ini' ]

for root, dirs, files in os.walk( os.path.join( MODULE_NAME, 'templates' ) ):
    for filename in files:
        PACKAGE_DATA.append("%s/%s" % ( root[len(MODULE_NAME)+1:], filename ))


def read( fname ):
    try:
        return open( os.path.join( os.path.dirname( __file__ ), fname ) ).read()
    except IOError:
        return ''


META_DATA = dict(
    name=PROJECT,
    version=VERSION,
    description=read( 'DESCRIPTION' ),
    long_description=read( 'README.rst' ),
    license='GNU LGPL',

    author='Kirill Klenov',
    author_email='horneds@gmail.com',

    url=' http://github.com/klen',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Environment :: Console',
        'License :: Public domain',
    ],

    platforms=('Any'),

    scripts=map( lambda x: 'scripts/' + x, os.listdir( 'scripts' )),

    packages=find_packages(),
    package_data = { '': PACKAGE_DATA, },

    entry_points={
        'console_scripts': [
            'sitegen = sitegen.main:main',
        ]
    },
)


if __name__ == "__main__":
    setup( **META_DATA )

