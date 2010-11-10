#!/usr/bin/env python

from setuptools import setup, find_packages
import os
from sitegen import VERSION

package_data = [ '*.ini' ]
for root, dirs, files in os.walk( 'sitegen/templates' ):
    if files:
        package_data.append(root[8:] + '/*')

setup(name='sitegen',
    version=VERSION,
    description='sitegen: generate site structure',
    long_description="Simple script for make site structure.",
    author='Kirill Klenov',
    author_email='horneds@gmail.com',
    url=' http://github.com/klen',
    packages=find_packages(),
    package_data = { '': package_data, },
    entry_points={
        'console_scripts': [
            'sitegen = sitegen.main:main',
        ]
    },
    classifiers=[
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: Public domain',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Unix',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Topic :: Software Development',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: System :: Clustering',
          'Topic :: System :: Software Distribution',
          'Topic :: System :: Systems Administration',
    ],
)
