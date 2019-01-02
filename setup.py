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
      packages = ['sunspec', 'sunspec.core', 'sunspec.core.modbus', 'sunspec.core.test', 'sunspec.core.test.fake'],
      package_data = {'sunspec': ['models/smdx/*'], 'sunspec.core.test': ['devices/*']},
      scripts = ['scripts/suns.py'],
      install_requires = ['pyserial'],
      )
