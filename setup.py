#!/usr/bin/env python

from distutils.core import setup

setup(name='Music Staff Live',
      version='1.0',
      description='Real time music staff reading and playing',
      author='Max Spiegelman',
      author_email='mspiegelman@wesleyan.edu',
      url='https://github.com/maxrosssp/music-staff-live',
      packages=['msl', 'msl.calibration', 'msl.parameters', 'msl.settings', 'msl.sight'],
      package_data={'msl.parameters': ['params/*.p']},
     )