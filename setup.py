#!/usr/bin/env python
import os

from setuptools import setup, find_packages

from sitegen import VERSION


package_data = [ '*.ini' ]
for root, dirs, files in os.walk( 'sitegen/templates' ):
    for filename in files:
        package_data.append("%s/%s" % ( root[8:], filename ))

setup(name='sitegen',
    version=VERSION,

    description='sitegen: generate site structure',
    long_description="Simple script for make site structure.",

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

    scripts=['sitegenwrapper.sh', 'installsite', 'updatesite', 'removesite', 'sitegenparse'],

    packages=find_packages(),
    package_data = { '': package_data, },

    entry_points={
        'console_scripts': [
            'sitegen = sitegen.main:main',
        ]
    },
)
