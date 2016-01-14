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

    $FileInfo: motherless-dl.py - Last Update: 1/14/2016 Ver. 0.2.2 RC 1 - Author: cooldude2k $
'''

# https://raw.githubusercontent.com/GameMaker2k/Python-Scripts/master/MiniScripts/motherless-dl.py

from __future__ import division, absolute_import, print_function;
import re, os, sys, pymotherless, argparse;

__program_name__ = pymotherless.__program_name__;
__version_info__ = pymotherless.__version_info__;
__version_date__ = pymotherless.__version_date__;
__version__ = pymotherless.__version__;

geturls_cj = pymotherless.geturls_cj;
geturls_ua = pymotherless.geturls_ua;
geturls_ua_firefox_windows7 = pymotherless.geturls_ua_firefox_windows7;
geturls_ua_chrome_windows7 = pymotherless.geturls_ua_chrome_windows7;
geturls_ua_internet_explorer_windows7 = pymotherless.geturls_ua_internet_explorer_windows7;
geturls_headers = pymotherless.geturls_headers;
geturls_download_sleep = pymotherless.geturls_download_sleep;

parser = argparse.ArgumentParser(description="get urls of images/videos from motherless.com", conflict_handler="resolve", add_help=True);
parser.add_argument('-v', '--version', action='version', version=__program_name__+" "+__version__);
getargs = parser.parse_args();

