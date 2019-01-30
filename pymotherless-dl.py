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

    $FileInfo: pymotherless-dl.py - Last Update: 1/30/2019 Ver. 0.4.7 RC 4 - Author: cooldude2k $
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
parser.add_argument("url", help="motherless url");
parser.add_argument("-v", "--version", action="version", version=__program_name__+" "+__version__);
parser.add_argument("-U", "--update", action="store_true", help="update this program to latest version. Make sure that you have sufficient permissions (run with sudo if needed)");
parser.add_argument("-d", "--dump-user-agent", action="store_true", help="display the current browser identification");
parser.add_argument("-u", "--user-agent", default=geturls_ua_firefox_windows7, help="specify a custom user agent");
parser.add_argument("-r", "--referer", default="http://motherless.com/", help="specify a custom referer, use if the video access");
parser.add_argument("-g", "--get-url", action="store_true", help="simulate, quiet but print URL");
parser.add_argument("-p", "--get-pageurl", action="store_true", help="simulate, quiet but print URL");
parser.add_argument("-e", "--get-title", action="store_true", help="simulate, quiet but print title");
parser.add_argument("-i", "--get-id", action="store_true", help="simulate, quiet but print id");
parser.add_argument("-t", "--get-thumbnail", action="store_true", help="simulate, quiet but print thumbnail URL");
parser.add_argument("-f", "--get-filename", action="store_true", help="simulate, quiet but print output filename");
parser.add_argument("-u", "--get-username", action="store_true", help="simulate, quiet but print uploaders username");
parser.add_argument("-i", "--get-views", action="store_true", help="simulate, quiet but print number of views");
parser.add_argument("-f", "--get-favorites", action="store_true", help="simulate, quiet but print number of favorites");
parser.add_argument("-o", "--output-directory", default=os.path.realpath(os.getcwd()), help="specify a directory to output file to");
parser.add_argument("-l", "--use-httplib", default="urllib", help="select library to download file can be urllib or requests or mechanize");
parser.add_argument("-b", "--set-buffersize", default=524288, type=int, help="set how big buffersize is in bytes. how much it will download");
parser.add_argument("-V", "--verbose", action="store_true", help="print various debugging information");
getargs = parser.parse_args();

if(not pymotherless.check_httplib_support(getargs.use_httplib)):
 getargs.use_httplib = "urllib";

getargs_cj = geturls_cj;
getargs_headers = {'Referer': getargs.referer, 'User-Agent': getargs.user_agent, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"};

getargs.output_directory = os.path.realpath(getargs.output_directory);

if(getargs.verbose==True):
 log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG);

if(getargs.dump_user_agent==True):
 print(getargs.user_agent);
 sys.exit();

motherless_linktype = pymotherless.get_motherless_link_type(getargs.url);
motherless_links = [];
motherless_links_dir = [];
if(motherless_linktype=="link"):
 motherless_links.append(getargs.url);
if(motherless_linktype=="gallery"):
 numpages = pymotherless.get_motherless_number_of_pages(getargs.url, getargs_headers, getargs_cj, getargs.use_httplib);
 numcount = 1;
 while(numcount <= numpages):
  getlinks = pymotherless.get_motherless_galleries_links(getargs.url, getargs_headers, getargs_cj, getargs.use_httplib, page=numcount);
  innumlinks = getlinks['numoflinks'];
  innumcount = 0;
  while(innumcount < innumlinks):
   inmotherless_linktype = pymotherless.get_motherless_link_type(getlinks[innumcount]['url']);
   if(inmotherless_linktype=="link"):
    motherless_links_dir.append(getargs.url.rsplit('/', 1)[-1]);
    motherless_links.append(getlinks[innumcount]['url']);
   if(inmotherless_linktype=="gallery"):
    innumpages = pymotherless.get_motherless_number_of_pages(getlinks[innumcount]['url'], getargs_headers, getargs_cj, getargs.use_httplib);
    innumcountpages = 1;
    while(innumcountpages <= innumpages):
     ingetlinks = pymotherless.get_motherless_galleries_links(getlinks[innumcount]['url'], getargs_headers, getargs_cj, getargs.use_httplib, page=innumcountpages);
     ininnumlinks = ingetlinks['numoflinks'];
     ininnumcount = 0;
     while(ininnumcount < ininnumlinks):
      ininmotherless_linktype = pymotherless.get_motherless_link_type(ingetlinks[ininnumcount]['url']);
      if(ininmotherless_linktype=="link"):
       motherless_links_dir.append(getlinks[innumcount]['url'].rsplit('/', 1)[-1]);
       motherless_links.append(ingetlinks[ininnumcount]['url']);
      ininnumcount = ininnumcount + 1;
     innumcountpages = innumcountpages + 1;
   innumcount = innumcount + 1;
  numcount = numcount + 1;
if(motherless_linktype=="board"):
 getlinks = pymotherless.get_motherless_boards_links(getargs.url, getargs_headers, getargs_cj, getargs.use_httplib);
 innumlinks = getlinks['numoflinks'];
 innumcount = 0;
 while(innumcount < innumlinks):
  inmotherless_linktype = pymotherless.get_motherless_link_type(getlinks[innumcount]['url']);
  if(inmotherless_linktype=="link"):
   motherless_links_dir.append(getargs.url.rsplit('/', 1)[-1]);
   motherless_links.append(getlinks[innumcount]['url']);
  innumcount = innumcount + 1;

if(getargs.get_url==True):
 listsize = len(motherless_links);
 listcount = 0;
 while(listcount < listsize):
  print(pymotherless.get_motherless_links(motherless_links[listcount], getargs_headers, getargs_cj, getargs.use_httplib)['url']);
  listcount = listcount + 1;

if(getargs.get_pageurl==True):
 listsize = len(motherless_links);
 listcount = 0;
 while(listcount < listsize):
  print(motherless_links[listcount]);
  listcount = listcount + 1;

if(getargs.get_filename==True):
 listsize = len(motherless_links);
 listcount = 0;
 while(listcount < listsize):
  print(pymotherless.get_motherless_links(motherless_links[listcount], getargs_headers, getargs_cj, getargs.use_httplib)['fullfilename']);
  listcount = listcount + 1;

if(getargs.get_title==True):
 listsize = len(motherless_links);
 listcount = 0;
 while(listcount < listsize):
  print(pymotherless.get_motherless_links(motherless_links[listcount], getargs_headers, getargs_cj, getargs.use_httplib)['title']);
  listcount = listcount + 1;

if(getargs.get_username==True):
 listsize = len(motherless_links);
 listcount = 0;
 while(listcount < listsize):
  print(pymotherless.get_motherless_links(motherless_links[listcount], getargs_headers, getargs_cj, getargs.use_httplib)['username']);
  listcount = listcount + 1;

if(getargs.get_views==True):
 listsize = len(motherless_links);
 listcount = 0;
 while(listcount < listsize):
  print(pymotherless.get_motherless_links(motherless_links[listcount], getargs_headers, getargs_cj, getargs.use_httplib)['numberofviews']);
  listcount = listcount + 1;

if(getargs.get_favorites==True):
 listsize = len(motherless_links);
 listcount = 0;
 while(listcount < listsize):
  print(pymotherless.get_motherless_links(motherless_links[listcount], getargs_headers, getargs_cj, getargs.use_httplib)['numberoffavorites']);
  listcount = listcount + 1;

if(getargs.get_url==False and getargs.get_pageurl==False and getargs.get_thumbnail==False and getargs.get_filename==False and getargs.get_title==False and getargs.get_username==False and getargs.get_views==False and getargs.get_favorites==False):
 listsize = len(motherless_links);
 listcount = 0;
 while(listcount < listsize):
  listcountalt = listcount + 1;
  percentage = str("{0:.2f}".format(float(float(listcountalt / listsize) * 100))).rstrip('0').rstrip('.')+"%";
  log.info("Downloading URL Number "+str(listcountalt)+" / "+str(listsize)+" "+str(percentage));
  if(motherless_linktype=="link"):
   pymotherless.download_motherless_links(motherless_links[listcount], getargs_headers, getargs_cj, getargs.use_httplib, buffersize=[getargs.set_buffersize, getargs.set_buffersize], outpath=getargs.output_directory);
  if(motherless_linktype=="board" or motherless_linktype=="gallery"):
   pymotherless.download_motherless_links(motherless_links[listcount], getargs_headers, getargs_cj, getargs.use_httplib, buffersize=[getargs.set_buffersize, getargs.set_buffersize], outpath=getargs.output_directory+os.path.sep+motherless_links_dir[listcount]);
  listcount = listcount + 1;
