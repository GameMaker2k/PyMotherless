#!/usr/bin/env python

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2016 Cool Dude 2k - http://idb.berlios.de/
    Copyright 2016 Game Maker 2k - http://intdb.sourceforge.net/
    Copyright 2016 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: setup.py - Last Update: 02/04/2016 Ver. 0.3.3 RC 1 - Author: cooldude2k $
'''

import re, os, sys, time, datetime, platform, pkg_resources;
from setuptools import setup, find_packages;

setup(
 name = 'PyMotherless',
 version = '0.3.3',
 author = 'Kazuki Przyborowski',
 author_email = 'kazuki.przyborowski@gmail.com',
 maintainer = 'Kazuki Przyborowski',
 maintainer_email = 'kazuki.przyborowski@gmail.com',
 description = 'Get urls of images/videos from motherless.',
 license = 'Revised BSD License',
 keywords = 'motherless pymotherless python python-motherless',
 url = 'https://github.com/GameMaker2k/PyMotherless',
 download_url = 'https://github.com/GameMaker2k/PyMotherless/archive/master.tar.gz',
 long_description = 'Get urls of images/videos from motherless.',
 platforms = 'OS Independent',
 zip_safe = True,
 py_modules = ['pymotherless'],
 classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Intended Audience :: Other Audience',
  'License :: OSI Approved',
  'License :: OSI Approved :: BSD License',
  'Natural Language :: English',
  'Operating System :: MacOS',
  'Operating System :: MacOS :: MacOS X',
  'Operating System :: Microsoft',
  'Operating System :: Microsoft :: Windows',
  'Operating System :: OS/2',
  'Operating System :: OS Independent',
  'Operating System :: POSIX',
  'Operating System :: Unix',
  'Programming Language :: Python',
  'Topic :: Utilities',
  'Topic :: Software Development',
  'Topic :: Software Development :: Libraries',
  'Topic :: Software Development :: Libraries :: Python Modules',
 ],
)
