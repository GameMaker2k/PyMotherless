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

    $FileInfo: pymotherless-demo.py - Last Update: 1/30/2019 Ver. 0.4.7 RC 4 - Author: cooldude2k $
'''

from __future__ import division, absolute_import, print_function;
import re, os, sys, pymotherless, argparse;
import logging as log;

__project__ = pymotherless.__project__;
__program_name__ = pymotherless.__program_name__;
__project_url__ = pymotherless.__project_url__;
__version_info__ = pymotherless.__version_info__;
__version_date_info__ = pymotherless.__version_date_info__;
__version_date__ = pymotherless.__version_date__;
__version_date_plusrc__ = pymotherless.__version_date_plusrc__
__version__ = pymotherless.__version__;
__version_date_plusrc__ = pymotherless.__version_date_plusrc__;

geturls_cj = pymotherless.geturls_cj;
geturls_ua = pymotherless.geturls_ua;
geturls_ua_firefox_windows7 = pymotherless.geturls_ua_firefox_windows7;
geturls_ua_seamonkey_windows7 = pymotherless.geturls_ua_seamonkey_windows7;
geturls_ua_chrome_windows7 = pymotherless.geturls_ua_chrome_windows7;
geturls_ua_chromium_windows7 = pymotherless.geturls_ua_chromium_windows7;
geturls_ua_palemoon_windows7 = pymotherless.geturls_ua_palemoon_windows7;
geturls_ua_opera_windows7 = pymotherless.geturls_ua_opera_windows7;
geturls_ua_vivaldi_windows7 = pymotherless.geturls_ua_chromium_windows7;
geturls_ua_internet_explorer_windows7 = pymotherless.geturls_ua_internet_explorer_windows7;
geturls_ua_microsoft_edge_windows7 = pymotherless.geturls_ua_microsoft_edge_windows7;
geturls_ua_pymotherless_python = pymotherless.geturls_ua_pymotherless_python;
geturls_ua_pymotherless_python_alt = pymotherless.geturls_ua_pymotherless_python_alt;
geturls_ua_googlebot_google = pymotherless.geturls_ua_googlebot_google;
geturls_ua_googlebot_google_old = pymotherless.geturls_ua_googlebot_google_old;
geturls_headers = pymotherless.geturls_headers;
geturls_headers_firefox_windows7 = pymotherless.geturls_headers_firefox_windows7;
geturls_headers_seamonkey_windows7 = pymotherless.geturls_headers_seamonkey_windows7;
geturls_headers_chrome_windows7 = pymotherless.geturls_headers_chrome_windows7;
geturls_headers_chromium_windows7 = pymotherless.geturls_headers_chromium_windows7;
geturls_headers_palemoon_windows7 = pymotherless.geturls_headers_palemoon_windows7;
geturls_headers_opera_windows7 = pymotherless.geturls_headers_opera_windows7;
geturls_headers_vivaldi_windows7 = pymotherless.geturls_headers_vivaldi_windows7;
geturls_headers_internet_explorer_windows7 = pymotherless.geturls_headers_internet_explorer_windows7;
geturls_headers_microsoft_edge_windows7 = pymotherless.geturls_headers_microsoft_edge_windows7;
geturls_headers_pymotherless_python = pymotherless.geturls_headers_pymotherless_python;
geturls_headers_pymotherless_python_alt = pymotherless.geturls_headers_pymotherless_python_alt;
geturls_headers_googlebot_google = pymotherless.geturls_headers_googlebot_google;
geturls_headers_googlebot_google_old = pymotherless.geturls_headers_googlebot_google_old;
geturls_download_sleep = pymotherless.geturls_download_sleep;

parser = argparse.ArgumentParser(description="get urls of images/videos from motherless.com", conflict_handler="resolve", add_help=True);
parser.add_argument('-v', '--version', action='version', version=__program_name__+" "+__version__);
parser.add_argument("-V", "--verbose", action = "store_true", help = "print various debugging information");
getargs = parser.parse_args();

if(getargs.verbose==True):
 log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG);

