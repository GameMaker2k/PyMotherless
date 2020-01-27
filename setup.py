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

    $FileInfo: setup.py - Last Update: 1/30/2019 Ver. 0.4.7 RC 4 - Author: cooldude2k $
'''

import re, os, sys, time, datetime, platform, pkg_resources;
from setuptools import setup, find_packages;

verinfofilename = os.path.realpath("."+os.path.sep+os.path.sep+"pymotherless.py");
verinfofile = open(verinfofilename, "r");
verinfodata = verinfofile.read();
verinfofile.close();
setuppy_verinfo_esc = re.escape("__version_info__ = (")+"(.*)"+re.escape(");");
setuppy_verinfo = re.findall(setuppy_verinfo_esc, verinfodata)[0];
setuppy_verinfo_exp = [vergetspt.strip().replace("\"", "") for vergetspt in setuppy_verinfo.split(',')];
setuppy_dateinfo_esc = re.escape("__version_date_info__ = (")+"(.*)"+re.escape(");");
setuppy_dateinfo = re.findall(setuppy_dateinfo_esc, verinfodata)[0];
setuppy_dateinfo_exp = [vergetspt.strip().replace("\"", "") for vergetspt in setuppy_dateinfo.split(',')];
pymodule = {};
pymodule['version'] = str(setuppy_verinfo_exp[0])+"."+str(setuppy_verinfo_exp[1])+"."+str(setuppy_verinfo_exp[2]);
pymodule['versionrc'] = int(setuppy_verinfo_exp[4]);
pymodule['versionlist'] = (int(setuppy_verinfo_exp[0]), int(setuppy_verinfo_exp[1]), int(setuppy_verinfo_exp[2]), str(setuppy_verinfo_exp[3]), int(setuppy_verinfo_exp[4]));
pymodule['verdate'] = str(setuppy_dateinfo_exp[0])+"."+str(setuppy_dateinfo_exp[1])+"."+str(setuppy_dateinfo_exp[2]);
pymodule['verdaterc'] = int(setuppy_dateinfo_exp[4]);
pymodule['verdatelist'] = (int(setuppy_dateinfo_exp[0]), int(setuppy_dateinfo_exp[1]), int(setuppy_dateinfo_exp[2]), str(setuppy_dateinfo_exp[3]), int(setuppy_dateinfo_exp[4]));
pymodule['name'] = 'PyMotherless';
pymodule['author'] = 'Kazuki Przyborowski';
pymodule['authoremail'] = 'kazuki.przyborowski@gmail.com';
pymodule['maintainer'] = 'Kazuki Przyborowski';
pymodule['maintaineremail'] = 'kazuki.przyborowski@gmail.com';
pymodule['description'] = 'Get urls of images/videos from motherless.';
pymodule['license'] = 'Revised BSD License';
pymodule['keywords'] = 'motherless pymotherless python python-motherless';
pymodule['url'] = 'https://github.com/GameMaker2k/PyMotherless';
pymodule['downloadurl'] = 'https://github.com/GameMaker2k/PyMotherless/archive/master.tar.gz';
pymodule['longdescription'] = 'Get urls of images/videos from motherless.';
pymodule['platforms'] = 'OS Independent';
pymodule['zipsafe'] = True;
pymodule['pymodules'] = ['pymotherless'];
pymodule['scripts'] = ['pymotherless-demo.py', 'pymotherless-dl.py', 'pymotherless-httpd.py'];
pymodule['classifiers'] = [
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
 'Topic :: Software Development :: Libraries :: Python Modules'
];
if(len(sys.argv)>1 and (sys.argv[1]=="versioninfo" or sys.argv[1]=="getversioninfo")):
 import json;
 pymodule_data = json.dumps(pymodule);
 print(pymodule_data);
 sys.exit();
if(len(sys.argv)>1 and (sys.argv[1]=="sourceinfo" or sys.argv[1]=="getsourceinfo")):
 srcinfofilename = os.path.realpath("."+os.path.sep+pkg_resources.to_filename(pymodule['name'])+".egg-info"+os.path.sep+"SOURCES.txt");
 srcinfofile = open(srcinfofilename, "r");
 srcinfodata = srcinfofile.read();
 srcinfofile.close();
 srcinfolist = srcinfodata.split('\n');
 srcfilelist = "";
 srcpdir = os.path.basename(os.path.dirname(os.path.realpath(__file__)));
 for ifile in srcinfolist:
  srcfilelist = "."+os.path.sep+srcpdir+os.path.sep+ifile+" "+srcfilelist;
 print(srcfilelist);
 sys.exit();
if(len(sys.argv)>1 and sys.argv[1]=="cleansourceinfo"):
 os.system("rm -rfv \""+os.path.realpath("."+os.path.sep+"dist\""));
 os.system("rm -rfv \""+os.path.realpath("."+os.path.sep+pkg_resources.to_filename(pymodule['name'])+".egg-info\""));
 sys.exit();

setup(
 name = pymodule['name'],
 version = pymodule['version'],
 author = pymodule['author'],
 author_email = pymodule['authoremail'],
 maintainer = pymodule['maintainer'],
 maintainer_email = pymodule['maintaineremail'],
 description = pymodule['description'],
 license = pymodule['license'],
 keywords = pymodule['keywords'],
 url = pymodule['url'],
 download_url = pymodule['downloadurl'],
 long_description = pymodule['longdescription'],
 platforms = pymodule['platforms'],
 zip_safe = pymodule['zipsafe'],
 py_modules = pymodule['pymodules'],
 scripts = pymodule['scripts'],
 classifiers = pymodule['classifiers']
)
