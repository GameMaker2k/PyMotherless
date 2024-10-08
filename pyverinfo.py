#!/usr/bin/python2

import json
import os
import re
import subprocess
import sys

pyexecpath = os.path.realpath(sys.executable)
pkgsetuppy = os.path.realpath("." + os.path.sep + "setup.py")
pypkgenlistp = subprocess.Popen([pyexecpath,
                                 pkgsetuppy,
                                 "getversioninfo"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
pypkgenout, pypkgenerr = pypkgenlistp.communicate()
if (sys.version[0] == "3"):
    pypkgenout = pypkgenout.decode('utf-8')
pyconfiginfo = json.loads(pypkgenout)
print(pypkgenout)
