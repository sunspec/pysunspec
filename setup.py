#!/usr/bin/env python

"""
  Copyright (c) 2018, SunSpec Alliance
  All Rights Reserved

"""
from distutils.core import setup

setup(name = 'pysunspec',
      version = '2.0.0',
      description = 'Python SunSpec Tools',
      author = ['Bob Fox'],
      author_email = ['bob@sunspec.org'],
      classifiers = [
            'Operating System :: OS Independent',
            'Operating System :: POSIX :: Linux',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
      ],
      packages = ['sunspec', 'sunspec.core', 'sunspec.core.modbus', 'sunspec.core.test', 'sunspec.core.test.fake'],
      package_data = {'sunspec': ['models/smdx/*'], 'sunspec.core.test': ['devices/*']},
      scripts = ['scripts/suns.py'],
      python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
      install_requires = ['pyserial'],
      )
