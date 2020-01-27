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

    $FileInfo: pymotherless.py - Last Update: 1/30/2019 Ver. 0.4.7 RC 4 - Author: cooldude2k $
'''

from __future__ import division, absolute_import, print_function;
import re, os, sys, hashlib, shutil, platform, tempfile, urllib, gzip, time, argparse, cgi, subprocess, imp;
import logging as log;
haverequests = False;
try:
 imp.find_module('requests');
 haverequests = True;
 import requests;
except ImportError:
 haverequests = False;
havemechanize = False;
try:
 imp.find_module('mechanize');
 havemechanize = True;
 import mechanize;
except ImportError:
 havemechanize = False;
if(sys.version[0]=="2"):
 try:
  from cStringIO import StringIO;
 except ImportError:
  from StringIO import StringIO;
 # From http://python-future.org/compatible_idioms.html
 from urlparse import urlparse, urlunparse, urlsplit, urlunsplit, urljoin;
 from urllib import urlencode;
 from urllib2 import urlopen, Request, HTTPError;
 import urllib2, urlparse, cookielib;
if(sys.version[0]>="3"):
 from io import StringIO, BytesIO;
 # From http://python-future.org/compatible_idioms.html
 from urllib.parse import urlparse, urlunparse, urlsplit, urlunsplit, urljoin, urlencode;
 from urllib.request import urlopen, Request;
 from urllib.error import HTTPError;
 import urllib.request as urllib2;
 import urllib.parse as urlparse;
 import http.cookiejar as cookielib;

__program_name__ = "PyMotherless";
__project__ = __program_name__;
__project_url__ = "https://github.com/GameMaker2k/PyMotherless";
__version_info__ = (0, 4, 7, "RC 4", 4);
__version_date_info__ = (2019, 1, 30, "RC 4", 4);
__version_date__ = str(__version_date_info__[0])+"."+str(__version_date_info__[1]).zfill(2)+"."+str(__version_date_info__[2]).zfill(2);
__revision__ = __version_info__[3];
__revision_id__ = "$Id$";
if(__version_info__[4]!=None):
 __version_date_plusrc__ = __version_date__+"-"+str(__version_date_info__[4]);
if(__version_info__[4]==None):
 __version_date_plusrc__ = __version_date__;
if(__version_info__[3]!=None):
 __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2])+" "+str(__version_info__[3]);
if(__version_info__[3]==None):
 __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2]);

tmpfileprefix = "py"+str(sys.version_info[0])+"motherless"+str(__version_info__[0])+"-";
tmpfilesuffix = "-";
pytempdir = tempfile.gettempdir();
defbuffersize = 524288;
defbuffersizedub = [defbuffersize, defbuffersize];

geturls_cj = cookielib.CookieJar();
geturls_ua_firefox_windows7 = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0";
geturls_ua_seamonkey_windows7 = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0 SeaMonkey/2.49.3";
geturls_ua_chrome_windows7 = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36";
geturls_ua_chromium_windows7 = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chromium/67.0.3396.99 Chrome/67.0.3396.99 Safari/537.36";
geturls_ua_palemoon_windows7 = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.9) Gecko/20100101 Goanna/3.4 Firefox/52.9 PaleMoon/27.9.3";
geturls_ua_opera_windows7 = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36 OPR/54.0.2952.54";
geturls_ua_vivaldi_windows7 = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.183 Safari/537.36 Vivaldi/1.96.1147.52";
geturls_ua_internet_explorer_windows7 = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko";
geturls_ua_microsoft_edge_windows7 = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134";
geturls_ua_pymotherless_python = "Mozilla/5.0 (compatible; {proname}/{prover}; +{prourl})".format(proname=__project__, prover=__version__, prourl=__project_url__);
if(platform.python_implementation()!=""):
 geturls_ua_pymotherless_python_alt = "Mozilla/5.0 ({osver}; {archtype}; +{prourl}) {pyimp}/{pyver} (KHTML, like Gecko) {proname}/{prover}".format(osver=platform.system()+" "+platform.release(), archtype=platform.machine(), prourl=__project_url__, pyimp=platform.python_implementation(), pyver=platform.python_version(), proname=__project__, prover=__version__);
if(platform.python_implementation()==""):
 geturls_ua_pymotherless_python_alt = "Mozilla/5.0 ({osver}; {archtype}; +{prourl}) {pyimp}/{pyver} (KHTML, like Gecko) {proname}/{prover}".format(osver=platform.system()+" "+platform.release(), archtype=platform.machine(), prourl=__project_url__, pyimp="Python", pyver=platform.python_version(), proname=__project__, prover=__version__);
geturls_ua_googlebot_google = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)";
geturls_ua_googlebot_google_old = "Googlebot/2.1 (+http://www.google.com/bot.html)";
geturls_ua = geturls_ua_firefox_windows7;
geturls_headers_firefox_windows7 = {'Referer': "http://motherless.com/", 'User-Agent': geturls_ua_firefox_windows7, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"};
geturls_headers_seamonkey_windows7 = {'Referer': "http://motherless.com/", 'User-Agent': geturls_ua_seamonkey_windows7, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"};
geturls_headers_chrome_windows7 = {'Referer': "http://motherless.com/", 'User-Agent': geturls_ua_chrome_windows7, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"};
geturls_headers_chromium_windows7 = {'Referer': "http://motherless.com/", 'User-Agent': geturls_ua_chromium_windows7, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"};
geturls_headers_palemoon_windows7 = {'Referer': "http://motherless.com/", 'User-Agent': geturls_ua_palemoon_windows7, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"};
geturls_headers_opera_windows7 = {'Referer': "http://motherless.com/", 'User-Agent': geturls_ua_opera_windows7, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"};
geturls_headers_vivaldi_windows7 = {'Referer': "http://motherless.com/", 'User-Agent': geturls_ua_vivaldi_windows7, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"};
geturls_headers_internet_explorer_windows7 = {'Referer': "http://motherless.com/", 'User-Agent': geturls_ua_internet_explorer_windows7, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"};
geturls_headers_microsoft_edge_windows7 = {'Referer': "http://motherless.com/", 'User-Agent': geturls_ua_microsoft_edge_windows7, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"};
geturls_headers_pymotherless_python = {'Referer': "http://motherless.com/", 'User-Agent': geturls_ua_pymotherless_python, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"};
geturls_headers_pymotherless_python_alt = {'Referer': "http://motherless.com/", 'User-Agent': geturls_ua_pymotherless_python_alt, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"};
geturls_headers_googlebot_google = {'Referer': "http://motherless.com/", 'User-Agent': geturls_ua_googlebot_google, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"};
geturls_headers_googlebot_google_old = {'Referer': "http://motherless.com/", 'User-Agent': geturls_ua_googlebot_google_old, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"};
geturls_headers = geturls_headers_firefox_windows7;
geturls_download_sleep = 0;

def add_url_param(url, **params):
 n=3;
 parts = list(urlparse.urlsplit(url));
 d = dict(cgi.parse_qsl(parts[n])); # use cgi.parse_qs for list values
 d.update(params);
 parts[n]=urlencode(d);
 return urlparse.urlunsplit(parts);

os.environ["PATH"] = os.environ["PATH"] + os.pathsep + os.path.dirname(os.path.realpath(__file__)) + os.pathsep + os.getcwd();
def which_exec(execfile):
 for path in os.environ["PATH"].split(":"):
  if os.path.exists(path + "/" + execfile):
   return path + "/" + execfile;

def listize(varlist):
 il = 0;
 ix = len(varlist);
 ilx = 1;
 newlistreg = {};
 newlistrev = {};
 newlistfull = {};
 while(il < ix):
  newlistreg.update({ilx: varlist[il]});
  newlistrev.update({varlist[il]: ilx});
  ilx = ilx + 1;
  il = il + 1;
 newlistfull = {1: newlistreg, 2: newlistrev, 'reg': newlistreg, 'rev': newlistrev};
 return newlistfull;

def twolistize(varlist):
 il = 0;
 ix = len(varlist);
 ilx = 1;
 newlistnamereg = {};
 newlistnamerev = {};
 newlistdescreg = {};
 newlistdescrev = {};
 newlistfull = {};
 while(il < ix):
  newlistnamereg.update({ilx: varlist[il][0].strip()});
  newlistnamerev.update({varlist[il][0].strip(): ilx});
  newlistdescreg.update({ilx: varlist[il][1].strip()});
  newlistdescrev.update({varlist[il][1].strip(): ilx});
  ilx = ilx + 1;
  il = il + 1;
 newlistnametmp = {1: newlistnamereg, 2: newlistnamerev, 'reg': newlistnamereg, 'rev': newlistnamerev};
 newlistdesctmp = {1: newlistdescreg, 2: newlistdescrev, 'reg': newlistdescreg, 'rev': newlistdescrev};
 newlistfull = {1: newlistnametmp, 2: newlistdesctmp, 'name': newlistnametmp, 'desc': newlistdesctmp}
 return newlistfull;

def arglistize(proexec, *varlist):
 il = 0;
 ix = len(varlist);
 ilx = 1;
 newarglist = [proexec];
 while(il < ix):
  if varlist[il][0] is not None:
   newarglist.append(varlist[il][0]);
  if varlist[il][1] is not None:
   newarglist.append(varlist[il][1]);
  il = il + 1;
 return newarglist;

# hms_string by ArcGIS Python Recipes
# https://arcpy.wordpress.com/2012/04/20/146/
def hms_string(sec_elapsed):
 h = int(sec_elapsed / (60 * 60));
 m = int((sec_elapsed % (60 * 60)) / 60);
 s = sec_elapsed % 60.0;
 return "{}:{:>02}:{:>05.2f}".format(h, m, s);

# get_readable_size by Lipis
# http://stackoverflow.com/posts/14998888/revisions
def get_readable_size(bytes, precision=1, unit="IEC"):
 unit = unit.upper();
 if(unit!="IEC" and unit!="SI"):
  unit = "IEC";
 if(unit=="IEC"):
  units = [" B"," KiB"," MiB"," GiB"," TiB"," PiB"," EiB"," ZiB"];
  unitswos = ["B","KiB","MiB","GiB","TiB","PiB","EiB","ZiB"];
  unitsize = 1024.0;
 if(unit=="SI"):
  units = [" B"," kB"," MB"," GB"," TB"," PB"," EB"," ZB"];
  unitswos = ["B","kB","MB","GB","TB","PB","EB","ZB"];
  unitsize = 1000.0;
 return_val = {};
 orgbytes = bytes;
 for unit in units:
  if abs(bytes) < unitsize:
   strformat = "%3."+str(precision)+"f%s";
   pre_return_val = (strformat % (bytes, unit));
   pre_return_val = re.sub(r"([0]+) ([A-Za-z]+)", r" \2", pre_return_val);
   pre_return_val = re.sub(r"\. ([A-Za-z]+)", r" \1", pre_return_val);
   alt_return_val = pre_return_val.split();
   return_val = {'Bytes': orgbytes, 'ReadableWithSuffix': pre_return_val, 'ReadableWithoutSuffix': alt_return_val[0], 'ReadableSuffix': alt_return_val[1]}
   return return_val;
  bytes /= unitsize;
 strformat = "%."+str(precision)+"f%s";
 pre_return_val = (strformat % (bytes, "YiB"));
 pre_return_val = re.sub(r"([0]+) ([A-Za-z]+)", r" \2", pre_return_val);
 pre_return_val = re.sub(r"\. ([A-Za-z]+)", r" \1", pre_return_val);
 alt_return_val = pre_return_val.split();
 return_val = {'Bytes': orgbytes, 'ReadableWithSuffix': pre_return_val, 'ReadableWithoutSuffix': alt_return_val[0], 'ReadableSuffix': alt_return_val[1]}
 return return_val;

def get_readable_size_from_file(infile, precision=1, unit="IEC", usehashes=False, usehashtypes="md5,sha1"):
 unit = unit.upper();
 usehashtypes = usehashtypes.lower();
 getfilesize = os.path.getsize(infile);
 return_val = get_readable_size(getfilesize, precision, unit);
 if(usehashes==True):
  hashtypelist = usehashtypes.split(",");
  openfile = open(infile, "rb");
  filecontents = openfile.read();
  openfile.close();
  listnumcount = 0;
  listnumend = len(hashtypelist);
  while(listnumcount < listnumend):
   hashtypelistlow = hashtypelist[listnumcount].strip();
   hashtypelistup = hashtypelistlow.upper();
   filehash = hashlib.new(hashtypelistup);
   filehash.update(filecontents);
   filegethash = filehash.hexdigest();
   return_val.update({hashtypelistup: filegethash});
   listnumcount += 1;
 return return_val;

def get_readable_size_from_string(instring, precision=1, unit="IEC", usehashes=False, usehashtypes="md5,sha1"):
 unit = unit.upper();
 usehashtypes = usehashtypes.lower();
 getfilesize = len(instring);
 return_val = get_readable_size(getfilesize, precision, unit);
 if(usehashes==True):
  hashtypelist = usehashtypes.split(",");
  listnumcount = 0;
  listnumend = len(hashtypelist);
  while(listnumcount < listnumend):
   hashtypelistlow = hashtypelist[listnumcount].strip();
   hashtypelistup = hashtypelistlow.upper();
   filehash = hashlib.new(hashtypelistup);
   if(sys.version[0]=="2"):
    filehash.update(instring);
   if(sys.version[0]>="3"):
    filehash.update(instring.encode('utf-8'));
   filegethash = filehash.hexdigest();
   return_val.update({hashtypelistup: filegethash});
   listnumcount += 1;
 return return_val;

def make_http_headers_from_dict_to_list(headers={'Referer': "http://motherless.com/", 'User-Agent': geturls_ua, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"}):
 if isinstance(headers, dict):
  returnval = [];
  if(sys.version[0]=="2"):
   for headkey, headvalue in headers.iteritems():
    returnval.append((headkey, headvalue));
  if(sys.version[0]>="3"):
   for headkey, headvalue in headers.items():
    returnval.append((headkey, headvalue));
 elif isinstance(headers, list):
  returnval = headers;
 else:
  returnval = False;
 return returnval;

def make_http_headers_from_dict_to_pycurl(headers={'Referer': "http://motherless.com/", 'User-Agent': geturls_ua, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"}):
 if isinstance(headers, dict):
  returnval = [];
  if(sys.version[0]=="2"):
   for headkey, headvalue in headers.iteritems():
    returnval.append(headkey+": "+headvalue);
  if(sys.version[0]>="3"):
   for headkey, headvalue in headers.items():
    returnval.append(headkey+": "+headvalue);
 elif isinstance(headers, list):
  returnval = headers;
 else:
  returnval = False;
 return returnval;

def make_http_headers_from_list_to_dict(headers=[("Referer", "http://motherless.com/"), ("User-Agent", geturls_ua), ("Accept-Encoding", "gzip, deflate"), ("Accept-Language", "en-US,en;q=0.8,en-CA,en-GB;q=0.6"), ("Accept-Charset", "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7"), ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"), ("Connection", "close")]):
 if isinstance(headers, list):
  returnval = {};
  mli = 0;
  mlil = len(headers);
  while(mli<mlil):
   returnval.update({headers[mli][0]: headers[mli][1]});
   mli = mli + 1;
 elif isinstance(headers, dict):
  returnval = headers;
 else:
  returnval = False;
 return returnval;

def get_httplib_support(checkvalue=None):
 global haverequests, havemechanize;
 returnval = [];
 returnval.append("urllib");
 if(haverequests==True):
  returnval.append("requests");
 if(havemechanize==True):
  returnval.append("mechanize");
 if(not checkvalue==None):
  if(checkvalue=="urllib1" or checkvalue=="urllib2"):
   checkvalue = "urllib";
  if(checkvalue in returnval):
   returnval = True;
  else:
   returnval = False;
 return returnval;

def check_httplib_support(checkvalue="urllib"):
 if(checkvalue=="urllib1" or checkvalue=="urllib2"):
  checkvalue = "urllib";
 returnval = get_httplib_support(checkvalue);
 return returnval;

def get_httplib_support_list():
 returnval = get_httplib_support(None);
 return returnval;

def download_from_url(httpurl, httpheaders, httpcookie, httplibuse="urllib", sleep=-1):
 global geturls_download_sleep, haverequests, havemechanize;
 if(sleep<0):
  sleep = geturls_download_sleep;
 if(httplibuse=="urllib1" or httplibuse=="urllib2"):
  httplibuse = "urllib";
 if(haverequests==False and httplibuse=="requests"):
  httplibuse = "urllib";
 if(havemechanize==False and httplibuse=="mechanize"):
  httplibuse = "urllib";
 if(httplibuse=="urllib"):
  returnval = download_from_url_with_urllib(httpurl, httpheaders, httpcookie, sleep);
 elif(httplibuse=="requests"):
  returnval = download_from_url_with_requests(httpurl, httpheaders, httpcookie, sleep);
 elif(httplibuse=="mechanize"):
  returnval = download_from_url_with_mechanize(httpurl, httpheaders, httpcookie, sleep);
 else:
  returnval = False;
 return returnval;

def download_from_url_file(httpurl, httpheaders, httpcookie, httplibuse="urllib", buffersize=defbuffersize, sleep=-1):
 global geturls_download_sleep, haverequests, havemechanize;
 if(sleep<0):
  sleep = geturls_download_sleep;
 if(httplibuse=="urllib1" or httplibuse=="urllib2"):
  httplibuse = "urllib";
 if(haverequests==False and httplibuse=="requests"):
  httplibuse = "urllib";
 if(havemechanize==False and httplibuse=="mechanize"):
  httplibuse = "urllib";
 if(httplibuse=="urllib"):
  returnval = download_from_url_file_with_urllib(httpurl, httpheaders, httpcookie, buffersize, sleep);
 elif(httplibuse=="requests"):
  returnval = download_from_url_file_with_requests(httpurl, httpheaders, httpcookie, buffersize, sleep);
 elif(httplibuse=="mechanize"):
  returnval = download_from_url_file_with_mechanize(httpurl, httpheaders, httpcookie, buffersize, sleep);
 else:
  returnval = False;
 return returnval;

def download_from_url_to_file(httpurl, httpheaders, httpcookie, httplibuse="urllib", outfile="-", outpath=os.getcwd(), buffersize=defbuffersizedub, sleep=-1):
 global geturls_download_sleep, haverequests, havemechanize;
 if(sleep<0):
  sleep = geturls_download_sleep;
 if(httplibuse=="urllib1" or httplibuse=="urllib2"):
  httplibuse = "urllib";
 if(haverequests==False and httplibuse=="requests"):
  httplibuse = "urllib";
 if(havemechanize==False and httplibuse=="mechanize"):
  httplibuse = "urllib";
 if(httplibuse=="urllib"):
  returnval = download_from_url_to_file_with_urllib(httpurl, httpheaders, httpcookie, outfile, outpath, buffersize, sleep);
 elif(httplibuse=="requests"):
  returnval = download_from_url_to_file_with_requests(httpurl, httpheaders, httpcookie, outfile, outpath, buffersize, sleep);
 elif(httplibuse=="mechanize"):
  returnval = download_from_url_to_file_with_mechanize(httpurl, httpheaders, httpcookie, outfile, outpath, buffersize, sleep);
 else:
  returnval = False;
 return returnval;

def download_from_url_with_urllib(httpurl, httpheaders, httpcookie, sleep=-1):
 global geturls_download_sleep;
 if(sleep<0):
  sleep = geturls_download_sleep;
 geturls_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(httpcookie));
 if(isinstance(httpheaders, dict)):
  httpheaders = make_http_headers_from_dict_to_list(httpheaders);
 geturls_opener.addheaders = httpheaders;
 time.sleep(sleep);
 geturls_text = geturls_opener.open(httpurl);
 log.info("Downloading URL "+httpurl);
 if(geturls_text.info().get("Content-Encoding")=="gzip" or geturls_text.info().get("Content-Encoding")=="deflate"):
  if(sys.version[0]=="2"):
   strbuf = StringIO(geturls_text.read());
  if(sys.version[0]>="3"):
   strbuf = BytesIO(geturls_text.read());
  gzstrbuf = gzip.GzipFile(fileobj=strbuf);
  returnval_content = gzstrbuf.read()[:];
 if(geturls_text.info().get("Content-Encoding")!="gzip" and geturls_text.info().get("Content-Encoding")!="deflate"):
  returnval_content = geturls_text.read()[:];
 returnval = {'Type': "Content", 'Content': returnval_content, 'Headers': dict(geturls_text.info()), 'URL': geturls_text.geturl(), 'Code': geturls_text.getcode()};
 geturls_text.close();
 return returnval;

def download_from_url_file_with_urllib(httpurl, httpheaders, httpcookie, buffersize=defbuffersize, sleep=-1):
 global geturls_download_sleep, tmpfileprefix, tmpfilesuffix;
 exec_time_start = time.time();
 myhash = hashlib.new("sha1");
 if(sys.version[0]=="2"):
  myhash.update(httpurl);
  myhash.update(str(buffersize));
  myhash.update(str(exec_time_start));
 if(sys.version[0]>="3"):
  myhash.update(httpurl.encode('utf-8'));
  myhash.update(str(buffersize).encode('utf-8'));
  myhash.update(str(exec_time_start).encode('utf-8'));
 newtmpfilesuffix = tmpfilesuffix + str(myhash.hexdigest());
 if(sleep<0):
  sleep = geturls_download_sleep;
 geturls_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(httpcookie));
 if(isinstance(httpheaders, dict)):
  httpheaders = make_http_headers_from_dict_to_list(httpheaders);
 geturls_opener.addheaders = httpheaders;
 time.sleep(sleep);
 geturls_text = geturls_opener.open(httpurl);
 downloadsize = geturls_text.info().get('Content-Length');
 if(downloadsize is not None):
  downloadsize = int(downloadsize);
 if downloadsize is None: downloadsize = 0;
 fulldatasize = 0;
 prevdownsize = 0;
 log.info("Downloading URL "+httpurl);
 with tempfile.NamedTemporaryFile('wb+', prefix=tmpfileprefix, suffix=newtmpfilesuffix, delete=False) as f:
  tmpfilename = f.name;
  returnval = {'Type': "File", 'Filename': tmpfilename, 'Filesize': downloadsize, 'FilesizeAlt': {'IEC': get_readable_size(downloadsize, 2, "IEC"), 'SI': get_readable_size(downloadsize, 2, "SI")}, 'Headers': dict(geturls_text.info()), 'URL': geturls_text.geturl(), 'Code': geturls_text.getcode()};
  while True:
   databytes = geturls_text.read(buffersize);
   if not databytes: break;
   datasize = len(databytes);
   fulldatasize = datasize + fulldatasize;
   percentage = "";
   if(downloadsize>0):
    percentage = str("{0:.2f}".format(float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%";
   downloaddiff = fulldatasize - prevdownsize;
   log.info("Downloading "+get_readable_size(fulldatasize, 2, "SI")['ReadableWithSuffix']+" / "+get_readable_size(downloadsize, 2, "SI")['ReadableWithSuffix']+" "+str(percentage)+" / Downloaded "+get_readable_size(downloaddiff, 2, "IEC")['ReadableWithSuffix']);
   prevdownsize = fulldatasize;
   f.write(databytes);
  f.close();
 geturls_text.close();
 exec_time_end = time.time();
 log.info("It took "+hms_string(exec_time_start - exec_time_end)+" to download file.");
 returnval.update({'Filesize': os.path.getsize(tmpfilename), 'DownloadTime': float(exec_time_start - exec_time_end), 'DownloadTimeReadable': hms_string(exec_time_start - exec_time_end)});
 return returnval;

def download_from_url_to_file_with_urllib(httpurl, httpheaders, httpcookie, outfile="-", outpath=os.getcwd(), buffersize=defbuffersizedub, sleep=-1):
 global geturls_download_sleep;
 if(sleep<0):
  sleep = geturls_download_sleep;
 if(not outfile=="-"):
  outpath = outpath.rstrip(os.path.sep);
  filepath = os.path.realpath(outpath+os.path.sep+outfile);
  if(not os.path.exists(outpath)):
   os.makedirs(outpath);
  if(os.path.exists(outpath) and os.path.isfile(outpath)):
   return False;
  if(os.path.exists(filepath) and os.path.isdir(filepath)):
   return False;
  pretmpfilename = download_from_url_file_with_urllib(httpurl, httpheaders, httpcookie, buffersize[0], sleep);
  tmpfilename = pretmpfilename['Filename'];
  downloadsize = os.path.getsize(tmpfilename);
  fulldatasize = 0;
  log.info("Moving file "+tmpfilename+" to "+filepath);
  exec_time_start = time.time();
  shutil.move(tmpfilename, filepath);
  exec_time_end = time.time();
  log.info("It took "+hms_string(exec_time_start - exec_time_end)+" to move file.");
  if(os.path.exists(tmpfilename)==True):
   os.remove(tmpfilename);
  returnval = {'Type': "File", 'Filename': filepath, 'Filesize': downloadsize, 'FilesizeAlt': {'IEC': get_readable_size(downloadsize, 2, "IEC"), 'SI': get_readable_size(downloadsize, 2, "SI")}, 'DownloadTime': pretmpfilename['DownloadTime'], 'DownloadTimeReadable': pretmpfilename['DownloadTimeReadable'], 'MoveFileTime': float(exec_time_start - exec_time_end), 'MoveFileTimeReadable': hms_string(exec_time_start - exec_time_end), 'Headers': pretmpfilename['Headers'], 'URL': pretmpfilename['URL'], 'Code': pretmpfilename['Code']};
 if(outfile=="-" and sys.version[0]=="2"):
  pretmpfilename = download_from_url_file_with_urllib(httpurl, httpheaders, httpcookie, buffersize[0], sleep);
  tmpfilename = pretmpfilename['Filename'];
  downloadsize = os.path.getsize(tmpfilename);
  fulldatasize = 0;
  prevdownsize = 0;
  exec_time_start = time.time();
  with open(tmpfilename, 'rb') as ft:
   f = StringIO();
   while True:
    databytes = ft.read(buffersize[1]);
    if not databytes: break;
    datasize = len(databytes);
    fulldatasize = datasize + fulldatasize;
    percentage = "";
    if(downloadsize>0):
     percentage = str("{0:.2f}".format(float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%";
    downloaddiff = fulldatasize - prevdownsize;
    log.info("Copying "+get_readable_size(fulldatasize, 2, "SI")['ReadableWithSuffix']+" / "+get_readable_size(downloadsize, 2, "SI")['ReadableWithSuffix']+" "+str(percentage)+" / Copied "+get_readable_size(downloaddiff, 2, "IEC")['ReadableWithSuffix']);
    prevdownsize = fulldatasize;
    f.write(databytes);
   f.seek(0);
   fdata = f.getvalue();
   f.close();
   ft.close();
   os.remove(tmpfilename);
   exec_time_end = time.time();
   log.info("It took "+hms_string(exec_time_start - exec_time_end)+" to copy file.");
  returnval = {'Type': "Content", 'Content': fdata, 'Contentsize': downloadsize, 'ContentsizeAlt': {'IEC': get_readable_size(downloadsize, 2, "IEC"), 'SI': get_readable_size(downloadsize, 2, "SI")}, 'DownloadTime': pretmpfilename['DownloadTime'], 'DownloadTimeReadable': pretmpfilename['DownloadTimeReadable'], 'MoveFileTime': float(exec_time_start - exec_time_end), 'MoveFileTimeReadable': hms_string(exec_time_start - exec_time_end), 'Headers': pretmpfilename['Headers'], 'URL': pretmpfilename['URL'], 'Code': pretmpfilename['Code']};
 if(outfile=="-" and sys.version[0]>="3"):
  pretmpfilename = download_from_url_file_with_urllib(httpurl, httpheaders, httpcookie, buffersize[0], sleep);
  tmpfilename = pretmpfilename['Filename'];
  downloadsize = os.path.getsize(tmpfilename);
  fulldatasize = 0;
  prevdownsize = 0;
  exec_time_start = time.time();
  with open(tmpfilename, 'rb') as ft:
   f = BytesIO();
   while True:
    databytes = ft.read(buffersize[1]);
    if not databytes: break;
    datasize = len(databytes);
    fulldatasize = datasize + fulldatasize;
    percentage = "";
    if(downloadsize>0):
     percentage = str("{0:.2f}".format(float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%";
    downloaddiff = fulldatasize - prevdownsize;
    log.info("Copying "+get_readable_size(fulldatasize, 2, "SI")['ReadableWithSuffix']+" / "+get_readable_size(downloadsize, 2, "SI")['ReadableWithSuffix']+" "+str(percentage)+" / Copied "+get_readable_size(downloaddiff, 2, "IEC")['ReadableWithSuffix']);
    prevdownsize = fulldatasize;
    f.write(databytes);
   f.seek(0);
   fdata = f.getvalue();
   f.close();
   ft.close();
   os.remove(tmpfilename);
   exec_time_end = time.time();
   log.info("It took "+hms_string(exec_time_start - exec_time_end)+" to copy file.");
  returnval = {'Type': "Content", 'Content': fdata, 'Contentsize': downloadsize, 'ContentsizeAlt': {'IEC': get_readable_size(downloadsize, 2, "IEC"), 'SI': get_readable_size(downloadsize, 2, "SI")}, 'DownloadTime': pretmpfilename['DownloadTime'], 'DownloadTimeReadable': pretmpfilename['DownloadTimeReadable'], 'MoveFileTime': float(exec_time_start - exec_time_end), 'MoveFileTimeReadable': hms_string(exec_time_start - exec_time_end), 'Headers': pretmpfilename['Headers'], 'URL': pretmpfilename['URL'], 'Code': pretmpfilename['Code']};
 return returnval;

if(haverequests==True):
 def download_from_url_with_requests(httpurl, httpheaders, httpcookie, sleep=-1):
  global geturls_download_sleep;
  if(sleep<0):
   sleep = geturls_download_sleep;
  if(isinstance(httpheaders, list)):
   httpheaders = make_http_headers_from_list_to_dict(httpheaders);
  time.sleep(sleep);
  geturls_text = requests.get(httpurl, headers=httpheaders, cookies=httpcookie);
  log.info("Downloading URL "+httpurl);
  if(geturls_text.headers.get('Content-Type')=="gzip" or geturls_text.headers.get('Content-Type')=="deflate"):
   if(sys.version[0]=="2"):
    strbuf = StringIO(geturls_text.content);
   if(sys.version[0]>="3"):
    strbuf = BytesIO(geturls_text.content);
   gzstrbuf = gzip.GzipFile(fileobj=strbuf);
   returnval_content = gzstrbuf.content[:];
  if(geturls_text.headers.get('Content-Type')!="gzip" and geturls_text.headers.get('Content-Type')!="deflate"):
   returnval_content = geturls_text.content[:];
  returnval = {'Type': "Content", 'Content': returnval_content, 'Headers': dict(geturls_text.headers), 'URL': geturls_text.url, 'Code': geturls_text.status_code};
  geturls_text.close();
  return returnval;

if(haverequests==False):
 def download_from_url_with_requests(httpurl, httpheaders, httpcookie, sleep=-1):
  returnval = download_from_url_with_urllib(httpurl, httpheaders, httpcookie, sleep)
  return returnval;

if(haverequests==True):
 def download_from_url_file_with_requests(httpurl, httpheaders, httpcookie, buffersize=defbuffersize, sleep=-1):
  global geturls_download_sleep, tmpfileprefix, tmpfilesuffix;
  exec_time_start = time.time();
  myhash = hashlib.new("sha1");
  if(sys.version[0]=="2"):
   myhash.update(httpurl);
   myhash.update(str(buffersize));
   myhash.update(str(exec_time_start));
  if(sys.version[0]>="3"):
   myhash.update(httpurl.encode('utf-8'));
   myhash.update(str(buffersize).encode('utf-8'));
   myhash.update(str(exec_time_start).encode('utf-8'));
  newtmpfilesuffix = tmpfilesuffix + str(myhash.hexdigest());
  if(sleep<0):
   sleep = geturls_download_sleep;
  if(isinstance(httpheaders, list)):
   httpheaders = make_http_headers_from_list_to_dict(httpheaders);
  time.sleep(sleep);
  geturls_text = requests.get(httpurl, headers=httpheaders, cookies=httpcookie, stream=True);
  downloadsize = int(geturls_text.headers.get('Content-Length'));
  if(downloadsize is not None):
   downloadsize = int(downloadsize);
  if downloadsize is None: downloadsize = 0;
  fulldatasize = 0;
  prevdownsize = 0;
  log.info("Downloading URL "+httpurl);
  with tempfile.NamedTemporaryFile('wb+', prefix=tmpfileprefix, suffix=newtmpfilesuffix, delete=False) as f:
   tmpfilename = f.name;
   returnval = {'Type': "File", 'Filename': tmpfilename, 'Filesize': downloadsize, 'FilesizeAlt': {'IEC': get_readable_size(downloadsize, 2, "IEC"), 'SI': get_readable_size(downloadsize, 2, "SI")}, 'Headers': dict(geturls_text.headers), 'URL': geturls_text.url, 'Code': geturls_text.status_code};
   for databytes in geturls_text.iter_content(chunk_size=buffersize):
    datasize = len(databytes);
    fulldatasize = datasize + fulldatasize;
    percentage = "";
    if(downloadsize>0):
     percentage = str("{0:.2f}".format(float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%";
    downloaddiff = fulldatasize - prevdownsize;
    log.info("Downloading "+get_readable_size(fulldatasize, 2, "SI")['ReadableWithSuffix']+" / "+get_readable_size(downloadsize, 2, "SI")['ReadableWithSuffix']+" "+str(percentage)+" / Downloaded "+get_readable_size(downloaddiff, 2, "IEC")['ReadableWithSuffix']);
    prevdownsize = fulldatasize;
    f.write(databytes);
   f.close();
  geturls_text.close();
  exec_time_end = time.time();
  log.info("It took "+hms_string(exec_time_start - exec_time_end)+" to download file.");
  returnval.update({'Filesize': os.path.getsize(tmpfilename), 'DownloadTime': float(exec_time_start - exec_time_end), 'DownloadTimeReadable': hms_string(exec_time_start - exec_time_end)});
  return returnval;

if(haverequests==False):
 def download_from_url_file_with_requests(httpurl, httpheaders, httpcookie, buffersize=defbuffersize, sleep=-1):
  returnval = download_from_url_file_with_urllib(httpurl, httpheaders, httpcookie, buffersize, sleep)
  return returnval;

if(haverequests==True):
 def download_from_url_to_file_with_requests(httpurl, httpheaders, httpcookie, outfile="-", outpath=os.getcwd(), buffersize=defbuffersizedub, sleep=-1):
  global geturls_download_sleep;
  if(sleep<0):
   sleep = geturls_download_sleep;
  if(not outfile=="-"):
   outpath = outpath.rstrip(os.path.sep);
   filepath = os.path.realpath(outpath+os.path.sep+outfile);
   if(not os.path.exists(outpath)):
    os.makedirs(outpath);
   if(os.path.exists(outpath) and os.path.isfile(outpath)):
    return False;
   if(os.path.exists(filepath) and os.path.isdir(filepath)):
    return False;
   pretmpfilename = download_from_url_file_with_requests(httpurl, httpheaders, httpcookie, buffersize[0], sleep);
   tmpfilename = pretmpfilename['Filename'];
   downloadsize = os.path.getsize(tmpfilename);
   fulldatasize = 0;
   log.info("Moving file "+tmpfilename+" to "+filepath);
   exec_time_start = time.time();
   shutil.move(tmpfilename, filepath);
   exec_time_end = time.time();
   log.info("It took "+hms_string(exec_time_start - exec_time_end)+" to move file.");
   if(os.path.exists(tmpfilename)==True):
    os.remove(tmpfilename);
   returnval = {'Type': "File", 'Filename': filepath, 'Filesize': downloadsize, 'FilesizeAlt': {'IEC': get_readable_size(downloadsize, 2, "IEC"), 'SI': get_readable_size(downloadsize, 2, "SI")}, 'DownloadTime': pretmpfilename['DownloadTime'], 'DownloadTimeReadable': pretmpfilename['DownloadTimeReadable'], 'MoveFileTime': float(exec_time_start - exec_time_end), 'MoveFileTimeReadable': hms_string(exec_time_start - exec_time_end), 'Headers': pretmpfilename['Headers'], 'URL': pretmpfilename['URL'], 'Code': pretmpfilename['Code']};
  if(outfile=="-" and sys.version[0]=="2"):
   pretmpfilename = download_from_url_file_with_requests(httpurl, httpheaders, httpcookie, buffersize[0], sleep);
   tmpfilename = pretmpfilename['Filename'];
   downloadsize = os.path.getsize(tmpfilename);
   fulldatasize = 0;
   prevdownsize = 0;
   exec_time_start = time.time();
   with open(tmpfilename, 'rb') as ft:
    f = StringIO();
    while True:
     databytes = ft.read(buffersize[1]);
     if not databytes: break;
     datasize = len(databytes);
     fulldatasize = datasize + fulldatasize;
     percentage = "";
     if(downloadsize>0):
      percentage = str("{0:.2f}".format(float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%";
     downloaddiff = fulldatasize - prevdownsize;
     log.info("Copying "+get_readable_size(fulldatasize, 2, "SI")['ReadableWithSuffix']+" / "+get_readable_size(downloadsize, 2, "SI")['ReadableWithSuffix']+" "+str(percentage)+" / Copied "+get_readable_size(downloaddiff, 2, "IEC")['ReadableWithSuffix']);
     prevdownsize = fulldatasize;
     f.write(databytes);
    f.seek(0);
    fdata = f.getvalue();
    f.close();
    ft.close();
    os.remove(tmpfilename);
    exec_time_end = time.time();
    log.info("It took "+hms_string(exec_time_start - exec_time_end)+" to copy file.");
   returnval = {'Type': "Content", 'Content': fdata, 'Contentsize': downloadsize, 'ContentsizeAlt': {'IEC': get_readable_size(downloadsize, 2, "IEC"), 'SI': get_readable_size(downloadsize, 2, "SI")}, 'DownloadTime': pretmpfilename['DownloadTime'], 'DownloadTimeReadable': pretmpfilename['DownloadTimeReadable'], 'MoveFileTime': float(exec_time_start - exec_time_end), 'MoveFileTimeReadable': hms_string(exec_time_start - exec_time_end), 'Headers': pretmpfilename['Headers'], 'URL': pretmpfilename['URL'], 'Code': pretmpfilename['Code']};
  if(outfile=="-" and sys.version[0]>="3"):
   pretmpfilename = download_from_url_file_with_requests(httpurl, httpheaders, httpcookie, buffersize[0], sleep);
   tmpfilename = pretmpfilename['Filename'];
   downloadsize = os.path.getsize(tmpfilename);
   fulldatasize = 0;
   prevdownsize = 0;
   exec_time_start = time.time();
   with open(tmpfilename, 'rb') as ft:
    f = BytesIO();
    while True:
     databytes = ft.read(buffersize[1]);
     if not databytes: break;
     datasize = len(databytes);
     fulldatasize = datasize + fulldatasize;
     percentage = "";
     if(downloadsize>0):
      percentage = str("{0:.2f}".format(float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%";
     downloaddiff = fulldatasize - prevdownsize;
     log.info("Copying "+get_readable_size(fulldatasize, 2, "SI")['ReadableWithSuffix']+" / "+get_readable_size(downloadsize, 2, "SI")['ReadableWithSuffix']+" "+str(percentage)+" / Copied "+get_readable_size(downloaddiff, 2, "IEC")['ReadableWithSuffix']);
     prevdownsize = fulldatasize;
     f.write(databytes);
    f.seek(0);
    fdata = f.getvalue();
    f.close();
    ft.close();
    os.remove(tmpfilename);
    exec_time_end = time.time();
    log.info("It took "+hms_string(exec_time_start - exec_time_end)+" to copy file.");
   returnval = {'Type': "Content", 'Content': fdata, 'Contentsize': downloadsize, 'ContentsizeAlt': {'IEC': get_readable_size(downloadsize, 2, "IEC"), 'SI': get_readable_size(downloadsize, 2, "SI")}, 'DownloadTime': pretmpfilename['DownloadTime'], 'DownloadTimeReadable': pretmpfilename['DownloadTimeReadable'], 'MoveFileTime': float(exec_time_start - exec_time_end), 'MoveFileTimeReadable': hms_string(exec_time_start - exec_time_end), 'Headers': pretmpfilename['Headers'], 'URL': pretmpfilename['URL'], 'Code': pretmpfilename['Code']};
  return returnval;

if(haverequests==False):
 def download_from_url_to_file_with_requests(httpurl, httpheaders, httpcookie, outfile="-", outpath=os.getcwd(), buffersize=defbuffersizedub, sleep=-1):
  returnval = download_from_url_to_file_with_urllib(httpurl, httpheaders, httpcookie, buffersize, outfile, outpath, sleep)
  return returnval;

if(havemechanize==True):
 def download_from_url_with_mechanize(httpurl, httpheaders, httpcookie, sleep=-1):
  global geturls_download_sleep;
  if(sleep<0):
   sleep = geturls_download_sleep;
  geturls_opener = mechanize.Browser();
  if(isinstance(httpheaders, dict)):
   httpheaders = make_http_headers_from_dict_to_list(httpheaders);
  time.sleep(sleep);
  geturls_opener.addheaders = httpheaders;
  geturls_opener.set_cookiejar(httpcookie);
  geturls_opener.set_handle_robots(False);
  geturls_text = geturls_opener.open(httpurl);
  log.info("Downloading URL "+httpurl);
  if(geturls_text.info().get("Content-Encoding")=="gzip" or geturls_text.info().get("Content-Encoding")=="deflate"):
   if(sys.version[0]=="2"):
    strbuf = StringIO(geturls_text.read());
   if(sys.version[0]>="3"):
    strbuf = BytesIO(geturls_text.read());
   gzstrbuf = gzip.GzipFile(fileobj=strbuf);
   returnval_content = gzstrbuf.read()[:];
  if(geturls_text.info().get("Content-Encoding")!="gzip" and geturls_text.info().get("Content-Encoding")!="deflate"):
   returnval_content = geturls_text.read()[:];
  returnval = {'Type': "Content", 'Content': returnval_content, 'Headers': dict(geturls_text.info()), 'URL': geturls_text.geturl(), 'Code': geturls_text.code};
  geturls_text.close();
  return returnval;

if(havemechanize==False):
 def download_from_url_with_mechanize(httpurl, httpheaders, httpcookie, sleep=-1):
  returnval = download_from_url_with_urllib(httpurl, httpheaders, httpcookie, sleep)
  return returnval;

if(havemechanize==True):
 def download_from_url_file_with_mechanize(httpurl, httpheaders, httpcookie, buffersize=defbuffersize, sleep=-1):
  global geturls_download_sleep, tmpfileprefix, tmpfilesuffix;
  exec_time_start = time.time();
  myhash = hashlib.new("sha1");
  if(sys.version[0]=="2"):
   myhash.update(httpurl);
   myhash.update(str(buffersize));
   myhash.update(str(exec_time_start));
  if(sys.version[0]>="3"):
   myhash.update(httpurl.encode('utf-8'));
   myhash.update(str(buffersize).encode('utf-8'));
   myhash.update(str(exec_time_start).encode('utf-8'));
  newtmpfilesuffix = tmpfilesuffix + str(myhash.hexdigest());
  if(sleep<0):
   sleep = geturls_download_sleep;
  geturls_opener = mechanize.Browser();
  if(isinstance(httpheaders, dict)):
   httpheaders = make_http_headers_from_dict_to_list(httpheaders);
  time.sleep(sleep);
  geturls_opener.addheaders = httpheaders;
  geturls_opener.set_cookiejar(httpcookie);
  geturls_opener.set_handle_robots(False);
  geturls_text = geturls_opener.open(httpurl);
  downloadsize = int(geturls_text.info().get('Content-Length'));
  if(downloadsize is not None):
   downloadsize = int(downloadsize);
  if downloadsize is None: downloadsize = 0;
  fulldatasize = 0;
  prevdownsize = 0;
  log.info("Downloading URL "+httpurl);
  with tempfile.NamedTemporaryFile('wb+', prefix=tmpfileprefix, suffix=newtmpfilesuffix, delete=False) as f:
   tmpfilename = f.name;
   returnval = {'Type': "File", 'Filename': tmpfilename, 'Filesize': downloadsize, 'FilesizeAlt': {'IEC': get_readable_size(downloadsize, 2, "IEC"), 'SI': get_readable_size(downloadsize, 2, "SI")}, 'Headers': dict(geturls_text.info()), 'URL': geturls_text.geturl(), 'Code': geturls_text.code};
   while True:
    databytes = geturls_text.read(buffersize);
    if not databytes: break;
    datasize = len(databytes);
    fulldatasize = datasize + fulldatasize;
    percentage = "";
    if(downloadsize>0):
     percentage = str("{0:.2f}".format(float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%";
    downloaddiff = fulldatasize - prevdownsize;
    log.info("Downloading "+get_readable_size(fulldatasize, 2, "SI")['ReadableWithSuffix']+" / "+get_readable_size(downloadsize, 2, "SI")['ReadableWithSuffix']+" "+str(percentage)+" / Downloaded "+get_readable_size(downloaddiff, 2, "IEC")['ReadableWithSuffix']);
    prevdownsize = fulldatasize;
    f.write(databytes);
   f.close();
  geturls_text.close();
  exec_time_end = time.time();
  log.info("It took "+hms_string(exec_time_start - exec_time_end)+" to download file.");
  returnval.update({'Filesize': os.path.getsize(tmpfilename), 'DownloadTime': float(exec_time_start - exec_time_end), 'DownloadTimeReadable': hms_string(exec_time_start - exec_time_end)});
  return returnval;

if(havemechanize==False):
 def download_from_url_file_with_mechanize(httpurl, httpheaders, httpcookie, buffersize=defbuffersize, sleep=-1):
  returnval = download_from_url_file_with_urllib(httpurl, httpheaders, httpcookie, buffersize, sleep)
  return returnval;

if(havemechanize==True):
 def download_from_url_to_file_with_mechanize(httpurl, httpheaders, httpcookie, outfile="-", outpath=os.getcwd(), buffersize=defbuffersizedub, sleep=-1):
  global geturls_download_sleep;
  if(sleep<0):
   sleep = geturls_download_sleep;
  if(not outfile=="-"):
   outpath = outpath.rstrip(os.path.sep);
   filepath = os.path.realpath(outpath+os.path.sep+outfile);
   if(not os.path.exists(outpath)):
    os.makedirs(outpath);
   if(os.path.exists(outpath) and os.path.isfile(outpath)):
    return False;
   if(os.path.exists(filepath) and os.path.isdir(filepath)):
    return False;
   pretmpfilename = download_from_url_file_with_mechanize(httpurl, httpheaders, httpcookie, buffersize[0], sleep);
   tmpfilename = pretmpfilename['Filename'];
   downloadsize = os.path.getsize(tmpfilename);
   fulldatasize = 0;
   log.info("Moving file "+tmpfilename+" to "+filepath);
   exec_time_start = time.time();
   log.info("It took "+hms_string(exec_time_start - exec_time_end)+" to move file.");
   shutil.move(tmpfilename, filepath);
   if(os.path.exists(tmpfilename)==True):
    os.remove(tmpfilename);
   returnval = {'Type': "File", 'Filename': filepath, 'Filesize': downloadsize, 'FilesizeAlt': {'IEC': get_readable_size(downloadsize, 2, "IEC"), 'SI': get_readable_size(downloadsize, 2, "SI")}, 'DownloadTime': pretmpfilename['DownloadTime'], 'DownloadTimeReadable': pretmpfilename['DownloadTimeReadable'], 'MoveFileTime': float(exec_time_start - exec_time_end), 'MoveFileTimeReadable': hms_string(exec_time_start - exec_time_end), 'Headers': pretmpfilename['Headers'], 'URL': pretmpfilename['URL'], 'Code': pretmpfilename['Code']};
  if(outfile=="-" and sys.version[0]=="2"):
   pretmpfilename = download_from_url_file_with_mechanize(httpurl, httpheaders, httpcookie, buffersize[0], sleep);
   tmpfilename = pretmpfilename['Filename'];
   downloadsize = os.path.getsize(tmpfilename);
   fulldatasize = 0;
   prevdownsize = 0;
   exec_time_start = time.time();
   with open(tmpfilename, 'rb') as ft:
    f = StringIO();
    while True:
     databytes = ft.read(buffersize[1]);
     if not databytes: break;
     datasize = len(databytes);
     fulldatasize = datasize + fulldatasize;
     percentage = "";
     if(downloadsize>0):
      percentage = str("{0:.2f}".format(float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%";
     downloaddiff = fulldatasize - prevdownsize;
     log.info("Copying "+get_readable_size(fulldatasize, 2, "SI")['ReadableWithSuffix']+" / "+get_readable_size(downloadsize, 2, "SI")['ReadableWithSuffix']+" "+str(percentage)+" / Copied "+get_readable_size(downloaddiff, 2, "IEC")['ReadableWithSuffix']);
     prevdownsize = fulldatasize;
     f.write(databytes);
    f.seek(0);
    fdata = f.getvalue();
    f.close();
    ft.close();
    os.remove(tmpfilename);
    exec_time_end = time.time();
    log.info("It took "+hms_string(exec_time_start - exec_time_end)+" to copy file.");
   returnval = {'Type': "Content", 'Content': fdata, 'Contentsize': downloadsize, 'ContentsizeAlt': {'IEC': get_readable_size(downloadsize, 2, "IEC"), 'SI': get_readable_size(downloadsize, 2, "SI")}, 'DownloadTime': pretmpfilename['DownloadTime'], 'DownloadTimeReadable': pretmpfilename['DownloadTimeReadable'], 'MoveFileTime': float(exec_time_start - exec_time_end), 'MoveFileTimeReadable': hms_string(exec_time_start - exec_time_end), 'Headers': pretmpfilename['Headers'], 'URL': pretmpfilename['URL'], 'Code': pretmpfilename['Code']};
  if(outfile=="-" and sys.version[0]>="3"):
   pretmpfilename = download_from_url_file_with_mechanize(httpurl, httpheaders, httpcookie, buffersize[0], sleep);
   tmpfilename = pretmpfilename['Filename'];
   downloadsize = os.path.getsize(tmpfilename);
   fulldatasize = 0;
   prevdownsize = 0;
   exec_time_start = time.time();
   with open(tmpfilename, 'rb') as ft:
    f = BytesIO();
    while True:
     databytes = ft.read(buffersize[1]);
     if not databytes: break;
     datasize = len(databytes);
     fulldatasize = datasize + fulldatasize;
     percentage = "";
     if(downloadsize>0):
      percentage = str("{0:.2f}".format(float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%";
     downloaddiff = fulldatasize - prevdownsize;
     log.info("Copying "+get_readable_size(fulldatasize, 2, "SI")['ReadableWithSuffix']+" / "+get_readable_size(downloadsize, 2, "SI")['ReadableWithSuffix']+" "+str(percentage)+" / Copied "+get_readable_size(downloaddiff, 2, "IEC")['ReadableWithSuffix']);
     prevdownsize = fulldatasize;
     f.write(databytes);
    f.seek(0);
    fdata = f.getvalue();
    f.close();
    ft.close();
    os.remove(tmpfilename);
    exec_time_end = time.time();
    log.info("It took "+hms_string(exec_time_start - exec_time_end)+" to copy file.");
   returnval = {'Type': "Content", 'Content': fdata, 'Contentsize': downloadsize, 'ContentsizeAlt': {'IEC': get_readable_size(downloadsize, 2, "IEC"), 'SI': get_readable_size(downloadsize, 2, "SI")}, 'DownloadTime': pretmpfilename['DownloadTime'], 'DownloadTimeReadable': pretmpfilename['DownloadTimeReadable'], 'MoveFileTime': float(exec_time_start - exec_time_end), 'MoveFileTimeReadable': hms_string(exec_time_start - exec_time_end), 'Headers': pretmpfilename['Headers'], 'URL': pretmpfilename['URL'], 'Code': pretmpfilename['Code']};
  return returnval;

if(havemechanize==False):
 def download_from_url_to_file_with_mechanize(httpurl, httpheaders, httpcookie, outfile="-", outpath=os.getcwd(), buffersize=defbuffersizedub, sleep=-1):
  returnval = download_from_url_to_file_with_urllib(httpurl, httpheaders, httpcookie, buffersize, outfile, outpath, sleep)
  return returnval;

def check_motherless_url(httpurl):
 returnval = {};
 httpurl.replace("https://", "http://");
 if(not httpurl.startswith("http")):
  httpurl = "http://"+httpurl;
 urlparts = urlsplit(httpurl);
 urltype = None;
 domaintype = None;
 urlservtype = None;
 if(urlparts.netloc=="motherless.com" or urlparts.netloc=="www.motherless.com"):
  urltype = "motherless-link";
  domaintype = "motherless";
  urlservtype = "www";
 if(urlparts.netloc=="cdn-avatars.motherlessmedia.com" or urlparts.netloc=="cdn1-avatars.motherlessmedia.com" or urlparts.netloc=="cdn2-avatars.motherlessmedia.com" or urlparts.netloc=="cdn3-avatars.motherlessmedia.com" or urlparts.netloc=="cdn4-avatars.motherlessmedia.com" or urlparts.netloc=="cdn5-avatars.motherlessmedia.com"):
  urltype = "motherless-avatar";
  domaintype = "motherlessmedia";
 if(urlparts.netloc=="cdn-images.motherlessmedia.com" or urlparts.netloc=="cdn1-images.motherlessmedia.com" or urlparts.netloc=="cdn2-images.motherlessmedia.com" or urlparts.netloc=="cdn3-images.motherlessmedia.com" or urlparts.netloc=="cdn4-images.motherlessmedia.com" or urlparts.netloc=="cdn5-images.motherlessmedia.com"):
  urltype = "motherless-image";
  domaintype = "motherlessmedia";
 if(urlparts.netloc=="cdn-videos.motherlessmedia.com" or urlparts.netloc=="cdn1-videos.motherlessmedia.com" or urlparts.netloc=="cdn2-videos.motherlessmedia.com" or urlparts.netloc=="cdn3-videos.motherlessmedia.com" or urlparts.netloc=="cdn4-videos.motherlessmedia.com" or urlparts.netloc=="cdn5-videos.motherlessmedia.com"):
  urltype = "motherless-video";
  domaintype = "motherlessmedia";
 if(urlparts.netloc=="cdn-thumbs.motherlessmedia.com" or urlparts.netloc=="cdn1-thumbs.motherlessmedia.com" or urlparts.netloc=="cdn2-thumbs.motherlessmedia.com" or urlparts.netloc=="cdn3-thumbs.motherlessmedia.com" or urlparts.netloc=="cdn4-thumbs.motherlessmedia.com" or urlparts.netloc=="cdn5-thumbs.motherlessmedia.com"):
  urltype = "motherless-thumbnail";
  domaintype = "motherlessmedia";
 if(urlparts.netloc=="cdn-avatars.motherlessmedia.com" or urlparts.netloc=="cdn-images.motherlessmedia.com" or urlparts.netloc=="cdn-videos.motherlessmedia.com" or urlparts.netloc=="cdn-thumbs.motherlessmedia.com"):
  urlservtype = "cdn";
 if(urlparts.netloc=="cdn1-avatars.motherlessmedia.com" or urlparts.netloc=="cdn1-images.motherlessmedia.com" or urlparts.netloc=="cdn1-videos.motherlessmedia.com" or urlparts.netloc=="cdn1-thumbs.motherlessmedia.com"):
  urlservtype = "cdn1";
 if(urlparts.netloc=="cdn2-avatars.motherlessmedia.com" or urlparts.netloc=="cdn2-images.motherlessmedia.com" or urlparts.netloc=="cdn2-videos.motherlessmedia.com" or urlparts.netloc=="cdn2-thumbs.motherlessmedia.com"):
  urlservtype = "cdn2";
 if(urlparts.netloc=="cdn3-avatars.motherlessmedia.com" or urlparts.netloc=="cdn3-images.motherlessmedia.com" or urlparts.netloc=="cdn3-videos.motherlessmedia.com" or urlparts.netloc=="cdn3-thumbs.motherlessmedia.com"):
  urlservtype = "cdn3";
 if(urlparts.netloc=="cdn4-avatars.motherlessmedia.com" or urlparts.netloc=="cdn4-images.motherlessmedia.com" or urlparts.netloc=="cdn4-videos.motherlessmedia.com" or urlparts.netloc=="cdn4-thumbs.motherlessmedia.com"):
  urlservtype = "cdn4";
 if(urlparts.netloc=="cdn5-avatars.motherlessmedia.com" or urlparts.netloc=="cdn5-images.motherlessmedia.com" or urlparts.netloc=="cdn5-videos.motherlessmedia.com" or urlparts.netloc=="cdn5-thumbs.motherlessmedia.com"):
  urlservtype = "cdn5";
 if(urltype==None or domaintype==None or urlservtype==None):
  return False;
 returnval.update({'url': urlparts.geturl(), 'originalurl': httpurl, 'urltype': urltype, 'urlserv': urlservtype, 'domaintype': domaintype, 'urlinfo': {'scheme': urlparts.scheme, 'netloc': urlparts.netloc, 'path': urlparts.path, 'query': urlparts.query, 'fragment': urlparts.fragment}});
 return returnval;

def fix_motherless_url(httpurl):
 tmpreturnval = check_motherless_url(httpurl);
 if(tmpreturnval==False):
  returnval = False
 else:
  returnval = tmpreturnval['url'];
 return returnval;

def get_motherless_link_type(httpurl):
 httpurl = fix_motherless_url(httpurl);
 if(httpurl==False):
  return False;
 mregex_gettitle = re.escape("http://cdn")+"([1-5])"+re.escape("-");
 httpurl = re.sub(mregex_gettitle, "http://cdn-", httpurl);
 mlessvidqstr = urlparse.parse_qs(urlparse.urlparse(httpurl).query);
 mlessvidid_parts = urlparse.urlparse(httpurl);
 mlessvidid = mlessvidid_parts.path.split("/");
 returnval = False;
 if(mlessvidid[1]=="videos" and len(mlessvidid)==3 and (mlessvidid[2]=="recent" or mlessvidid[2]=="favorited" or mlessvidid[2]=="viewed" or mlessvidid[2]=="commented" or mlessvidid[2]=="popular")):
  returnval = "gallery";
 if(mlessvidid[1]=="images" and len(mlessvidid)==3 and (mlessvidid[2]=="recent" or mlessvidid[2]=="favorited" or mlessvidid[2]=="viewed" or mlessvidid[2]=="commented" or mlessvidid[2]=="popular")):
  returnval = "gallery";
 if(mlessvidid[1]=="galleries" and len(mlessvidid)==3 and (mlessvidid[2]=="recent" or mlessvidid[2]=="favorited" or mlessvidid[2]=="viewed" or mlessvidid[2]=="commented" or mlessvidid[2]=="popular")):
  returnval = "gallery";
 if(mlessvidid[1]=="videos" and len(mlessvidid)==2):
  returnval = "sample-videos";
 if(mlessvidid[1]=="images" and len(mlessvidid)==2):
  returnval = "sample-images";
 if(mlessvidid[1]=="galleries" and len(mlessvidid)==2):
  returnval = "sample-galleries";
 if(mlessvidid[1]=="" and len(mlessvidid)==2):
  returnval = "sample";
 if(mlessvidid[1]=="groups" and len(mlessvidid)==2):
  returnval = "group";
 if(mlessvidid[1]=="groups" and len(mlessvidid)==3 and mlessvidid[2]=="search"):
  returnval = "group";
 if(mlessvidid[1]=="groups" and len(mlessvidid)==4 and mlessvidid[2]=="category"):
  returnval = "group";
 if(mlessvidid[1]=="live" and len(mlessvidid)==3 and (mlessvidid[2]=="videos" or mlessvidid[2]=="images")):
  returnval = "gallery";
 if(mlessvidid[1]=="u" and len(mlessvidid)==3):
  returnval = "gallery";
 if(mlessvidid[1]=="f" and len(mlessvidid)==4 and (mlessvidid[2]=="videos" or mlessvidid[2]=="images" or mlessvidid[2]=="galleries")):
  returnval = "gallery";
 if(mlessvidid[1]=="galleries" and len(mlessvidid)==4 and mlessvidid[2]=="member"):
  returnval = "gallery";
 if(mlessvidid[1]=="galleries" and len(mlessvidid)==5 and mlessvidid[2]=="member" and (mlessvidid[4]=="created" or mlessvidid[4]=="viewed" or mlessvidid[4]=="favorited" or mlessvidid[4]=="commented")):
  returnval = "gallery";
 if(mlessvidid[1]=="gv" and len(mlessvidid)==3):
  returnval = "gallery";
 if(mlessvidid[1]=="gi" and len(mlessvidid)==3):
  returnval = "gallery";
 if(mlessvidid[1]=="gm" and len(mlessvidid)==3):
  returnval = "member";
 if(mlessvidid[1]=="term" and len(mlessvidid)==3 and (mlessvidid[2]=="videos" or mlessvidid[2]=="images" or mlessvidid[2]=="galleries")):
  returnval = "gallery";
 if(mlessvidid[1]=="g" and len(mlessvidid)==4 and re.match("^([0-9A-F]+)$", mlessvidid[3])):
  returnval = "link";
 if(mlessvidid[1]=="random" and len(mlessvidid)==3 and (mlessvidid[2]=="video" or mlessvidid[2]=="image")):
  returnval = "link";
 if(re.match("^V", mlessvidid[1]) and len(mlessvidid)==2):
  returnval = "board";
 if(re.match("^H", mlessvidid[1]) and len(mlessvidid)==2):
  returnval = "gallery";
 if(re.match("^G", mlessvidid[1]) and len(mlessvidid)==2):
  returnval = "gallery";
 if(re.match("^G", mlessvidid[1]) and len(mlessvidid)==3):
  returnval = "link";
 if(re.match("^g", mlessvidid[1]) and len(mlessvidid)==4 and re.match("^([0-9A-F]+)$", mlessvidid[3])):
  returnval = "link";
 if(mlessvidid[1]=="members" and len(mlessvidid)==2):
  returnval = "member";
 if(mlessvidid[1]=="members" and len(mlessvidid)==3 and mlessvidid[2]=="search"):
  returnval = "member";
 if(mlessvidid[1]=="members" and len(mlessvidid)==4 and (mlessvidid[2]=="uploader" or mlessvidid[2]=="viewed" or mlessvidid[2]=="social" or mlessvidid[2]=="favorited" or mlessvidid[2]=="commented" or mlessvidid[2]=="mentioned" or mlessvidid[2]=="verified")):
  returnval = "member";
 if(mlessvidid[1]=="girls" and len(mlessvidid)==2):
  returnval = "girls";
 if(mlessvidid[1]=="referers" and len(mlessvidid)==2):
  returnval = "referers";
 if(mlessvidid[1]=="about" and len(mlessvidid)==2):
  returnval = "team";
 if(mlessvidid_parts.netloc=="cdn-images.motherlessmedia.com" or mlessvidid_parts.netloc=="cdn-videos.motherlessmedia.com" or mlessvidid_parts.netloc=="cdn-thumbs.motherlessmedia.com"):
  returnval = "download";
 if(mlessvidid_parts.netloc=="cdn1-images.motherlessmedia.com" or mlessvidid_parts.netloc=="cdn1-videos.motherlessmedia.com" or mlessvidid_parts.netloc=="cdn1-thumbs.motherlessmedia.com"):
  returnval = "download";
 if(mlessvidid_parts.netloc=="cdn2-images.motherlessmedia.com" or mlessvidid_parts.netloc=="cdn2-videos.motherlessmedia.com" or mlessvidid_parts.netloc=="cdn2-thumbs.motherlessmedia.com"):
  returnval = "download";
 if(mlessvidid_parts.netloc=="cdn3-images.motherlessmedia.com" or mlessvidid_parts.netloc=="cdn3-videos.motherlessmedia.com" or mlessvidid_parts.netloc=="cdn3-thumbs.motherlessmedia.com"):
  returnval = "download";
 if(mlessvidid_parts.netloc=="cdn4-images.motherlessmedia.com" or mlessvidid_parts.netloc=="cdn4-videos.motherlessmedia.com" or mlessvidid_parts.netloc=="cdn4-thumbs.motherlessmedia.com"):
  returnval = "download";
 if(mlessvidid_parts.netloc=="cdn5-images.motherlessmedia.com" or mlessvidid_parts.netloc=="cdn5-videos.motherlessmedia.com" or mlessvidid_parts.netloc=="cdn5-thumbs.motherlessmedia.com"):
  returnval = "download";
 if(returnval==False and len(mlessvidid)==2 and re.match("^([0-9A-F]+)$", mlessvidid[1])):
  returnval = "link";
 return returnval;

def get_motherless_link_type_alt(httpurl):
 httpurl = fix_motherless_url(httpurl);
 returnval = {'urlinfo': check_motherless_url(httpurl), 'motherlessinfo': get_motherless_link_type(httpurl)};
 return returnval;

def get_motherless_number_of_pages(httpurl, httpheaders, httpcookie, httplibuse="urllib"):
 httpurl = fix_motherless_url(httpurl);
 premrtext = download_from_url(httpurl, httpheaders, httpcookie, httplibuse);
 mrtext = premrtext['Content'];
 if(sys.version[0]>="3"):
  mrtext = mrtext.decode('ascii', 'replace');
 mregex_getpagenum = re.escape("\" class=\"pop\" rel=\"")+'?\'?([^"\'>]*)'+re.escape("\">")+"([0-9]+)"+re.escape("</a>");
 mlesspagenum = re.findall(mregex_getpagenum, mrtext);
 try:
  returnval = int(mlesspagenum[-1][0]);
 except:
  returnval = 1;
 return returnval;

def get_motherless_user_info(username, motherless_serv=None):
 motherless_subdomain = "cdn-";
 if(motherless_serv==None):
  motherless_serv = "";
 if(motherless_serv!="" and (motherless_serv<5 or motherless_serv>0)):
  motherless_subdomain = "cdn"+str(motherless_serv)+"-";
 if(motherless_serv==""):
  motherless_subdomain = "cdn-";
 returnval = {'username': username};
 avatarfilenameext = os.path.basename(urlparse.urljoin("http://"+motherless_subdomain+"avatars.motherlessmedia.com/thumbs/"+username+"-avatar.jpg", urlparse.urlparse("http://"+motherless_subdomain+"avatars.motherlessmedia.com/thumbs/"+username+"-avatar.jpg").path));
 avatarfilename, avatarfileextension = os.path.splitext(avatarfilenameext);
 returnval.update({'orginurl': "http://motherless.com/m/"+username});
 returnval.update({'orginurltype': "profile"});
 returnval.update({'url': "http://motherless.com/m/"+username});
 returnval.update({'urltype': "profile"});
 returnval.update({'avatarurl': "http://"+motherless_subdomain+"avatars.motherlessmedia.com/thumbs/"+username+"-avatar.jpg"});
 returnval.update({'avatarfullfilename': avatarfilenameext});
 returnval.update({'avatarfilename': avatarfilename});
 returnval.update({'avatarextension': avatarfileextension});
 return returnval;

def get_motherless_links(httpurl, httpheaders, httpcookie, httplibuse="urllib", motherless_serv=None):
 httpurl = fix_motherless_url(httpurl);
 if(get_motherless_link_type(httpurl)!="link"):
  returnval = False;
  return returnval;
 motherless_subdomain = "cdn-";
 if(motherless_serv==None):
  motherless_serv = "";
 if(motherless_serv!="" and (motherless_serv<5 or motherless_serv>0)):
  motherless_subdomain = "cdn"+str(motherless_serv)+"-";
 if(motherless_serv==""):
  motherless_subdomain = "cdn-";
 premrtext = download_from_url(httpurl, httpheaders, httpcookie, httplibuse);
 mrtext = premrtext['Content'];
 if(sys.version[0]>="3"):
  mrtext = mrtext.decode('ascii', 'replace');
 mregex_gettitle = re.escape("http://cdn")+"([1-5])"+re.escape("-");
 mrtext = re.sub(mregex_gettitle, "http://cdn-", mrtext);
 mregex_gettitle = re.escape("<h1 class=\"ellipsis gold\" id=\"view-upload-title\">\n                        ")+"(.*)"+re.escape("                    </h1>");
 mlesstitle = re.findall(mregex_gettitle, mrtext);
 mregex_geturlone = re.escape("__fileurl = '")+'?\'?([^"\'>]*)'+re.escape("';");
 mlesslinkone = re.findall(mregex_geturlone, mrtext);
 mregex_geturlonetype = re.escape("https://")+"cdn([1-5]+)\-"+"(images|videos)"+re.escape(".motherlessmedia.com/")+"(images|videos)"+re.escape("/")+"([\w\/\?\&\=\.\-]+)";
 mlesslinkonetype = re.findall(mregex_geturlonetype, mrtext);
 mregex_geturltwo = re.escape("<meta property=\"og:image\" content=\"")+'?\'?([^"\'>]*)'+re.escape("\">");
 mlesslinktwo = re.findall(mregex_geturltwo, mrtext);
 mregex_geturltwotype = re.escape("https://")+"cdn([1-5]+)\-"+"(images|thumbs)"+re.escape(".motherlessmedia.com/")+"(images|thumbs)"+re.escape("/")+"([\w\/\?\&\=\.\-]+)";
 mlesslinktwotype = re.findall(mregex_geturltwotype, mrtext);
 filenameext = os.path.basename(urlparse.urljoin(mlesslinkone[0], urlparse.urlparse(mlesslinkone[0]).path));
 filename, fileextension = os.path.splitext(filenameext);
 thumbfilenameext = os.path.basename(urlparse.urljoin(mlesslinktwo[0], urlparse.urlparse(mlesslinktwo[0]).path));
 thumbfilename, thumbfileextension = os.path.splitext(thumbfilenameext);
 mregex_getuname = re.escape("<tr rel=\"")+'?\'?([^"\'>]*)'+re.escape("\"");
 mlessuname = re.findall(mregex_getuname, mrtext);
 mlessuname = mlessuname[0];
 mregex_geturlname = re.escape("<td class=\"thumb-member-avatar\">\n		<a href=\"")+'?\'?([^"\'>]*)'+re.escape("\" target=\"_blank\">\n                <img");
 mlessurlname = re.findall(mregex_geturlname, mrtext);
 mlessurlname = mlessurlname[0].replace("/m/", "");
 mregex_getavatar = re.escape("<img\n            src=\"")+'?\'?([^"\'>]*)'+re.escape("\"\n            class=\"avatar avatar-small\"");
 mlessavatar = re.findall(mregex_getavatar, mrtext);
 mlessavatar = mlessavatar[0];
 avatarfilenameext = os.path.basename(urlparse.urljoin(mlessavatar, urlparse.urlparse(mlessavatar).path));
 avatarfilename, avatarfileextension = os.path.splitext(avatarfilenameext);
 mregex_getviews = re.escape("<strong>Views</strong>\n")+"([\s+|\t]+)([0-9\,]+)([\s+\t]+)"+re.escape("</h2>");
 mlessviews = re.findall(mregex_getviews, mrtext);
 mregex_getfavorited = re.escape("<strong>Favorited</strong>\n")+"([\s+\t]+)([0-9\,]+)([\s+\t]+)"+re.escape("</h2>");
 mlessfavorited = re.findall(mregex_getfavorited, mrtext);
 if(mlesslinkonetype[0][2]=="images"):
  thumbnailaltpart = thumbfilename+"-zoom"+thumbfileextension;
  thumbnailalt = "http://cdn"+mlesslinktwotype[0][0]+"-thumbs.motherlessmedia.com/thumbs/"+thumbnailaltpart;
  thumbnailaltfilenameext = os.path.basename(urlparse.urljoin(thumbnailalt, urlparse.urlparse(thumbnailalt).path));
  thumbnailaltfilename, thumbnailaltfileextension = os.path.splitext(thumbnailaltfilenameext);
 if(mlesslinkonetype[0][2]=="videos"):
  thumbnailaltpart = thumbfilename+"-small"+thumbfileextension;
  thumbnailalt = "http://cdn"+mlesslinktwotype[0][0]+"-thumbs.motherlessmedia.com/thumbs/"+thumbnailaltpart;
  thumbnailaltfilenameext = os.path.basename(urlparse.urljoin(thumbnailalt, urlparse.urlparse(thumbnailalt).path));
  thumbnailaltfilename, thumbnailaltfileextension = os.path.splitext(thumbnailaltfilenameext);
  stripimgpart = thumbfilename+"-strip"+thumbfileextension;
  stripimg = "http://cdn"+mlesslinktwotype[0][0]+"-thumbs.motherlessmedia.com/thumbs/"+stripimgpart;
  stripimgfilenameext = os.path.basename(urlparse.urljoin(stripimg, urlparse.urlparse(stripimg).path));
  stripimgfilename, stripimgfileextension = os.path.splitext(stripimgfilenameext);
 returnval = False;
 mlessurltype = get_motherless_link_type(mlesslinkone[0]);
 if(mlesslinkonetype[0][2]=="images"):
  regex_getimgsize = re.escape("style=\"width: ")+"([0-9]+)"+re.escape("px; height: ")+"([0-9]+)"+re.escape("px;\"");
  mlessgetimgsize = re.findall(regex_getimgsize, mrtext);
  returnval = {'type': mlesslinkonetype[0][2], 'urltype': mlessurltype, 'url': mlesslinkone[0], 'height': int(mlessgetimgsize[0][1]), 'width': int(mlessgetimgsize[0][0]), 'orginurl': httpurl, 'orginurltype': get_motherless_link_type(httpurl), 'thumbnail': mlesslinktwo[0].replace("images", "thumbs"), 'thumbnailalt': thumbnailalt+"?from_helper", 'title': mlesstitle[0], 'fullfilename': filenameext, 'filename': filename, 'extension': fileextension, 'thumbfullfilename': thumbfilenameext, 'thumbfilename': thumbfilename, 'thumbextension': thumbfileextension, 'thumbnailaltfullfilename': thumbnailaltpart, 'thumbnailaltfilename': thumbnailaltfilename, 'thumbnailaltextension': thumbnailaltfileextension, 'userinfo': get_motherless_user_info(mlessuname), 'username': mlessuname, 'avatarurl': mlessavatar, 'avatarfullfilename': avatarfilenameext, 'avatarfilename': avatarfilename, 'avatarextension': avatarfileextension, 'numberofviews': int(mlessviews[0][1].replace(',', '')), 'numberoffavorites': int(mlessfavorited[0][1].replace(',', ''))};
 if(mlesslinkonetype[0][2]=="videos"):
  returnval = {'type': mlesslinkonetype[0][2], 'url': mlesslinkone[0], 'orginurl': httpurl, 'orginurltype': get_motherless_link_type(httpurl), 'thumbnail': thumbnailalt+"?from_helper", 'thumbnailalt': mlesslinktwo[0].replace("images", "thumbs"), 'strip': stripimg+"?from_helper", 'title': mlesstitle[0], 'fullfilename': filenameext, 'filename': filename, 'extension': fileextension, 'thumbfullfilename': thumbnailaltpart, 'thumbfilename': thumbnailaltfilename, 'thumbextension': thumbnailaltfileextension, 'thumbnailaltfullfilename': thumbfilenameext, 'thumbnailaltfilename': thumbfilename, 'thumbnailaltextension': thumbfileextension, 'stripfullfilename': stripimgfilenameext, 'stripfilename': stripimgfilename, 'stripextension': stripimgfileextension, 'userinfo': get_motherless_user_info(mlessuname), 'username': mlessuname, 'avatarurl': mlessavatar, 'avatarfullfilename': avatarfilenameext, 'avatarfilename': avatarfilename, 'avatarextension': avatarfileextension, 'numberofviews': int(mlessviews[0][1].replace(',', '')), 'numberoffavorites': int(mlessfavorited[0][1].replace(',', ''))};
 return returnval;

def get_motherless_links_from_url(httpurl, httpheaders, httpcookie, httplibuse="urllib"):
 httpurl = fix_motherless_url(httpurl);
 if(get_motherless_link_type(httpurl)!="download"):
  returnval = False;
  return returnval;
 returnval = False;
 if(get_motherless_link_type(httpurl)=="download"):
  urlparts = urlparse.urlparse(httpurl);
  filewithext = os.path.split(urlparts.path);
  if(filewithext[0]=="/images"):
   filewithoutext = os.path.splitext(filewithext[1])[0];
   returnval = get_motherless_links("http://motherless.com/"+filewithoutext, httpheaders, httpcookie, httplibuse="urllib");
  if(filewithext[0]=="/thumbs"):
   filewithoutext = os.path.splitext(filewithext[1])[0];
   filewithoutext = filewithoutext.replace("-zoom", "");
   filewithoutext = filewithoutext.replace("-small", "");
   filewithoutext = filewithoutext.replace("-strip", "");
   returnval = get_motherless_links("http://motherless.com/"+filewithoutext, httpheaders, httpcookie, httplibuse="urllib");
 return returnval;

def get_motherless_external_links(httpurl, httpheaders, httpcookie, httplibuse="urllib"):
 httpurl = fix_motherless_url(httpurl);
 if(get_motherless_link_type(httpurl)!="board" and get_motherless_link_type(httpurl)!="link"):
  returnval = False;
  return returnval;
 premrtext = download_from_url(httpurl, httpheaders, httpcookie, httplibuse);
 mrtext = premrtext['Content'];
 if(sys.version[0]>="3"):
  mrtext = mrtext.decode('ascii', 'replace');
 mregex_geturlinternal = re.escape("<a href=\"")+'?\'?([^"\'>]*)'+re.escape("\" rev=\"outbound\" rel=\"nofollow\" class=\"pop\" target=\"_blank\" title=\"motherless link\">");
 mlesslinkinternal = re.findall(mregex_geturlinternal, mrtext);
 mregex_geturlexternal = re.escape("<a href=\"")+'?\'?([^"\'>]*)'+re.escape("\" rev=\"outbound\" rel=\"nofollow\" class=\"pop\" target=\"_blank\" title=\"external link\">");
 mlesslinkexternal = re.findall(mregex_geturlexternal, mrtext);
 returnvalone = None;
 if(len(mlesslinkinternal)>1):
  mli = 0;
  mlil = len(mlesslinkinternal);
  returnvalone = {'numoflinks': mlil};
  returnvalone.update({'numofalllinks': len(mlesslinkinternal)});
  returnvalone.update({'orginurl': httpurl});
  returnvalone.update({'orginurltype': get_motherless_link_type(httpurl)});
  mlessrooturltype = get_motherless_link_type(httpurl);
  returnvalone.update({'urltype': mlessrooturltype});
  while(mli<mlil):
   mlessurltype = get_motherless_link_type(mlesslinkinternal[mli]);
   returnvalone.update({mli: {'urltype': mlessurltype, 'url': mlesslinkinternal[mli]} });
   mli = mli + 1;
 returnvaltwo = None;
 if(len(mlesslinkexternal)>1):
  mli = 0;
  mlil = len(mlesslinkexternal);
  returnvaltwo = {'numoflinks': mlil};
  returnvaltwo.update({'numofalllinks': len(mlesslinkexternal)});
  returnvaltwo.update({'orginurl': httpurl});
  returnvaltwo.update({'orginurltype': get_motherless_link_type(httpurl)});
  mlessrooturltype = get_motherless_link_type(httpurl);
  returnvaltwo.update({'urltype': mlessrooturltype});
  while(mli<mlil):
   returnvaltwo.update({mli: {'urltype': "external", 'url': mlesslinkexternal[mli]} });
   mli = mli + 1;
 if(returnvalone==None and returnvaltwo==None):
  returnval = {'internal': None, 'external': None};
 if(not returnvalone==None and not returnvaltwo==None):
  returnval = {'internal': returnvalone, 'external': returnvaltwo};
 if(not returnvalone==None and returnvaltwo==None):
  returnval = {'internal': returnvalone, 'external': None};
 if(returnvalone==None and not returnvaltwo==None):
  returnval = {'internal': None, 'external': returnvaltwo};
 return returnval;

def get_motherless_galleries_links(httpurl, httpheaders, httpcookie, httplibuse="urllib", page=1, getlinks=[0, -1], motherless_serv=None):
 httpurl = fix_motherless_url(httpurl);
 if(get_motherless_link_type(httpurl)!="gallery"):
  returnval = False;
  return returnval;
 motherless_subdomain = "cdn-";
 if(motherless_serv==None):
  motherless_serv = "";
 if(motherless_serv!="" and (motherless_serv<5 or motherless_serv>0)):
  motherless_subdomain = "cdn"+str(motherless_serv)+"-";
 if(motherless_serv==""):
  motherless_subdomain = "cdn-";
 premrtext = download_from_url(httpurl, httpheaders, httpcookie, httplibuse);
 mrtext = premrtext['Content'];
 if(sys.version[0]>="3"):
  mrtext = mrtext.decode('ascii', 'replace');
 mregex_getpagenum = re.escape("\" class=\"pop\" rel=\"")+'?\'?([^"\'>]*)'+re.escape("\">")+"([0-9]+)"+re.escape("</a>");
 mlesspagenum = re.findall(mregex_getpagenum, mrtext);
 try:
  lastpage = int(mlesspagenum[-1][0]);
 except:
  lastpage = 1;
 if(page>lastpage):
  page = lastpage;
 httpurl = add_url_param(httpurl, page=str(page));
 premrtext = download_from_url(httpurl, httpheaders, httpcookie, httplibuse);
 mrtext = premrtext['Content'];
 if(sys.version[0]>="3"):
  mrtext = mrtext.decode('ascii', 'replace');
 mregex_geturlone = re.escape("<a href=\"")+'?\'?([^"\'>]*)'+re.escape("\" class=\"img-container\" target=\"_self\">");
 mrtext_tmp = re.sub(re.escape("http://motherless.com"), "", mrtext);
 mrtext_tmp = re.sub(re.escape("http://www.motherless.com"), "", mrtext_tmp);
 mrtext_tmp = re.sub(re.escape("http://motherless.com"), "", mrtext_tmp);
 mrtext_tmp = re.sub(re.escape("http://www.motherless.com"), "", mrtext_tmp);
 mlesslinkone = re.findall(mregex_geturlone, mrtext_tmp);
 mregex_geturltwo = re.escape("<img class=\"static\" src=\"")+'?\'?([^"\'>]*)'+re.escape("\" data-strip-src=\"")+'?\'?([^"\'>]*)'+re.escape("\" alt=\"")+'?\'?([^">]*)'+re.escape("\" />");
 mlesslinktwo = re.findall(mregex_geturltwo, mrtext);
 mregex_getcaption = re.escape("<h2 class=\"caption title\">")+"(.*)"+re.escape("</h2>");
 mlesscaption = re.findall(mregex_getcaption, mrtext);
 mregex_gethits = re.escape("<div class=\"caption right\">")+"([0-9\,]+)"+re.escape(" Hits</div>");
 mlesshits = re.findall(mregex_gethits, mrtext);
 if(len(mlesshits)<1):
  mregex_gethits = re.escape("<div class=\"caption right\">\n        ")+"([0-9\,]+)"+re.escape(" Hits\n    </div>");
  mlesshits = re.findall(mregex_gethits, mrtext);
 mregex_getuserinfo = re.escape("<a class=\"caption left\" href=\"")+'?\'?([^"\'>]*)'+re.escape("\">");
 mlessuname = re.findall(mregex_getuserinfo, mrtext);
 mregex_getmediainfo = re.escape("data-size=\"")+'?\'?([^"\'>]*)'+re.escape("\" ")+re.escape("data-is-premium=\"")+'?\'?([^"\'>]*)'+re.escape("\" ")+re.escape("data-codename=\"")+'?\'?([^"\'>]*)'+re.escape("\" ")+re.escape("data-mediatype=\"")+'?\'?([^"\'>]*)'+re.escape("\" ")+re.escape("data-gallery-codename=\"")+'?\'?([^"\'>]*)'+re.escape("\" ")+re.escape("data-frames=\"")+'?\'?([^"\'>]*)'+re.escape("\">");
 mlessmediainfo = re.findall(mregex_getmediainfo, mrtext);
 if(getlinks[1]>len(mlesslinkone) or getlinks[1]==-1):
  getlinks[1] = len(mlesslinkone);
 if(getlinks[0]>getlinks[1] and not getlinks[1]==-1):
  tmpgetlinks0 = getlinks[0];
  tmpgetlinks1 = getlinks[1];
  getlinks[0] = tmpgetlinks1;
  getlinks[1] = tmpgetlinks0;
 if(getlinks[0]<0):
  getlinks[0] = 0;
 mli = getlinks[0];
 mlil = getlinks[1];
 returnval = {'pages': lastpage};
 returnval.update({'curpage': page});
 returnval.update({'numoflinks': mlil});
 returnval.update({'numofalllinks': len(mlesslinkone)});
 returnval.update({'orginurl': httpurl});
 returnval.update({'orginurltype': get_motherless_link_type(httpurl)});
 mlessrooturltype = get_motherless_link_type(httpurl);
 returnval.update({'urltype': mlessrooturltype});
 while(mli<mlil):
  mlessuname[mli] = mlessuname[mli].replace("/m/", "");
  stripfilenameext = os.path.basename(urlparse.urljoin(mlesslinktwo[mli][1], urlparse.urlparse(mlesslinktwo[mli][1]).path));
  stripfilename, stripfileextension = os.path.splitext(stripfilenameext);
  thumbfilenameext = os.path.basename(urlparse.urljoin(mlesslinktwo[mli][0], urlparse.urlparse(mlesslinktwo[mli][0]).path));
  thumbfilename, thumbfileextension = os.path.splitext(thumbfilenameext);
  mlessurltype = get_motherless_link_type("http://motherless.com/"+mlesslinkone[mli]);
  avatarfilenameext = os.path.basename(urlparse.urljoin("http://"+motherless_subdomain+"avatars.motherlessmedia.com/thumbs/"+mlessuname[mli]+"-avatar.jpg", urlparse.urlparse("http://"+motherless_subdomain+"avatars.motherlessmedia.com/thumbs/"+mlessuname[mli]+"-avatar.jpg").path));
  avatarfilename, avatarfileextension = os.path.splitext(avatarfilenameext);
  if(mlessmediainfo[mli][3]=="image"):
   returnval.update({mli: {'type': "images", 'urltype': mlessurltype, 'url': "http://motherless.com"+mlesslinkone[mli], 'thumbnail': mlesslinktwo[mli][0], 'thumbnailalt': mlesslinktwo[mli][1], 'title': mlesslinktwo[mli][2], 'thumbfullfilename': thumbfilenameext, 'thumbfilename': thumbfilename, 'thumbextension': thumbfileextension, 'thumbnailaltfullfilename': stripfilenameext, 'thumbnailaltfilename': stripfilename, 'thumbnailaltextension': stripfileextension, 'userinfo': get_motherless_user_info(mlessuname[mli]), 'username': mlessuname[mli], 'avatarurl': "http://"+motherless_subdomain+"avatars.motherlessmedia.com/thumbs/"+mlessuname[mli]+"-avatar.jpg", 'avatarfullfilename': avatarfilenameext, 'avatarfilename': avatarfilename, 'avatarextension': avatarfileextension, 'numberofviews': int(mlesshits[mli].replace(',', ''))} });
  if(mlessmediainfo[mli][3]=="video"):
   altthumbnail = mlesslinktwo[mli][1].replace('-strip', '');
   altfilenameext = os.path.basename(urlparse.urljoin(mlesslinktwo[mli][1], urlparse.urlparse(mlesslinktwo[mli][1]).path));
   altfilename, altfileextension = os.path.splitext(altfilenameext);
   returnval.update({mli: {'type': "videos", 'urltype': mlessurltype, 'url': "http://motherless.com"+mlesslinkone[mli], 'thumbnail': mlesslinktwo[mli][0], 'strip': mlesslinktwo[mli][1], 'thumbnailalt': altthumbnail, 'title': mlesslinktwo[mli][2], 'thumbfullfilename': thumbfilenameext, 'thumbfilename': thumbfilename, 'thumbextension': thumbfileextension, 'stripfullfilename': stripfilenameext, 'stripfilename': stripfilename, 'stripextension': stripfileextension, 'thumbnailaltfullfilename': altfilenameext, 'thumbnailaltfilename': altfilename, 'thumbnailaltextension': altfileextension, 'userinfo': get_motherless_user_info(mlessuname[mli]), 'username': mlessuname[mli], 'avatarurl': "http://"+motherless_subdomain+"avatars.motherlessmedia.com/thumbs/"+mlessuname[mli]+"-avatar.jpg", 'avatarfullfilename': avatarfilenameext, 'avatarfilename': avatarfilename, 'avatarextension': avatarfileextension, 'numberofviews': int(mlesshits[mli].replace(',', ''))} });
  mli = mli + 1;
 return returnval;

def get_motherless_random_links(httpheaders, httpcookie, httplibuse="urllib", linktype="video", getlinks=[0, 80]):
 if(getlinks[0]>getlinks[1] and not getlinks[1]==-1):
  tmpgetlinks0 = getlinks[0];
  tmpgetlinks1 = getlinks[1];
  getlinks[0] = tmpgetlinks1;
  getlinks[1] = tmpgetlinks0;
 if(getlinks[0]<0):
  getlinks[0] = 0;
 mli = getlinks[0];
 mlil = getlinks[1];
 if(linktype=="image"):
  returnval = {'pages': 1};
  returnval.update({'curpage': 1});
  returnval.update({'numoflinks': 80});
  returnval.update({'numofalllinks': mlil});
  returnval.update({'orginurl': "http://motherless.com/random/image"});
  returnval.update({'orginurltype': "gallery"});
  returnval.update({'urltype': "gallery"});
  while(mli<mlil):
   get_links = get_motherless_links("http://motherless.com/random/image", httpheaders, httpcookie, httplibuse);
   returnval.update({mli: {'type': "images", 'urltype': get_motherless_link_type("http://motherless.com/"+get_links['filename']), 'url': "http://motherless.com/"+get_links['filename'], 'thumbnail': get_links['thumbnail'], 'strip': get_links['thumbnailalt'], 'title': get_links['title'], 'thumbfullfilename': get_links['thumbfullfilename'], 'thumbfilename': get_links['thumbfilename'], 'thumbextension': get_links['thumbextension'], 'stripfullfilename': get_links['thumbnailaltfullfilename'], 'stripfilename': get_links['thumbnailaltextension'], 'stripextension': get_links['thumbnailaltfilename'], 'userinfo': get_motherless_user_info(get_links['username']), 'username': get_links['username'], 'avatarurl': get_links['avatarurl'], 'avatarfullfilename': get_links['avatarfullfilename'], 'avatarfilename': get_links['avatarfilename'], 'avatarextension': get_links['avatarextension']} });
   mli = mli + 1;
 if(linktype=="video"):
  returnval = {'pages': 1};
  returnval.update({'curpage': 1});
  returnval.update({'numoflinks': 80});
  returnval.update({'numofalllinks': mlil});
  returnval.update({'orginurl': "http://motherless.com/random/video"});
  returnval.update({'orginurltype': "gallery"});
  returnval.update({'urltype': "gallery"});
  while(mli<mlil):
   get_links = get_motherless_links("http://motherless.com/random/video", httpheaders, httpcookie, httplibuse);
   returnval.update({mli: {'type': "videos", 'urltype': get_motherless_link_type("http://motherless.com/"+get_links['filename']), 'url': "http://motherless.com/"+get_links['filename'], 'thumbnail': get_links['thumbnail'], 'strip': get_links['thumbnailalt'], 'title': get_links['title'], 'thumbfullfilename': get_links['thumbfullfilename'], 'thumbfilename': get_links['thumbfilename'], 'thumbextension': get_links['thumbextension'], 'stripfullfilename': get_links['thumbnailaltfullfilename'], 'stripfilename': get_links['thumbnailaltextension'], 'stripextension': get_links['thumbnailaltfilename'], 'userinfo': get_motherless_user_info(get_links['username']), 'username': get_links['username'], 'avatarurl': get_links['avatarurl'], 'avatarfullfilename': get_links['avatarfullfilename'], 'avatarfilename': get_links['avatarfilename'], 'avatarextension': get_links['avatarextension']} });
   mli = mli + 1;
 return returnval;

def get_motherless_random_links_alt(httpheaders, httpcookie, httplibuse="urllib", linktype="video", getlinks=[0, 80]):
 if(getlinks[0]>getlinks[1] and not getlinks[1]==-1):
  tmpgetlinks0 = getlinks[0];
  tmpgetlinks1 = getlinks[1];
  getlinks[0] = tmpgetlinks1;
  getlinks[1] = tmpgetlinks0;
 if(getlinks[0]<0):
  getlinks[0] = 0;
 mli = getlinks[0];
 mlil = getlinks[1];
 if(linktype=="image"):
  returnval = {'pages': 1};
  returnval.update({'curpage': 1});
  returnval.update({'numoflinks': 80});
  returnval.update({'numofalllinks': mlil});
  returnval.update({'orginurl': "http://motherless.com/random/image"});
  returnval.update({'orginurltype': "gallery"});
  returnval.update({'urltype': "gallery"});
  while(mli<mlil):
   get_links = get_motherless_links("http://motherless.com/random/image", httpheaders, httpcookie, httplibuse);
   returnval.update({mli: get_links});
   mli = mli + 1;
 if(linktype=="video"):
  returnval = {'pages': 1};
  returnval.update({'curpage': 1});
  returnval.update({'numoflinks': 80});
  returnval.update({'numofalllinks': mlil});
  returnval.update({'orginurl': "http://motherless.com/random/video"});
  returnval.update({'orginurltype': "gallery"});
  returnval.update({'urltype': "gallery"});
  while(mli<mlil):
   get_links = get_motherless_links("http://motherless.com/random/video", httpheaders, httpcookie, httplibuse);
   returnval.update({mli: get_links});
   mli = mli + 1;
 return returnval;

def get_motherless_boards_links(httpurl, httpheaders, httpcookie, httplibuse="urllib", geturlinfo=False, getlinks=[0, -1], motherless_serv=None):
 httpurl = fix_motherless_url(httpurl);
 if(get_motherless_link_type(httpurl)!="board"):
  returnval = False;
  return returnval;
 motherless_subdomain = "cdn-";
 if(motherless_serv==None):
  motherless_serv = "";
 if(motherless_serv!="" and (motherless_serv<5 or motherless_serv>0)):
  motherless_subdomain = "cdn"+str(motherless_serv)+"-";
 if(motherless_serv==""):
  motherless_subdomain = "cdn-";
 premrtext = download_from_url(httpurl, httpheaders, httpcookie, httplibuse);
 mrtext = premrtext['Content'];
 if(sys.version[0]>="3"):
  mrtext = mrtext.decode('ascii', 'replace');
 mrtext_tmp = re.sub(re.escape("http://motherless.com"), "", mrtext);
 mrtext_tmp = re.sub(re.escape("http://www.motherless.com"), "", mrtext_tmp);
 mrtext_tmp = re.sub(re.escape("http://motherless.com"), "", mrtext_tmp);
 mrtext_tmp = re.sub(re.escape("http://www.motherless.com"), "", mrtext_tmp);
 mregex_geturlone = re.escape("<a href=\"")+'?\'?([^"\'>]*)'+re.escape("\" title=\"motherless link\">");
 mlesslinkone = re.findall(mregex_geturlone, mrtext_tmp);
 mregex_geturlname = re.escape("<a href=\"")+'?\'?([^"\'>]*)'+re.escape("\" class=\"post-username special-member op-member\" title=\"op\" rel=\"")+'?\'?([^"\'>]*)'+re.escape("\">");
 mlessurlname = re.findall(mregex_geturlname, mrtext);
 mregex_getdatasrc = re.escape("data-src=\"")+'?\'?([^"\'>]*)'+re.escape("\"");
 mlessdatasrc = re.findall(mregex_getdatasrc, mrtext_tmp);
 print(mlessdatasrc);
 mlessavaturl = "http://"+motherless_subdomain+"avatars.motherlessmedia.com/thumbs/"+mlessurlname[0][1]+"-avatar.jpg";
 avatarfilenameext = os.path.basename(urlparse.urljoin(mlessavaturl, urlparse.urlparse(mlessavaturl).path));
 avatarfilename, avatarfileextension = os.path.splitext(avatarfilenameext);
 if(getlinks[1]>len(mlesslinkone) or getlinks[1]==-1):
  getlinks[1] = len(mlesslinkone);
 if(getlinks[0]>getlinks[1] and not getlinks[1]==-1):
  tmpgetlinks0 = getlinks[0];
  tmpgetlinks1 = getlinks[1];
  getlinks[0] = tmpgetlinks1;
  getlinks[1] = tmpgetlinks0;
 if(getlinks[0]<0):
  getlinks[0] = 0;
 mli = getlinks[0];
 mlil = getlinks[1];
 returnval = {'numoflinks': mlil};
 returnval.update({'numofalllinks': len(mlesslinkone)});
 returnval.update({'orginurl': httpurl});
 returnval.update({'orginurltype': get_motherless_link_type(httpurl)});
 mlessrooturltype = get_motherless_link_type(httpurl);
 returnval.update({'urltype': mlessrooturltype});
 returnval.update({'userinfo': get_motherless_user_info(mlessurlname[0][1])});
 returnval.update({'username': mlessurlname[0][1]});
 returnval.update({'avatarurl': mlessavaturl});
 returnval.update({'avatarfullfilename': avatarfilenameext});
 returnval.update({'avatarfilename': avatarfilename});
 returnval.update({'avatarextension': avatarfileextension});
 while(mli<mlil):
  mlessurltype = get_motherless_link_type("http://motherless.com"+mlesslinkone[mli]);
  mlessdlurltype = get_motherless_link_type(mlessdatasrc[mli]);
  if(geturlinfo==False):
   returnval.update({mli: {'urltype': mlessurltype, 'url': "http://motherless.com"+mlesslinkone[mli], 'downloadurl': mlessdatasrc[mli], 'downloadurltype': mlessdlurltype} });
  if(geturlinfo==True):
   returnval.update({mli: {'urltype': mlessurltype, 'urlinfo': get_motherless_links(httpurl, httpheaders, httpcookie, httplibuse, motherless_serv), 'url': "http://motherless.com"+mlesslinkone[mli], 'downloadurl': mlessdatasrc[mli], 'downloadurltype': mlessdlurltype} });
  mli = mli + 1;
 return returnval;

def get_motherless_boards_posts(httpurl, httpheaders, httpcookie, httplibuse="urllib", getposts=[0, -1], motherless_serv=None):
 httpurl = fix_motherless_url(httpurl);
 if(get_motherless_link_type(httpurl)!="board"):
  returnval = False;
  return returnval;
 motherless_subdomain = "cdn-";
 if(motherless_serv==None):
  motherless_serv = "";
 if(motherless_serv!="" and (motherless_serv<5 or motherless_serv>0)):
  motherless_subdomain = "cdn"+str(motherless_serv)+"-";
 if(motherless_serv==""):
  motherless_subdomain = "cdn-";
 premrtext = download_from_url(httpurl, httpheaders, httpcookie, httplibuse);
 mrtext = premrtext['Content'];
 if(sys.version[0]>="3"):
  mrtext = mrtext.decode('ascii', 'replace');
 mregex_getposts = "(\t+)"+re.escape("<p>")+"(.+?)"+re.escape("</p>")+"(\t+)";
 mlessposts = re.findall(mregex_getposts, mrtext);
 mregex_getuname = re.escape("<a href=\"")+'?\'?([^"\'>]*)'+re.escape("\"");
 mlessuname = re.findall(mregex_getuname, mrtext);
 mregex_getopuname = re.escape("<a href=\"")+'?\'?([^"\'>]*)'+re.escape("\" class=\"post-username special-member op-member\" title=\"op\" rel=\"")+'?\'?([^"\'>]*)'+re.escape("\">");
 mlessopuname = re.findall(mregex_getopuname, mrtext);
 if(getposts[1]>len(mlessposts) or getposts[1]==-1):
  getposts[1] = len(mlessposts);
 if(getposts[0]>getposts[1] and not getposts[1]==-1):
  tmpgetposts0 = getposts[0];
  tmpgetposts1 = getposts[1];
  getposts[0] = tmpgetposts1;
  getposts[1] = tmpgetposts0;
 if(getposts[0]<0):
  getposts[0] = 0;
 mli = getposts[0];
 mlil = getposts[1];
 returnval = {'numofposts': mlil};
 returnval.update({'numofallposts': len(mlessposts)});
 returnval.update({'orginurl': httpurl});
 returnval.update({'orginurltype': get_motherless_link_type(httpurl)});
 mlessrooturltype = get_motherless_link_type(httpurl);
 returnval.update({'urltype': mlessrooturltype});
 returnval.update({'userinfo': get_motherless_user_info(mlessopuname[0][1])});
 returnval.update({'username': mlessopuname[0][1]});
 avatarfilenameext = os.path.basename(urlparse.urljoin("http://"+motherless_subdomain+"avatars.motherlessmedia.com/thumbs/"+mlessopuname[0][1]+"-avatar.jpg", urlparse.urlparse("http://"+motherless_subdomain+"avatars.motherlessmedia.com/thumbs/"+mlessopuname[0][1]+"-avatar.jpg").path));
 avatarfilename, avatarfileextension = os.path.splitext(avatarfilenameext);
 returnval.update({'avatarurl': "http://"+motherless_subdomain+"avatars.motherlessmedia.com/thumbs/"+mlessopuname[0][1]+"-avatar.jpg"});
 returnval.update({'avatarfullfilename': avatarfilenameext});
 returnval.update({'avatarfilename': avatarfilename});
 returnval.update({'avatarextension': avatarfileextension});
 while(mli<mlil):
  avatarfilenameext = os.path.basename(urlparse.urljoin("http://"+motherless_subdomain+"avatars.motherlessmedia.com/thumbs/"+mlessuname[mli]+"-avatar.jpg", urlparse.urlparse("http://"+motherless_subdomain+"avatars.motherlessmedia.com/thumbs/"+mlessuname[mli]+"-avatar.jpg").path));
  avatarfilename, avatarfileextension = os.path.splitext(avatarfilenameext);
  returnval.update({mli: {'post': mlessposts[mli][1], 'userinfo': get_motherless_user_info(mlessuname[mli]), 'username': mlessuname[mli], 'avatarurl': "http://"+motherless_subdomain+"avatars.motherlessmedia.com/thumbs/"+mlessuname[mli]+"-avatar.jpg", 'avatarfullfilename': avatarfilenameext, 'avatarfilename': avatarfilename, 'avatarextension': avatarfileextension} });
  mli = mli + 1;
 return returnval;

def get_motherless_links_comments(httpurl, httpheaders, httpcookie, httplibuse="urllib", getposts=[0, -1], motherless_serv=None):
 httpurl = fix_motherless_url(httpurl);
 if(get_motherless_link_type(httpurl)!="link"):
  returnval = False;
  return returnval;
 motherless_subdomain = "cdn-";
 if(motherless_serv==None):
  motherless_serv = "";
 if(motherless_serv!="" and (motherless_serv<5 or motherless_serv>0)):
  motherless_subdomain = "cdn"+str(motherless_serv)+"-";
 if(motherless_serv==""):
  motherless_subdomain = "cdn-";
 premrtext = download_from_url(httpurl, httpheaders, httpcookie, httplibuse);
 mrtext = premrtext['Content'];
 if(sys.version[0]>="3"):
  mrtext = mrtext.decode('ascii', 'replace');
 mregex_getposts = re.escape("<div style=\"text-align: justify;\">\n")+"(\t+)(.+?)"+re.escape("</div>");
 mlessposts = re.findall(mregex_getposts, mrtext);
 mregex_getuname = re.escape("<div class=\"media-comment\" id=\"")+'?\'?([^"\'>]*)'+re.escape("\" rel=\"0\" rev=\"")+'?\'?([^"\'>]*)'+re.escape("\">");
 mlessuname = re.findall(mregex_getuname, mrtext);
 mregex_getopuname = re.escape("<tr rel=\"")+'?\'?([^"\'>]*)'+re.escape("\"");
 mlessopuname = re.findall(mregex_getopuname, mrtext);
 if(getposts[1]>len(mlessposts) or getposts[1]==-1):
  getposts[1] = len(mlessposts);
 if(getposts[0]>getposts[1] and not getposts[1]==-1):
  tmpgetposts0 = getposts[0];
  tmpgetposts1 = getposts[1];
  getposts[0] = tmpgetposts1;
  getposts[1] = tmpgetposts0;
 if(getposts[0]<0):
  getposts[0] = 0;
 mli = getposts[0];
 mlil = getposts[1];
 returnval = {'numofposts': mlil};
 returnval.update({'numofallposts': len(mlessposts)});
 returnval.update({'orginurl': httpurl});
 returnval.update({'orginurltype': get_motherless_link_type(httpurl)});
 mlessrooturltype = get_motherless_link_type(httpurl);
 returnval.update({'urltype': mlessrooturltype});
 returnval.update({'userinfo': get_motherless_user_info(mlessopuname[0])});
 returnval.update({'username': mlessopuname[0]});
 avatarfilenameext = os.path.basename(urlparse.urljoin("http://"+motherless_subdomain+"avatars.motherlessmedia.com/thumbs/"+mlessopuname[0]+"-avatar.jpg", urlparse.urlparse("http://"+motherless_subdomain+"avatars.motherlessmedia.com/thumbs/"+mlessopuname[0]+"-avatar.jpg").path));
 avatarfilename, avatarfileextension = os.path.splitext(avatarfilenameext);
 returnval.update({'avatarurl': "http://"+motherless_subdomain+"avatars.motherlessmedia.com/thumbs/"+mlessopuname[0]+"-avatar.jpg"});
 returnval.update({'avatarfullfilename': avatarfilenameext});
 returnval.update({'avatarfilename': avatarfilename});
 returnval.update({'avatarextension': avatarfileextension});
 while(mli<mlil):
  avatarfilenameext = os.path.basename(urlparse.urljoin("http://"+motherless_subdomain+"avatars.motherlessmedia.com/thumbs/"+mlessuname[mli][1]+"-avatar.jpg", urlparse.urlparse("http://"+motherless_subdomain+"avatars.motherlessmedia.com/thumbs/"+mlessuname[mli][1]+"-avatar.jpg").path));
  avatarfilename, avatarfileextension = os.path.splitext(avatarfilenameext);
  returnval.update({mli: {'post': mlessposts[mli][1], 'userinfo': get_motherless_user_info(mlessuname[mli][1]), 'username': mlessuname[mli][1], 'avatarurl': "http://"+motherless_subdomain+"avatars.motherlessmedia.com/thumbs/"+mlessuname[mli][1]+"-avatar.jpg", 'avatarfullfilename': avatarfilenameext, 'avatarfilename': avatarfilename, 'avatarextension': avatarfileextension} });
  mli = mli + 1;
 return returnval;

def get_motherless_search_members(httpurl, httpheaders, httpcookie, httplibuse="urllib", page=1, getlinks=[0, -1]):
 httpurl = fix_motherless_url(httpurl);
 if(get_motherless_link_type(httpurl)!="member"):
  returnval = False;
  return returnval;
 premrtext = download_from_url(httpurl, httpheaders, httpcookie, httplibuse);
 mrtext = premrtext['Content'];
 if(sys.version[0]>="3"):
  mrtext = mrtext.decode('ascii', 'replace');
 mregex_getpagenum = re.escape("\" class=\"pop\" rel=\"")+'?\'?([^"\'>]*)'+re.escape("\">")+"([0-9]+)"+re.escape("</a>");
 mlesspagenum = re.findall(mregex_getpagenum, mrtext);
 try:
  lastpage = int(mlesspagenum[-1][0]);
 except:
  lastpage = 1;
 if(page>lastpage):
  page = lastpage;
 httpurl = add_url_param(httpurl, page=str(page));
 premrtext = download_from_url(httpurl, httpheaders, httpcookie, httplibuse);
 mrtext = premrtext['Content'];
 if(sys.version[0]>="3"):
  mrtext = mrtext.decode('ascii', 'replace');
 mregex_getuname = re.escape("<tr rel=\"")+'?\'?([^"\'>]*)'+re.escape("\"");
 mlessuname = re.findall(mregex_getuname, mrtext);
 mregex_geturlname = re.escape("<a href=\"")+'?\'?([^"\'>]*)'+re.escape("\" target=\"_blank\">\n            <img");
 mlessurlname = re.findall(mregex_geturlname, mrtext);
 mregex_getavatar = re.escape("<img\n    src=\"")+'?\'?([^"\'>]*)'+re.escape("\"\n    class=\"avatar avatar-small\"");
 mlessavatar = re.findall(mregex_getavatar, mrtext);
 if(getlinks[1]>len(mlessuname) or getlinks[1]==-1):
  getlinks[1] = len(mlessuname);
 if(getlinks[0]>getlinks[1] and not getlinks[1]==-1):
  tmpgetlinks0 = getlinks[0];
  tmpgetlinks1 = getlinks[1];
  getlinks[0] = tmpgetlinks1;
  getlinks[1] = tmpgetlinks0;
 if(getlinks[0]<0):
  getlinks[0] = 0;
 mli = getlinks[0];
 mlil = getlinks[1];
 returnval = {'numoflinks': mlil};
 returnval.update({'numofalllinks': len(mlessuname)});
 returnval.update({'pages': lastpage});
 returnval.update({'curpage': page});
 returnval.update({'orginurl': httpurl});
 returnval.update({'orginurltype': get_motherless_link_type(httpurl)});
 mlessrooturltype = get_motherless_link_type(httpurl);
 returnval.update({'urltype': mlessrooturltype});
 while(mli<mlil):
  avatarfilenameext = os.path.basename(urlparse.urljoin(mlessavatar[mli], urlparse.urlparse(mlessavatar[mli]).path));
  avatarfilename, avatarfileextension = os.path.splitext(avatarfilenameext);
  mlessurlname[mli] = mlessurlname[mli].replace("/m/", "");
  mlessurltype = get_motherless_link_type("http://motherless.com/"+mlessurlname[mli]);
  returnval.update({mli: {'urltype': mlessurltype, 'url': "http://motherless.com/"+mlessurlname[mli], 'userinfo': get_motherless_user_info(mlessurlname[mli]), 'username': mlessuname[mli], 'avatarurl': mlessavatar[mli], 'avatarfullfilename': avatarfilenameext, 'avatarfilename': avatarfilename, 'avatarextension': avatarfileextension} });
  mli = mli + 1;
 return returnval;

def get_motherless_girls(httpheaders, httpcookie, httplibuse="urllib", getlinks=[0, -1]):
 premrtext = download_from_url("http://motherless.com/girls", httpheaders, httpcookie, httplibuse);
 mrtext = premrtext['Content'];
 if(sys.version[0]>="3"):
  mrtext = mrtext.decode('ascii', 'replace');
 mregex_getuname = re.escape("<a href=\"")+'?\'?([^"\'>]*)'+re.escape("\" rev=\"")+'?\'?([^"\'>]*)'+re.escape("\" rel=\"")+'?\'?([^"\'>]*)'+re.escape("\">");
 mlessuname = re.findall(mregex_getuname, mrtext);
 mregex_geturlname = re.escape("\n\t\t\t\t\t\t<a href=\"")+'?\'?([^"\'>]*)'+re.escape("\" target=\"_blank\">");
 mlessurlname = re.findall(mregex_geturlname, mrtext);
 if(getlinks[1]>len(mlessuname) or getlinks[1]==-1):
  getlinks[1] = len(mlessuname);
 if(getlinks[0]>getlinks[1] and not getlinks[1]==-1):
  tmpgetlinks0 = getlinks[0];
  tmpgetlinks1 = getlinks[1];
  getlinks[0] = tmpgetlinks1;
  getlinks[1] = tmpgetlinks0;
 if(getlinks[0]<0):
  getlinks[0] = 0;
 mli = getlinks[0];
 mlil = getlinks[1];
 returnval = {'numoflinks': mlil};
 returnval.update({'numofalllinks': len(mlessuname)});
 returnval.update({'orginurl': "http://motherless.com/girls"});
 returnval.update({'orginurltype': get_motherless_link_type("http://motherless.com/girls")});
 mlessrooturltype = get_motherless_link_type("http://motherless.com/girls");
 returnval.update({'urltype': mlessrooturltype});
 while(mli<mlil):
  avatarfilenameext = os.path.basename(urlparse.urljoin(mlessuname[mli][0], urlparse.urlparse(mlessuname[mli][0]).path));
  avatarfilename, avatarfileextension = os.path.splitext(avatarfilenameext);
  mlessurltype = get_motherless_link_type("http://motherless.com/"+mlessuname[mli][1]);
  returnval.update({mli: {'urltype': mlessurltype, 'url': "http://motherless.com/"+mlessuname[mli][1], 'userinfo': get_motherless_user_info(mlessuname[mli][1]), 'username': mlessuname[mli][1], 'avatarurl': mlessuname[mli][0], 'avatarfullfilename': avatarfilenameext, 'avatarfilename': avatarfilename, 'avatarextension': avatarfileextension} });
  mli = mli + 1;
 return returnval;

def get_motherless_team(httpheaders, httpcookie, httplibuse="urllib", getlinks=[0, -1]):
 premrtext = download_from_url("http://motherless.com/about", httpheaders, httpcookie, httplibuse);
 mrtext = premrtext['Content'];
 if(sys.version[0]>="3"):
  mrtext = mrtext.decode('ascii', 'replace');
 mregex_getuname = re.escape("<div class=\"about-us-member\">\n				<a href=\"")+'?\'?([^"\'>]*)'+re.escape("\"");
 mlessuname = re.findall(mregex_getuname, mrtext);
 mlessuname_odd = mlessuname[1::2];
 mlessuname_even = mlessuname[::2];
 mregex_getavatar = re.escape("<img\n        src=\"")+'?\'?([^"\'>]*)'+re.escape("\"\n        class=\"avatar avatar-")+"(full|medium)"+re.escape("\"");
 mlessavatar = re.findall(mregex_getavatar, mrtext);
 if(getlinks[1]>len(mlessuname_odd) or getlinks[1]==-1):
  getlinks[1] = len(mlessuname_odd);
 if(getlinks[0]>getlinks[1] and not getlinks[1]==-1):
  tmpgetlinks0 = getlinks[0];
  tmpgetlinks1 = getlinks[1];
  getlinks[0] = tmpgetlinks1;
  getlinks[1] = tmpgetlinks0;
 if(getlinks[0]<0):
  getlinks[0] = 0;
 mli = getlinks[0];
 mlil = getlinks[1];
 returnval = {'numoflinks': mlil};
 returnval.update({'numofalllinks': len(mlessuname)});
 returnval.update({'orginurl': "http://motherless.com/about"});
 returnval.update({'orginurltype': get_motherless_link_type("http://motherless.com/about")});
 mlessrooturltype = get_motherless_link_type("http://motherless.com/about");
 returnval.update({'urltype': mlessrooturltype});
 while(mli<mlil):
  avatarfilenameext = os.path.basename(urlparse.urljoin(mlessavatar[mli][0], urlparse.urlparse(mlessavatar[mli][0]).path));
  avatarfilename, avatarfileextension = os.path.splitext(avatarfilenameext);
  mlessuname_odd[mli] = mlessuname_odd[mli].replace("/m/", "");
  mlessuname_even[mli] = mlessuname_even[mli].replace("/m/", "");
  mlessurltype = get_motherless_link_type("http://motherless.com/"+mlessuname_odd[mli]);
  returnval.update({mli: {'urltype': mlessurltype, 'url': "http://motherless.com/"+mlessuname_odd[mli], 'userinfo': get_motherless_user_info(mlessuname_odd[mli]), 'username': mlessuname_odd[mli], 'avatarurl': mlessavatar[mli][0], 'avatarfullfilename': avatarfilenameext, 'avatarfilename': avatarfilename, 'avatarextension': avatarfileextension} });
  mli = mli + 1;
 return returnval;

def get_motherless_top_referrers(httpheaders, httpcookie, httplibuse="urllib", getlinks=[0, -1]):
 premrtext = download_from_url("http://motherless.com/referers", httpheaders, httpcookie, httplibuse);
 mrtext = premrtext['Content'];
 if(sys.version[0]>="3"):
  mrtext = mrtext.decode('ascii', 'replace');
 mregex_geturlname = "([0-9]+)"+re.escape(". <a href=\"")+'?\'?([^"\'>]*)'+re.escape("\" class=\"pop\" target=\"_blank\" rel=\"nofollow\">\n						")+"(.*)"+re.escape("					</a>");
 mlessurlname = re.findall(mregex_geturlname, mrtext);
 if(getlinks[1]>len(mlessurlname) or getlinks[1]==-1):
  getlinks[1] = len(mlessurlname);
 if(getlinks[0]>getlinks[1] and not getlinks[1]==-1):
  tmpgetlinks0 = getlinks[0];
  tmpgetlinks1 = getlinks[1];
  getlinks[0] = tmpgetlinks1;
  getlinks[1] = tmpgetlinks0;
 if(getlinks[0]<0):
  getlinks[0] = 0;
 mli = getlinks[0];
 mlil = getlinks[1];
 returnval = {'numoflinks': mlil};
 returnval.update({'numofalllinks': len(mlessurlname)});
 returnval.update({'orginurl': "http://motherless.com/referers"});
 returnval.update({'orginurltype': get_motherless_link_type("http://motherless.com/referers")});
 mlessrooturltype = get_motherless_link_type("http://motherless.com/referers");
 returnval.update({'urltype': mlessrooturltype});
 while(mli<mlil):
  returnval.update({mli: {'urltype': "referer-links", 'url': mlessurlname[mli][1], 'title': mlessurlname[mli][2]} });
  mli = mli + 1;
 return returnval;

def get_motherless_top_referers(httpheaders, httpcookie, httplibuse="urllib", getlinks=[0, -1]):
 return get_motherless_top_referrers(httpheaders, httpcookie, httplibuse, getlinks);

def get_motherless_groups(httpurl, httpheaders, httpcookie, httplibuse="urllib", page=1, getlinks=[0, -1]):
 httpurl = fix_motherless_url(httpurl);
 if(get_motherless_link_type(httpurl)!="group"):
  returnval = False;
  return returnval;
 premrtext = download_from_url(httpurl, httpheaders, httpcookie, httplibuse);
 mrtext = premrtext['Content'];
 if(sys.version[0]>="3"):
  mrtext = mrtext.decode('ascii', 'replace');
 mregex_getpagenum = re.escape("\" class=\"pop\" rel=\"")+'?\'?([^"\'>]*)'+re.escape("\">")+"([0-9]+)"+re.escape("</a>");
 mlesspagenum = re.findall(mregex_getpagenum, mrtext);
 try:
  lastpage = int(mlesspagenum[-1][0]);
 except:
  lastpage = 1;
 if(page>lastpage):
  page = lastpage;
 httpurl = add_url_param(httpurl, page=str(page));
 premrtext = download_from_url(httpurl, httpheaders, httpcookie, httplibuse);
 mrtext = premrtext['Content'];
 if(sys.version[0]>="3"):
  mrtext = mrtext.decode('ascii', 'replace');
 mregex_getavatar = re.escape("<img\n        src=\"")+'?\'?([^"\'>]*)'+re.escape("\"\n        class=\"avatar avatar-")+"(full|medium)"+re.escape("\"");
 mlessavatar = re.findall(mregex_getavatar, mrtext);
 mregex_getgroups = re.escape("<a href=\"")+'?\'?([^"\'>]*)'+re.escape("\" class=\"grunge motherless-red\">\n")+"(.*)"+re.escape("</a>");
 mlessgroups = re.findall(mregex_getgroups, mrtext);
 if(getlinks[1]>len(mlessgroups) or getlinks[1]==-1):
  getlinks[1] = len(mlessgroups);
 if(getlinks[0]>getlinks[1] and not getlinks[1]==-1):
  tmpgetlinks0 = getlinks[0];
  tmpgetlinks1 = getlinks[1];
  getlinks[0] = tmpgetlinks1;
  getlinks[1] = tmpgetlinks0;
 if(getlinks[0]<0):
  getlinks[0] = 0;
 mli = getlinks[0];
 mlil = getlinks[1];
 returnval = {'pages': lastpage};
 returnval.update({'curpage': page});
 returnval.update({'numoflinks': mlil});
 returnval.update({'numofalllinks': len(mlessgroups)});
 returnval.update({'orginurl': httpurl});
 returnval.update({'orginurltype': get_motherless_link_type(httpurl)});
 while(mli<mlil):
  thumbfilenameext = os.path.basename(urlparse.urljoin(mlessavatar[mli][0], urlparse.urlparse(mlessavatar[mli][0]).path));
  thumbfilename, thumbfileextension = os.path.splitext(thumbfilenameext);
  returnval.update({mli: {'urltype': get_motherless_link_type("http://motherless.com/"+mlessgroups[mli][0]), 'url': "http://motherless.com"+mlessgroups[mli][0], 'urltype-image': get_motherless_link_type("http://motherless.com/"+mlessgroups[mli][0].replace("/g/", "/gi/")), 'url-image': "http://motherless.com"+mlessgroups[mli][0].replace("/g/", "/gi/"), 'urltype-video': get_motherless_link_type("http://motherless.com/"+mlessgroups[mli][0].replace("/g/", "/gv/")), 'url-video': "http://motherless.com"+mlessgroups[mli][0].replace("/g/", "/gv/"), 'urltype-member': get_motherless_link_type("http://motherless.com/"+mlessgroups[mli][0].replace("/g/", "/gm/")), 'url-member': "http://motherless.com"+mlessgroups[mli][0].replace("/g/", "/gm/"), 'thumbnail': mlessavatar[mli][0], 'title': mlessgroups[mli][1].strip(), 'thumbfullfilename': thumbfilenameext, 'thumbfilename': thumbfilename, 'thumbextension': thumbfileextension} });
  mli = mli + 1;
 return returnval;

def get_motherless_sample_links(httpheaders, httpcookie, httplibuse="urllib", numoflinks=10, urltype="video", enablerand=True):
 if(urltype=="video" and enablerand==True):
  returnval = {'numoflinks': numoflinks, 'orginurl': "http://motherless.com/videos", 'orginurltype': get_motherless_link_type("http://motherless.com/videos"), 'videos': {'recent': get_motherless_galleries_links("http://motherless.com/videos/recent", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'favorited': get_motherless_galleries_links("http://motherless.com/videos/favorited", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'viewed': get_motherless_galleries_links("http://motherless.com/videos/viewed", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'commented': get_motherless_galleries_links("http://motherless.com/videos/commented", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'popular': get_motherless_galleries_links("http://motherless.com/videos/popular", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'live': get_motherless_galleries_links("http://motherless.com/live/videos", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'random': get_motherless_random_links(httpheaders, httpcookie, httplibuse, "video", [0, numoflinks]) } };
 if(urltype=="video" and enablerand==False):
  returnval = {'numoflinks': numoflinks, 'orginurl': "http://motherless.com/videos", 'orginurltype': get_motherless_link_type("http://motherless.com/videos"), 'videos': {'recent': get_motherless_galleries_links("http://motherless.com/videos/recent", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'favorited': get_motherless_galleries_links("http://motherless.com/videos/favorited", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'viewed': get_motherless_galleries_links("http://motherless.com/videos/viewed", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'commented': get_motherless_galleries_links("http://motherless.com/videos/commented", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'popular': get_motherless_galleries_links("http://motherless.com/videos/popular", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'live': get_motherless_galleries_links("http://motherless.com/live/videos", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]) } };
 if(urltype=="image" and enablerand==True):
  returnval = {'numoflinks': numoflinks, 'orginurl': "http://motherless.com/images", 'orginurltype': get_motherless_link_type("http://motherless.com/images"), 'images': {'recent': get_motherless_galleries_links("http://motherless.com/images/recent", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'favorited': get_motherless_galleries_links("http://motherless.com/images/favorited", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'viewed': get_motherless_galleries_links("http://motherless.com/images/viewed", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'commented': get_motherless_galleries_links("http://motherless.com/images/commented", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'popular': get_motherless_galleries_links("http://motherless.com/images/popular", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'live': get_motherless_galleries_links("http://motherless.com/live/images", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'random': get_motherless_random_links(httpheaders, httpcookie, httplibuse, "image", [0, numoflinks]) } };
 if(urltype=="image" and enablerand==False):
  returnval = {'numoflinks': numoflinks, 'orginurl': "http://motherless.com/images", 'orginurltype': get_motherless_link_type("http://motherless.com/images"), 'images': {'recent': get_motherless_galleries_links("http://motherless.com/images/recent", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'favorited': get_motherless_galleries_links("http://motherless.com/images/favorited", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'viewed': get_motherless_galleries_links("http://motherless.com/images/viewed", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'commented': get_motherless_galleries_links("http://motherless.com/images/commented", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'popular': get_motherless_galleries_links("http://motherless.com/images/popular", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'live': get_motherless_galleries_links("http://motherless.com/live/images", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]) } };
 if(urltype=="gallery"):
  returnval = {'numoflinks': numoflinks, 'orginurl': "http://motherless.com/galleries", 'orginurltype': get_motherless_link_type("http://motherless.com/galleries"), 'galleries': {'updated': get_motherless_galleries_links("http://motherless.com/galleries/updated", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'created': get_motherless_galleries_links("http://motherless.com/galleries/created", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'viewed': get_motherless_galleries_links("http://motherless.com/galleries/viewed", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'favorited': get_motherless_galleries_links("http://motherless.com/galleries/favorited", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'commented': get_motherless_galleries_links("http://motherless.com/galleries/commented", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]) } };
 if(urltype=="all" and enablerand==True):
  returnval = {'numoflinks': numoflinks, 'orginurl': "http://motherless.com/", 'orginurltype': get_motherless_link_type("http://motherless.com/"), 'videos': {'recent': get_motherless_galleries_links("http://motherless.com/videos/recent", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'favorited': get_motherless_galleries_links("http://motherless.com/videos/favorited", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'viewed': get_motherless_galleries_links("http://motherless.com/videos/viewed", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'commented': get_motherless_galleries_links("http://motherless.com/videos/commented", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'popular': get_motherless_galleries_links("http://motherless.com/videos/popular", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'live': get_motherless_galleries_links("http://motherless.com/live/videos", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'random': get_motherless_random_links(httpheaders, httpcookie, httplibuse, "video", [0, numoflinks]) }, 'images': {'recent': get_motherless_galleries_links("http://motherless.com/images/recent", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'favorited': get_motherless_galleries_links("http://motherless.com/images/favorited", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'viewed': get_motherless_galleries_links("http://motherless.com/images/viewed", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'commented': get_motherless_galleries_links("http://motherless.com/images/commented", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'popular': get_motherless_galleries_links("http://motherless.com/images/popular", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'live': get_motherless_galleries_links("http://motherless.com/live/images", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'random': get_motherless_random_links(httpheaders, httpcookie, httplibuse, "image", [0, numoflinks]) }, 'galleries': {'updated': get_motherless_galleries_links("http://motherless.com/galleries/updated", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'created': get_motherless_galleries_links("http://motherless.com/galleries/created", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'viewed': get_motherless_galleries_links("http://motherless.com/galleries/viewed", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'favorited': get_motherless_galleries_links("http://motherless.com/galleries/favorited", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'commented': get_motherless_galleries_links("http://motherless.com/galleries/commented", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]) } };
 if(urltype=="all" and enablerand==False):
  returnval = {'numoflinks': numoflinks, 'orginurl': "http://motherless.com/", 'orginurltype': get_motherless_link_type("http://motherless.com/"), 'videos': {'recent': get_motherless_galleries_links("http://motherless.com/videos/recent", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'favorited': get_motherless_galleries_links("http://motherless.com/videos/favorited", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'viewed': get_motherless_galleries_links("http://motherless.com/videos/viewed", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'commented': get_motherless_galleries_links("http://motherless.com/videos/commented", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'popular': get_motherless_galleries_links("http://motherless.com/videos/popular", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'live': get_motherless_galleries_links("http://motherless.com/live/videos", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]) }, 'images': {'recent': get_motherless_galleries_links("http://motherless.com/images/recent", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'favorited': get_motherless_galleries_links("http://motherless.com/images/favorited", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'viewed': get_motherless_galleries_links("http://motherless.com/images/viewed", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'commented': get_motherless_galleries_links("http://motherless.com/images/commented", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'popular': get_motherless_galleries_links("http://motherless.com/images/popular", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'live': get_motherless_galleries_links("http://motherless.com/live/images", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]) }, 'galleries': {'updated': get_motherless_galleries_links("http://motherless.com/galleries/updated", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'created': get_motherless_galleries_links("http://motherless.com/galleries/created", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'viewed': get_motherless_galleries_links("http://motherless.com/galleries/viewed", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'favorited': get_motherless_galleries_links("http://motherless.com/galleries/favorited", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'commented': get_motherless_galleries_links("http://motherless.com/galleries/commented", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]) } };
 return returnval;

def get_motherless_link_by_type(httpurl, httpheaders, httpcookie, httplibuse="urllib", page=1, getlinks=[0, -1], motherless_serv=None):
 httpurl = fix_motherless_url(httpurl);
 returnval = False;
 if(get_motherless_link_type(httpurl)=="link"):
  returnval = get_motherless_links(httpurl, httpheaders, httpcookie, httplibuse, motherless_serv);
 if(get_motherless_link_type(httpurl)=="gallery"):
  returnval = get_motherless_galleries_links(httpurl, httpheaders, httpcookie, httplibuse, page, getlinks, motherless_serv);
 if(get_motherless_link_type(httpurl)=="sample-videos"):
  returnval = get_motherless_sample_links(httpheaders, httpcookie, httplibuse, 10, "video");
 if(get_motherless_link_type(httpurl)=="sample-images"):
  returnval = get_motherless_sample_links(httpheaders, httpcookie, httplibuse, 10, "image");
 if(get_motherless_link_type(httpurl)=="sample-galleries"):
  returnval = get_motherless_sample_links(httpheaders, httpcookie, httplibuse, 10, "gallery");
 if(get_motherless_link_type(httpurl)=="sample" or get_motherless_link_type(httpurl)=="sample-all"):
  returnval = get_motherless_sample_links(httpheaders, httpcookie, httplibuse, 10, "all");
 if(get_motherless_link_type(httpurl)=="board"):
  returnval = get_motherless_boards_links(httpurl, httpheaders, httpcookie, httplibuse, False, getlinks, motherless_serv);
 if(get_motherless_link_type(httpurl)=="member"):
  returnval = get_motherless_search_members(httpurl, httpheaders, httpcookie, httplibuse, page, getlinks);
 if(get_motherless_link_type(httpurl)=="girls"):
  returnval = get_motherless_girls(httpheaders, httpcookie, httplibuse, getlinks);
 if(get_motherless_link_type(httpurl)=="download"):
  returnval = get_motherless_links_from_url(httpurl, httpheaders, httpcookie, httplibuse);
 return returnval;

def view_motherless_links(httpurl, httpheaders, httpcookie, httplibuse="urllib", viewerpro="mpv", prearg=[], proarg=[]):
 httpurl = fix_motherless_url(httpurl);
 commandlist = [viewerpro] + prearg;
 commandlist = commandlist + [get_motherless_links(httpurl, httpheaders, httpcookie, httplibuse)['url']];
 commandlist = commandlist + proarg;
 mpvplaylistp = subprocess.Popen(commandlist, stdout=subprocess.PIPE, stderr=subprocess.PIPE);
 mpvplayout, mpvplayerr = mpvplaylistp.communicate();
 return True;

def download_motherless_links(httpurl, httpheaders, httpcookie, httplibuse="urllib", sleep=-1, buffersize=defbuffersizedub, outfile="-", outpath=os.getcwd(), usetitlename=False):
 global geturls_download_sleep;
 httpurl = fix_motherless_url(httpurl);
 if(sleep<0):
  sleep = geturls_download_sleep;
 mlessurl = get_motherless_links(httpurl, httpheaders, httpcookie, httplibuse);
 outputname = mlessurl['fullfilename'];
 outpath = outpath.rstrip(os.path.sep);
 if(usetitlename==True):
  outputname = mlessurl['title'];
 if(usetitlename=="-" and outfile=="-"):
  outputname = "-";
 if(usetitlename=="-" and not outfile=="-"):
  outputname = outfile;
 returnval = download_from_url_to_file(mlessurl['url'], httpheaders, httpcookie, httplibuse, outputname, outpath, buffersize, sleep);
 return returnval;

def download_motherless_links_by_type(httpurl, httpheaders, httpcookie, httplibuse="urllib", sleep=-1, buffersize=defbuffersizedub, outfile="-", outpath=os.getcwd(), usetitlename=False, page=1, getlinks=[0, -1], motherless_serv=None):
 global geturls_download_sleep;
 httpurl = fix_motherless_url(httpurl);
 if(sleep<0):
  sleep = geturls_download_sleep;
 mlessurl = get_motherless_link_by_type(httpurl, httpheaders, httpcookie, httplibuse, page, getlinks, motherless_serv);
 if(mlessurl['urltype']=="download"):
  outputname = mlessurl['fullfilename'];
  outpathname = outpath.rstrip(os.path.sep);
  if(usetitlename==True):
   outputname = mlessurl['title'];
  if(usetitlename=="-" and outfile[mli]=="-"):
   outputname = "-";
  if(usetitlename=="-" and not outfile[mli]=="-"):
   outputname = outfile;
  returnval = download_from_url_to_file(mlessurl['url'], httpheaders, httpcookie, httplibuse, outputname, outpathname, buffersize, sleep);
 if(not mlessurl['urltype']=="download"):
  returnval = mlessurl;
 return returnval;

def download_motherless_galleries_links(httpurl, httpheaders, httpcookie, httplibuse="urllib", sleep=-1, buffersize=defbuffersizedub, outfile="-", outpath=os.getcwd(), usetitlename=False, page=1, getlinks=[0, -1], motherless_serv=None):
 global geturls_download_sleep;
 httpurl = fix_motherless_url(httpurl);
 if(sleep<0):
  sleep = geturls_download_sleep;
 mlessgalleries = get_motherless_galleries_links(httpurl, httpheaders, httpcookie, httplibuse, page, getlinks, motherless_serv);
 mli = 0;
 mlil = mlessgalleries['numoflinks'];
 returnval = {'pages': mlessgalleries['pages']};
 returnval.update({'numoflists': mlessgalleries['numoflinks']});
 returnval.update({'curpage': mlessgalleries['curpage']});
 returnval.update({'numoflinks': mlessgalleries['numoflinks']});
 returnval.update({'numofalllinks': mlessgalleries['numofalllinks']});
 returnval.update({'orginurl': httpurl});
 returnval.update({'orginurltype': get_motherless_link_type(httpurl)});
 while(mli<mlil):
  mlesslink = get_motherless_links(mlessgalleries[mli]['url'], httpheaders, httpcookie, httplibuse);
  outputname = mlesslink['fullfilename'];
  outpath = outpath.rstrip(os.path.sep);
  if(usetitlename==True):
   outputname = mlesslink['title'];
  if(usetitlename=="-" and outfile=="-"):
   outputname = "-";
  if(usetitlename=="-" and not outfile=="-"):
   outputname = outfile;
  returnval.update({mli: {'download': download_from_url_to_file(mlesslink['url'], httpheaders, httpcookie, httplibuse, outputname, outpath, buffersize, sleep), 'linkinfo': mlesslink, 'outputfile': outputname} });
  mli = mli + 1;
 return returnval;

def download_motherless_boards_links(httpurl, httpheaders, httpcookie, httplibuse="urllib", sleep=-1, buffersize=defbuffersizedub, outfile="-", outpath=os.getcwd(), usetitlename=False, getlinks=[0, -1], motherless_serv=None):
 global geturls_download_sleep;
 httpurl = fix_motherless_url(httpurl);
 if(sleep<0):
  sleep = geturls_download_sleep;
 mlessgalleries = get_motherless_boards_links(httpurl, httpheaders, httpcookie, httplibuse, False, getlinks, motherless_serv);
 mli = 0;
 mlil = mlessgalleries['numoflinks'];
 returnval = {'numoflists': mlessgalleries['numoflinks']};
 returnval.update({'numofalllinks': mlessgalleries['numofalllinks']});
 returnval.update({'orginurl': httpurl});
 returnval.update({'orginurltype': get_motherless_link_type(httpurl)});
 while(mli<mlil):
  mlesslink = get_motherless_links(mlessgalleries[mli]['url'], httpheaders, httpcookie, httplibuse);
  outputname = mlesslink['fullfilename'];
  outpath = outpath.rstrip(os.path.sep);
  if(usetitlename==True):
   outputname = mlesslink['title'];
  if(usetitlename=="-" and outfile=="-"):
   outputname = "-";
  if(usetitlename=="-" and not outfile=="-"):
   outputname = outfile;
  returnval.update({mli: {'download': download_from_url_to_file(mlesslink['url'], httpheaders, httpcookie, httplibuse, outputname, outpath, buffersize, sleep), 'linkinfo': mlesslink, 'outputfile': outputname} });
  mli = mli + 1;
 return returnval;
