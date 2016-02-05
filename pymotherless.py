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

    $FileInfo: pymotherless.py - Last Update: 02/05/2016 Ver. 0.3.6 RC 3 - Author: cooldude2k $
'''

from __future__ import division, absolute_import, print_function;
import re, os, sys, urllib, gzip, time, datetime, argparse, cgi, subprocess, imp;
haverequests = False;
try:
 imp.find_module('requests');
 haverequests = True;
 import requests;
except ImportError:
 haverequests = False;
havehttplibtwo = False;
try:
 imp.find_module('httplib2');
 havehttplibtwo = True;
 import httplib2;
except ImportError:
 havehttplibtwo = False;
if(sys.version[0]=="2"):
 try:
  from cStringIO import StringIO;
 except ImportError:
  from StringIO import StringIO;
 # From http://python-future.org/compatible_idioms.html
 from urlparse import urlparse;
 from urllib import urlencode;
 from urllib2 import urlopen, Request, HTTPError;
 import urllib2, urlparse, cookielib;
if(sys.version[0]>="3"):
 from io import StringIO, BytesIO;
 # From http://python-future.org/compatible_idioms.html
 from urllib.parse import urlparse, urlencode
 from urllib.request import urlopen, Request
 from urllib.error import HTTPError
 import urllib.request as urllib2;
 import urllib.parse as urlparse;
 import http.cookiejar as cookielib;

__program_name__ = "PyMotherless";
__version_info__ = (0, 3, 6, "RC 1", 3);
__version_date_info__ = (2016, 2, 5, "RC 1", 3);
__version_date__ = str(__version_date_info__[0])+"."+str(__version_date_info__[1]).zfill(2)+"."+str(__version_date_info__[2]).zfill(2);
if(__version_info__[4]!=None):
 __version_date_plusrc__ = __version_date__+"-"+str(__version_date_info__[4]);
if(__version_info__[4]==None):
 __version_date_plusrc__ = __version_date__;
if(__version_info__[3]!=None):
 __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2])+" "+str(__version_info__[3]);
if(__version_info__[3]==None):
 __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2]);

geturls_cj = cookielib.CookieJar();
geturls_ua_firefox_windows7 = "Mozilla/5.0 (Windows NT 6.1; rv:43.0) Gecko/20100101 Firefox/43.0";
geturls_ua_chrome_windows7 = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36";
geturls_ua_internet_explorer_windows7 = "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko";
geturls_ua = geturls_ua_firefox_windows7;
geturls_headers_list = [("Referer", "http://motherless.com/"), ("User-Agent", geturls_ua), ("Accept-Encoding", "gzip, deflate"), ("Accept-Language", "en-US,en;q=0.8,en-CA,en-GB;q=0.6"), ("Accept-Charset", "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7"), ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"), ("Connection", "close")];
geturls_headers_dict = {'Referer': "http://motherless.com/", 'User-Agent': geturls_ua, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"};
geturls_headers = geturls_headers_dict;
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

def make_http_headers_from_dict(headers={'Referer': "http://motherless.com/", 'User-Agent': geturls_ua, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"}):
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

def make_http_headers_from_list(headers=[("Referer", "http://motherless.com/"), ("User-Agent", geturls_ua), ("Accept-Encoding", "gzip, deflate"), ("Accept-Language", "en-US,en;q=0.8,en-CA,en-GB;q=0.6"), ("Accept-Charset", "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7"), ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"), ("Connection", "close")]):
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

def download_from_url(httpurl, httpheaders, httpcookie, httplibuse="urllib", sleep=-1):
 global geturls_download_sleep, haverequests, havehttplibtwo;
 if(sleep<0):
  sleep = geturls_download_sleep;
 if(httplibuse=="urllib1" or httplibuse=="urllib2"):
  httplibuse = "urllib";
 if(httplibuse=="httplib1" or httplibuse=="httplib2"):
  httplibuse = "httplib";
 if(haverequests==False and httplibuse=="requests"):
  httplibuse = "urllib";
 if(havehttplibtwo==False and httplibuse=="httplib"):
  httplibuse = "urllib";
 if(httplibuse=="urllib"):
  returnval = download_from_url_with_urllib(httpurl, httpheaders, httpcookie, sleep);
 elif(httplibuse=="httplib"):
  returnval = download_from_url_with_httplib(httpurl, httpheaders, httpcookie, sleep);
 elif(httplibuse=="requests"):
  returnval = download_from_url_with_requests(httpurl, httpheaders, httpcookie, sleep);
 else:
  returnval = False;
 return returnval;

def download_from_url_file(httpurl, httpheaders, httpcookie, httplibuse="urllib", sleep=-1):
 global geturls_download_sleep, haverequests, havehttplibtwo;
 if(sleep<0):
  sleep = geturls_download_sleep;
 if(httplibuse=="urllib1" or httplibuse=="urllib2"):
  httplibuse = "urllib";
 if(httplibuse=="httplib1" or httplibuse=="httplib2"):
  httplibuse = "httplib";
 if(haverequests==False and httplibuse=="requests"):
  httplibuse = "urllib";
 if(havehttplibtwo==False and httplibuse=="httplib"):
  httplibuse = "urllib";
 if(httplibuse=="urllib"):
  returnval = download_from_url_file_with_urllib(httpurl, httpheaders, httpcookie, sleep);
 elif(httplibuse=="httplib"):
  returnval = download_from_url_file_with_requests(httpurl, httpheaders, httpcookie, sleep);
 elif(httplibuse=="requests"):
  returnval = download_from_url_file_with_requests(httpurl, httpheaders, httpcookie, sleep);
 else:
  returnval = False;
 return returnval;

def download_from_url_to_file(httpurl, httpheaders, httpcookie, httplibuse="urllib", outfile="-", outpath=os.getcwd(), sleep=-1):
 global geturls_download_sleep, haverequests, havehttplibtwo;
 if(sleep<0):
  sleep = geturls_download_sleep;
 if(httplibuse=="urllib1" or httplibuse=="urllib2"):
  httplibuse = "urllib";
 if(httplibuse=="httplib1" or httplibuse=="httplib2"):
  httplibuse = "httplib";
 if(haverequests==False and httplibuse=="requests"):
  httplibuse = "urllib";
 if(havehttplibtwo==False and httplibuse=="httplib"):
  httplibuse = "urllib";
 if(httplibuse=="urllib"):
  returnval = download_from_url_to_file_with_urllib(httpurl, httpheaders, httpcookie, outfile, outpath, sleep);
 elif(httplibuse=="httplib"):
  returnval = download_from_url_to_file_with_requests(httpurl, httpheaders, httpcookie, outfile, outpath, sleep);
 elif(httplibuse=="requests"):
  returnval = download_from_url_to_file_with_requests(httpurl, httpheaders, httpcookie, outfile, outpath, sleep);
 else:
  returnval = False;
 return returnval;

def download_from_url_with_urllib(httpurl, httpheaders, httpcookie, sleep=-1):
 global geturls_download_sleep;
 if(sleep<0):
  sleep = geturls_download_sleep;
 geturls_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(httpcookie));
 if isinstance(httpheaders, dict):
  httpheaders = make_http_headers_from_dict(httpheaders);
 geturls_opener.addheaders = httpheaders;
 time.sleep(sleep);
 geturls_text = geturls_opener.open(httpurl);
 if(geturls_text.info().get("Content-Encoding")=="gzip" or geturls_text.info().get("Content-Encoding")=="deflate"):
  if(sys.version[0]=="2"):
   strbuf = StringIO(geturls_text.read());
  if(sys.version[0]>="3"):
   strbuf = BytesIO(geturls_text.read());
  gzstrbuf = gzip.GzipFile(fileobj=strbuf);
  if(sys.version[0]=="2"):
   returnval = gzstrbuf.read()[:];
  if(sys.version[0]>="3"):
   returnval = gzstrbuf.read()[:].decode('ascii', 'replace');
 if(geturls_text.info().get("Content-Encoding")!="gzip" and geturls_text.info().get("Content-Encoding")!="deflate"):
  returnval = geturls_text.read()[:];
 return returnval;

def download_from_url_file_with_urllib(httpurl, httpheaders, httpcookie, sleep=-1):
 global geturls_download_sleep;
 if(sleep<0):
  sleep = geturls_download_sleep;
 geturls_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(httpcookie));
 if isinstance(httpheaders, dict):
  httpheaders = make_http_headers_from_dict(httpheaders);
 geturls_opener.addheaders = httpheaders;
 time.sleep(sleep);
 geturls_text = geturls_opener.open(httpurl);
 if(geturls_text.info().get("Content-Encoding")=="gzip" or geturls_text.info().get("Content-Encoding")=="deflate"):
  if(sys.version[0]=="2"):
   strbuf = StringIO(geturls_text.read());
  if(sys.version[0]>="3"):
   strbuf = BytesIO(geturls_text.read());
  gzstrbuf = gzip.GzipFile(fileobj=strbuf);
  returnval = gzstrbuf.read()[:];
 if(geturls_text.info().get("Content-Encoding")!="gzip" and geturls_text.info().get("Content-Encoding")!="deflate"):
  returnval = geturls_text.read()[:];
 return returnval;

def download_from_url_to_file_with_urllib(httpurl, httpheaders, httpcookie, outfile="-", outpath=os.getcwd(), sleep=-1):
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
  with open(filepath, 'wb+') as f:
   f.write(download_from_url_file_with_urllib(httpurl, httpheaders, httpcookie, sleep));
  f.closed;
  returnval = True;
 if(outfile=="-" and sys.version[0]=="2"):
  f = StringIO();
  f.write(download_from_url_file_with_urllib(httpurl, httpheaders, httpcookie, sleep));
  returnval = f.getvalue();
  f.closed;
 if(outfile=="-" and sys.version[0]>="3"):
  f = BytesIO();
  f.write(download_from_url_file_with_urllib(httpurl, httpheaders, httpcookie, sleep));
  returnval = f.getvalue();
  f.closed;
 return returnval;

if(haverequests==True):
 def download_from_url_with_requests(httpurl, httpheaders, httpcookie, sleep=-1):
  global geturls_download_sleep;
  if(sleep<0):
   sleep = geturls_download_sleep;
  if isinstance(httpheaders, list):
   httpheaders = make_http_headers_from_list(httpheaders);
  time.sleep(sleep);
  geturls_text = requests.get(httpurl, headers=httpheaders);
  if(geturls_text.headers['Content-Type']=="gzip" or geturls_text.headers['Content-Type']=="deflate"):
   if(sys.version[0]=="2"):
    strbuf = StringIO(geturls_text.content);
   if(sys.version[0]>="3"):
    strbuf = BytesIO(geturls_text.content);
   gzstrbuf = gzip.GzipFile(fileobj=strbuf);
   if(sys.version[0]=="2"):
    returnval = gzstrbuf.content[:];
   if(sys.version[0]>="3"):
    returnval = gzstrbuf.content[:].decode('ascii', 'replace');
  if(geturls_text.headers['Content-Type']!="gzip" and geturls_text.headers['Content-Type']!="deflate"):
   returnval = geturls_text.content[:];
  return returnval;

if(havehttplibtwo==False):
 def download_from_url_with_requests(httpurl, httpheaders, httpcookie, sleep=-1):
  returnval = download_from_url_with_urllib(httpurl, httpheaders, httpcookie, sleep)
  return returnval;

if(haverequests==True):
 def download_from_url_file_with_requests(httpurl, httpheaders, httpcookie, sleep=-1):
  global geturls_download_sleep;
  if(sleep<0):
   sleep = geturls_download_sleep;
  if isinstance(httpheaders, list):
   httpheaders = make_http_headers_from_list(httpheaders);
  time.sleep(sleep);
  geturls_text = requests.get(httpurl, headers=httpheaders);
  if(geturls_text.headers['Content-Type']=="gzip" or geturls_text.headers['Content-Type']=="deflate"):
   if(sys.version[0]=="2"):
    strbuf = StringIO(geturls_text.content);
   if(sys.version[0]>="3"):
    strbuf = BytesIO(geturls_text.content);
   gzstrbuf = gzip.GzipFile(fileobj=strbuf);
   returnval = gzstrbuf.content[:];
  if(geturls_text.headers['Content-Type']!="gzip" and geturls_text.headers['Content-Type']!="deflate"):
   returnval = geturls_text.content[:];
  return returnval;

if(havehttplibtwo==False):
 def download_from_url_file_with_requests(httpurl, httpheaders, httpcookie, sleep=-1):
  returnval = download_from_url_file_with_urllib(httpurl, httpheaders, httpcookie, sleep)
  return returnval;

if(haverequests==True):
 def download_from_url_to_file_with_requests(httpurl, httpheaders, httpcookie, outfile="-", outpath=os.getcwd(), sleep=-1):
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
   with open(filepath, 'wb+') as f:
    f.write(download_from_url_file_with_requests(httpurl, httpheaders, httpcookie, sleep));
   f.closed;
   returnval = True;
  if(outfile=="-" and sys.version[0]=="2"):
   f = StringIO();
   f.write(download_from_url_file_with_requests(httpurl, httpheaders, httpcookie, sleep));
   returnval = f.getvalue();
   f.closed;
  if(outfile=="-" and sys.version[0]>="3"):
   f = BytesIO();
   f.write(download_from_url_file_with_requests(httpurl, httpheaders, httpcookie, sleep));
   returnval = f.getvalue();
   f.closed;
  return returnval;

if(havehttplibtwo==False):
 def download_from_url_to_file_with_requests(httpurl, httpheaders, httpcookie, outfile="-", outpath=os.getcwd(), sleep=-1):
  returnval = download_from_url_to_file_with_urllib(httpurl, httpheaders, httpcookie, outfile, outpath, sleep)
  return returnval;

if(havehttplibtwo==True):
 def download_from_url_with_httplib(httpurl, httpheaders, httpcookie, sleep=-1):
  global geturls_download_sleep;
  if(sleep<0):
   sleep = geturls_download_sleep;
  if isinstance(httpheaders, list):
   httpheaders = make_http_headers_from_list(httpheaders);
  time.sleep(sleep);
  httpreq = httplib2.Http();
  geturls_text = httpreq.request(httpurl, "GET", headers=httpheaders);
  if('Content-Type' not in geturls_text[0]):
   geturls_text[0].update({'Content-Type': "none"});
  if(geturls_text[0]['Content-Type']=="gzip" or geturls_text[0]['Content-Type']=="deflate"):
   if(sys.version[0]=="2"):
    strbuf = StringIO(geturls_text[1]);
   if(sys.version[0]>="3"):
    strbuf = BytesIO(geturls_text[1]);
   gzstrbuf = gzip.GzipFile(fileobj=strbuf);
   if(sys.version[0]=="2"):
    returnval = gzstrbuf.content[:];
   if(sys.version[0]>="3"):
    returnval = gzstrbuf.content[:].decode('ascii', 'replace');
  if(geturls_text[0]['Content-Type']!="gzip" and geturls_text[0]['Content-Type']!="deflate"):
   returnval = geturls_text[1][:];
  return returnval;

if(havehttplibtwo==False):
 def download_from_url_with_httplib(httpurl, httpheaders, httpcookie, sleep=-1):
  returnval = download_from_url_with_urllib(httpurl, httpheaders, httpcookie, sleep)
  return returnval;

if(havehttplibtwo==True):
 def download_from_url_file_with_httplib(httpurl, httpheaders, httpcookie, sleep=-1):
  global geturls_download_sleep;
  if(sleep<0):
   sleep = geturls_download_sleep;
  if isinstance(httpheaders, list):
   httpheaders = make_http_headers_from_list(httpheaders);
  time.sleep(sleep);
  httpreq = httplib2.Http();
  geturls_text = httpreq.request(httpurl, "GET", headers=httpheaders);
  if('Content-Type' not in geturls_text[0]):
   geturls_text[0].update({'Content-Type': "none"});
  if(geturls_text[0]['Content-Type']=="gzip" or geturls_text[0]['Content-Type']=="deflate"):
   if(sys.version[0]=="2"):
    strbuf = StringIO(geturls_text[1]);
   if(sys.version[0]>="3"):
    strbuf = BytesIO(geturls_text[1]);
   gzstrbuf = gzip.GzipFile(fileobj=strbuf);
   returnval = gzstrbuf.content[:];
  if(geturls_text[0]['Content-Type']!="gzip" and geturls_text[0]['Content-Type']!="deflate"):
   returnval = geturls_text[1][:];
  return returnval;

if(havehttplibtwo==False):
 def download_from_url_file_with_httplib(httpurl, httpheaders, httpcookie, sleep=-1):
  returnval = download_from_url_file_with_urllib(httpurl, httpheaders, httpcookie, sleep)
  return returnval;

if(havehttplibtwo==True):
 def download_from_url_to_file_with_httplib(httpurl, httpheaders, httpcookie, outfile="-", outpath=os.getcwd(), sleep=-1):
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
   with open(filepath, 'wb+') as f:
    f.write(download_from_url_file_with_httplib(httpurl, httpheaders, httpcookie, sleep));
   f.closed;
   returnval = True;
  if(outfile=="-" and sys.version[0]=="2"):
   f = StringIO();
   f.write(download_from_url_file_with_httplib(httpurl, httpheaders, httpcookie, sleep));
   returnval = f.getvalue();
   f.closed;
  if(outfile=="-" and sys.version[0]>="3"):
   f = BytesIO();
   f.write(download_from_url_file_with_httplib(httpurl, httpheaders, httpcookie, sleep));
   returnval = f.getvalue();
   f.closed;
  return returnval;

if(havehttplibtwo==False):
 def download_from_url_to_file_with_httplib(httpurl, httpheaders, httpcookie, outfile="-", outpath=os.getcwd(), sleep=-1):
  returnval = download_from_url_to_file_with_urllib(httpurl, httpheaders, httpcookie, outfile, outpath, sleep)
  return returnval;

def get_motherless_get_number_pages(httpurl, httpheaders, httpcookie, httplibuse="urllib"):
 mrtext = download_from_url(httpurl, httpheaders, httpcookie, httplibuse);
 mregex_getpagenum = re.escape("page=")+"([0-9]+)"+re.escape("\" class=\"pop\" rel=\"")+"([0-9]+)"+re.escape("\">")+"([0-9]+)"+re.escape("</a>");
 mlesspagenum = re.findall(mregex_getpagenum, mrtext);
 try:
  returnval = mlesspagenum[-1][0];
 except:
  returnval = 1;
 return returnval;

def get_motherless_get_link_type(httpurl):
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
  returnval = "file";
 if(mlessvidid[1]=="random" and len(mlessvidid)==3 and (mlessvidid[2]=="video" or mlessvidid[2]=="image")):
  returnval = "file";
 if(re.match("^V", mlessvidid[1]) and len(mlessvidid)==2):
  returnval = "board";
 if(re.match("^H", mlessvidid[1]) and len(mlessvidid)==2):
  returnval = "gallery";
 if(re.match("^G", mlessvidid[1]) and len(mlessvidid)==2):
  returnval = "gallery";
 if(re.match("^G", mlessvidid[1]) and len(mlessvidid)==3):
  returnval = "file";
 if(re.match("^g", mlessvidid[1]) and len(mlessvidid)==4 and re.match("^([0-9A-F]+)$", mlessvidid[3])):
  returnval = "file";
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
 if(mlessvidid_parts.netloc=="cdn.images.motherlessmedia.com" or mlessvidid_parts.netloc=="cdn.videos.motherlessmedia.com" or mlessvidid_parts.netloc=="cdn.thumbs.motherlessmedia.com"):
  returnval = "download";
 if(returnval==False and len(mlessvidid)==2 and re.match("^([0-9A-F]+)$", mlessvidid[1])):
  returnval = "file";
 return returnval;

def get_motherless_links(httpurl, httpheaders, httpcookie, httplibuse="urllib"):
 mrtext = download_from_url(httpurl, httpheaders, httpcookie, httplibuse);
 mregex_gettitle = re.escape("<title>")+"(.*)"+re.escape(" - MOTHERLESS.COM</title>");
 mlesstitle = re.findall(mregex_gettitle, mrtext);
 mregex_geturlone = re.escape("__fileurl = 'http://cdn.")+"(images|videos)"+re.escape(".motherlessmedia.com/")+"(images|videos)"+re.escape("/")+"([\w\/\?\&\=\.\-]+)"+re.escape("';");
 mlesslinkone = re.findall(mregex_geturlone, mrtext);
 mregex_geturltwo = re.escape("<meta property=\"og:image\" content=\"http://cdn.")+"(images|thumbs)"+re.escape(".motherlessmedia.com/")+"(images|thumbs)"+re.escape("/")+"([\w\/\?\&\=\.\-]+)"+re.escape("\">");
 mlesslinktwo = re.findall(mregex_geturltwo, mrtext);
 filenameext = os.path.basename(urlparse.urljoin("http://cdn."+mlesslinkone[0][0]+".motherlessmedia.com/"+mlesslinkone[0][1]+"/"+mlesslinkone[0][2], urlparse.urlparse("http://cdn."+mlesslinkone[0][0]+".motherlessmedia.com/"+mlesslinkone[0][1]+"/"+mlesslinkone[0][2]).path));
 filename, fileextension = os.path.splitext(filenameext);
 thumbfilenameext = os.path.basename(urlparse.urljoin("http://cdn.images.motherlessmedia.com/"+mlesslinktwo[0][1]+"/"+mlesslinktwo[0][2], urlparse.urlparse("http://cdn.images.motherlessmedia.com/"+mlesslinktwo[0][1]+"/"+mlesslinktwo[0][2]).path));
 thumbfilename, thumbfileextension = os.path.splitext(thumbfilenameext);
 mregex_getuname = re.escape("<tr rel=\"")+"([\w\/\?\&\=\.\-]+)"+re.escape("\"");
 mlessuname = re.findall(mregex_getuname, mrtext);
 mlessuname = mlessuname[0];
 mregex_geturlname = re.escape("<a href=\"/m/")+"([\w\/\?\&\=\.\-]+)"+re.escape("\" target=\"_blank\">\n            <img");
 mlessurlname = re.findall(mregex_geturlname, mrtext);
 mlessurlname = mlessurlname[0];
 mregex_getavatar = re.escape("<img\n    src=\"")+"(.*)"+re.escape("\"\n    class=\"avatar avatar-small\"");
 mlessavatar = re.findall(mregex_getavatar, mrtext);
 mlessavatar = mlessavatar[0];
 avatarfilenameext = os.path.basename(urlparse.urljoin(mlessavatar, urlparse.urlparse(mlessavatar).path));
 avatarfilename, avatarfileextension = os.path.splitext(avatarfilenameext);
 if(mlesslinkone[0][1]=="images"):
  thumbnailaltpart = thumbfilename+"-zoom"+thumbfileextension;
  thumbnailalt = "http://cdn.thumbs.motherlessmedia.com/thumbs/"+thumbnailaltpart;
  thumbnailaltfilenameext = os.path.basename(urlparse.urljoin(thumbnailalt, urlparse.urlparse(thumbnailalt).path));
  thumbnailaltfilename, thumbnailaltfileextension = os.path.splitext(thumbnailaltfilenameext);
 if(mlesslinkone[0][1]=="videos"):
  thumbnailaltpart = thumbfilename+"-small"+thumbfileextension;
  thumbnailalt = "http://cdn.thumbs.motherlessmedia.com/thumbs/"+thumbnailaltpart;
  thumbnailaltfilenameext = os.path.basename(urlparse.urljoin(thumbnailalt, urlparse.urlparse(thumbnailalt).path));
  thumbnailaltfilename, thumbnailaltfileextension = os.path.splitext(thumbnailaltfilenameext);
 returnval = False;
 mlessurltype = get_motherless_get_link_type("http://cdn."+mlesslinkone[0][0]+".motherlessmedia.com/"+mlesslinkone[0][1]+"/"+mlesslinkone[0][2]);
 if(mlesslinkone[0][1]=="images"):
  returnval = {'type': mlesslinkone[0][1], 'urltype': mlessurltype, 'url': "http://cdn."+mlesslinkone[0][0]+".motherlessmedia.com/"+mlesslinkone[0][1]+"/"+mlesslinkone[0][2], 'orginurl': httpurl, 'orginurltype': get_motherless_get_link_type(httpurl), 'thumbnail': "http://cdn.thumbs.motherlessmedia.com/thumbs/"+mlesslinktwo[0][2], 'thumbnailalt': thumbnailalt+"?from_helper", 'title': mlesstitle[0], 'fullfilename': filenameext, 'filename': filename, 'extension': fileextension, 'thumbfullfilename': thumbfilenameext, 'thumbfilename': thumbfilename, 'thumbextension': thumbfileextension, 'thumbnailaltfullfilename': thumbnailaltpart, 'thumbnailaltfilename': thumbnailaltfilename, 'thumbnailaltextension': thumbnailaltfileextension, 'username': mlessuname, 'avatarurl': mlessavatar, 'avatarfullfilename': avatarfilenameext, 'avatarfilename': avatarfilename, 'avatarextension': avatarfileextension};
 if(mlesslinkone[0][1]=="videos"):
  returnval = {'type': mlesslinkone[0][1], 'url': "http://cdn."+mlesslinkone[0][0]+".motherlessmedia.com/"+mlesslinkone[0][1]+"/"+mlesslinkone[0][2], 'orginurl': httpurl, 'orginurltype': get_motherless_get_link_type(httpurl), 'thumbnail': "http://cdn.thumbs.motherlessmedia.com/"+mlesslinktwo[0][1]+"/"+mlesslinktwo[0][2], 'thumbnailalt': thumbnailalt+"?from_helper", 'title': mlesstitle[0], 'fullfilename': filenameext, 'filename': filename, 'extension': fileextension, 'thumbfullfilename': thumbfilenameext, 'thumbfilename': thumbfilename, 'thumbextension': thumbfileextension, 'thumbnailaltfullfilename': thumbnailaltpart, 'thumbnailaltfilename': thumbnailaltfilename, 'thumbnailaltextension': thumbnailaltfileextension, 'username': mlessuname, 'avatarurl': mlessavatar, 'avatarfullfilename': avatarfilenameext, 'avatarfilename': avatarfilename, 'avatarextension': avatarfileextension};
 return returnval;

def get_motherless_external_links(httpurl, httpheaders, httpcookie, httplibuse="urllib"):
 mrtext = download_from_url(httpurl, httpheaders, httpcookie, httplibuse);
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
  returnvalone.update({'orginurltype': get_motherless_get_link_type(httpurl)});
  mlessrooturltype = get_motherless_get_link_type(httpurl);
  returnvalone.update({'urltype': mlessrooturltype});
  while(mli<mlil):
   mlessurltype = get_motherless_get_link_type(mlesslinkinternal[mli]);
   returnvalone.update({mli: {'urltype': mlessurltype, 'url': mlesslinkinternal[mli]} });
   mli = mli + 1;
 returnvaltwo = None;
 if(len(mlesslinkexternal)>1):
  mli = 0;
  mlil = len(mlesslinkexternal);
  returnvaltwo = {'numoflinks': mlil};
  returnvaltwo.update({'numofalllinks': len(mlesslinkexternal)});
  returnvaltwo.update({'orginurl': httpurl});
  returnvaltwo.update({'orginurltype': get_motherless_get_link_type(httpurl)});
  mlessrooturltype = get_motherless_get_link_type(httpurl);
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

def get_motherless_galleries_links(httpurl, httpheaders, httpcookie, httplibuse="urllib", page=1, getlinks=[0, -1]):
 mrtext = download_from_url(httpurl, httpheaders, httpcookie, httplibuse);
 mregex_getpagenum = re.escape("page=")+"([0-9]+)"+re.escape("\" class=\"pop\" rel=\"")+"([0-9]+)"+re.escape("\">")+"([0-9]+)"+re.escape("</a>");
 mlesspagenum = re.findall(mregex_getpagenum, mrtext);
 try:
  lastpage = mlesspagenum[-1][0];
 except:
  lastpage = 1;
 if(page>lastpage):
  page = lastpage;
 httpurl = add_url_param(httpurl, page=str(page));
 mrtext = download_from_url(httpurl, httpheaders, httpcookie, httplibuse);
 mregex_geturlone = re.escape("<a href=\"/")+"([\w\/]+)"+re.escape("\" class=\"img-container\" target=\"_self\">");
 mrtext_tmp = re.sub(re.escape("http://motherless.com"), "", mrtext);
 mrtext_tmp = re.sub(re.escape("http://www.motherless.com"), "", mrtext_tmp);
 mrtext_tmp = re.sub(re.escape("http://motherless.com"), "", mrtext_tmp);
 mrtext_tmp = re.sub(re.escape("http://www.motherless.com"), "", mrtext_tmp);
 mlesslinkone = re.findall(mregex_geturlone, mrtext_tmp);
 mregex_geturltwo = re.escape("<img class=\"static\" src=\"http://cdn.thumbs.motherlessmedia.com/")+"([\w\/\?\&\=\.\-]+)"+re.escape("\" data-strip-src=\"http://cdn.thumbs.motherlessmedia.com/")+"([\w\/\?\&\=\.\-]+)"+re.escape("\" alt=\"")+"(.*)"+re.escape("\" />");
 mlesslinktwo = re.findall(mregex_geturltwo, mrtext);
 mregex_getuserinfo = re.escape("<a class=\"caption left\" href=\"/m/")+"([\w\/\?\&\=\.\-]+)"+re.escape("\">");
 mlessuname = re.findall(mregex_getuserinfo, mrtext);
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
 returnval.update({'orginurltype': get_motherless_get_link_type(httpurl)});
 mlessrooturltype = get_motherless_get_link_type(httpurl);
 returnval.update({'urltype': mlessrooturltype});
 while(mli<mlil):
  stripfilenameext = os.path.basename(urlparse.urljoin("http://cdn.thumbs.motherlessmedia.com/"+mlesslinktwo[mli][1], urlparse.urlparse("http://cdn.thumbs.motherlessmedia.com/"+mlesslinktwo[mli][1]).path));
  stripfilename, stripfileextension = os.path.splitext(stripfilenameext);
  thumbfilenameext = os.path.basename(urlparse.urljoin("http://cdn.thumbs.motherlessmedia.com/"+mlesslinktwo[mli][0], urlparse.urlparse("http://cdn.thumbs.motherlessmedia.com/"+mlesslinktwo[mli][0]).path));
  thumbfilename, thumbfileextension = os.path.splitext(thumbfilenameext);
  mlessurltype = get_motherless_get_link_type("http://motherless.com/"+mlesslinkone[mli]);
  avatarfilenameext = os.path.basename(urlparse.urljoin("http://cdn.avatars.motherlessmedia.com/thumbs/"+mlessuname[mli]+"-avatar.jpg", urlparse.urlparse("http://cdn.avatars.motherlessmedia.com/thumbs/"+mlessuname[mli]+"-avatar.jpg").path));
  avatarfilename, avatarfileextension = os.path.splitext(avatarfilenameext);
  returnval.update({mli: {'urltype': mlessurltype, 'url': "http://motherless.com/"+mlesslinkone[mli], 'thumbnail': "http://cdn.thumbs.motherlessmedia.com/"+mlesslinktwo[mli][0], 'strip': "http://cdn.thumbs.motherlessmedia.com/"+mlesslinktwo[mli][1], 'title': mlesslinktwo[mli][2], 'thumbfullfilename': thumbfilenameext, 'thumbfilename': thumbfilename, 'thumbextension': thumbfileextension, 'stripfullfilename': stripfilenameext, 'stripfilename': stripfilename, 'stripextension': stripfileextension, 'username': mlessuname[mli], 'avatarurl': "http://cdn.avatars.motherlessmedia.com/thumbs/"+mlessuname[mli]+"-avatar.jpg", 'avatarfullfilename': avatarfilenameext, 'avatarfilename': avatarfilename, 'avatarextension': avatarfileextension} });
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
   returnval.update({mli: {'urltype': get_motherless_get_link_type("http://motherless.com/"+get_links['filename']), 'url': "http://motherless.com/"+get_links['filename'], 'thumbnail': get_links['thumbnail'], 'strip': get_links['thumbnailalt'], 'title': get_links['title'], 'thumbfullfilename': get_links['thumbfullfilename'], 'thumbfilename': get_links['thumbfilename'], 'thumbextension': get_links['thumbextension'], 'stripfullfilename': get_links['thumbnailaltfullfilename'], 'stripfilename': get_links['thumbnailaltextension'], 'stripextension': get_links['thumbnailaltfilename'], 'username': get_links['username'], 'avatarurl': get_links['avatarurl'], 'avatarfullfilename': get_links['avatarfullfilename'], 'avatarfilename': get_links['avatarfilename'], 'avatarextension': get_links['avatarextension']} });
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
   returnval.update({mli: {'urltype': get_motherless_get_link_type("http://motherless.com/"+get_links['filename']), 'url': "http://motherless.com/"+get_links['filename'], 'thumbnail': get_links['thumbnail'], 'strip': get_links['thumbnailalt'], 'title': get_links['title'], 'thumbfullfilename': get_links['thumbfullfilename'], 'thumbfilename': get_links['thumbfilename'], 'thumbextension': get_links['thumbextension'], 'stripfullfilename': get_links['thumbnailaltfullfilename'], 'stripfilename': get_links['thumbnailaltextension'], 'stripextension': get_links['thumbnailaltfilename'], 'username': get_links['username'], 'avatarurl': get_links['avatarurl'], 'avatarfullfilename': get_links['avatarfullfilename'], 'avatarfilename': get_links['avatarfilename'], 'avatarextension': get_links['avatarextension']} });
   mli = mli + 1;
 return returnval;

def get_motherless_boards_links(httpurl, httpheaders, httpcookie, httplibuse="urllib", getlinks=[0, -1]):
 mrtext = download_from_url(httpurl, httpheaders, httpcookie, httplibuse);
 mrtext_tmp = re.sub(re.escape("http://motherless.com"), "", mrtext);
 mrtext_tmp = re.sub(re.escape("http://www.motherless.com"), "", mrtext_tmp);
 mrtext_tmp = re.sub(re.escape("http://motherless.com"), "", mrtext_tmp);
 mrtext_tmp = re.sub(re.escape("http://www.motherless.com"), "", mrtext_tmp);
 mregex_geturlone = re.escape("<a href=\"/")+"([\w\/]+)"+re.escape("\" title=\"motherless link\">");
 mlesslinkone = re.findall(mregex_geturlone, mrtext_tmp);
 mregex_geturlname = re.escape("<a href=\"/boards/member/")+"([\w\/\?\&\=\.\-]+)"+re.escape("\" class=\"post-username special-member op-member\" title=\"op\" rel=\"")+"([\w\/\?\&\=\.\-]+)"+re.escape("\">");
 mlessurlname = re.findall(mregex_geturlname, mrtext);
 mlessavaturl = "http://cdn.avatars.motherlessmedia.com/thumbs/"+mlessurlname[0][0]+"-avatar.jpg";
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
 returnval.update({'orginurltype': get_motherless_get_link_type(httpurl)});
 mlessrooturltype = get_motherless_get_link_type(httpurl);
 returnval.update({'urltype': mlessrooturltype});
 returnval.update({'username': mlessurlname[0][0]});
 returnval.update({'avatarurl': mlessavaturl});
 returnval.update({'avatarfullfilename': avatarfilenameext});
 returnval.update({'avatarfilename': avatarfilename});
 returnval.update({'avatarextension': avatarfileextension});
 while(mli<mlil):
  mlessurltype = get_motherless_get_link_type("http://motherless.com/"+mlesslinkone[mli]);
  returnval.update({mli: {'urltype': mlessurltype, 'url': "http://motherless.com/"+mlesslinkone[mli]} });
  mli = mli + 1;
 return returnval;

def get_motherless_search_members(httpurl, httpheaders, httpcookie, httplibuse="urllib", page=1, getlinks=[0, -1]):
 mrtext = download_from_url(httpurl, httpheaders, httpcookie, httplibuse);
 mregex_getpagenum = re.escape("page=")+"([0-9]+)"+re.escape("\" class=\"pop\" rel=\"")+"([0-9]+)"+re.escape("\">")+"([0-9]+)"+re.escape("</a>");
 mlesspagenum = re.findall(mregex_getpagenum, mrtext);
 try:
  lastpage = mlesspagenum[-1][0];
 except:
  lastpage = 1;
 if(page>lastpage):
  page = lastpage;
 httpurl = add_url_param(httpurl, page=str(page));
 mrtext = download_from_url(httpurl, httpheaders, httpcookie, httplibuse);
 mregex_getuname = re.escape("<tr rel=\"")+"([\w\/\?\&\=\.\-]+)"+re.escape("\"");
 mlessuname = re.findall(mregex_getuname, mrtext);
 mregex_geturlname = re.escape("<a href=\"/m/")+"([\w\/\?\&\=\.\-]+)"+re.escape("\" target=\"_blank\">\n            <img");
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
 returnval.update({'orginurltype': get_motherless_get_link_type(httpurl)});
 mlessrooturltype = get_motherless_get_link_type(httpurl);
 returnval.update({'urltype': mlessrooturltype});
 while(mli<mlil):
  avatarfilenameext = os.path.basename(urlparse.urljoin(mlessavatar[mli], urlparse.urlparse(mlessavatar[mli]).path));
  avatarfilename, avatarfileextension = os.path.splitext(avatarfilenameext);
  mlessurltype = get_motherless_get_link_type("http://motherless.com/"+mlessurlname[mli]);
  returnval.update({mli: {'urltype': mlessurltype, 'url': "http://motherless.com/"+mlessurlname[mli], 'username': mlessuname[mli], 'avatarurl': mlessavatar[mli], 'avatarfullfilename': avatarfilenameext, 'avatarfilename': avatarfilename, 'avatarextension': avatarfileextension} });
  mli = mli + 1;
 return returnval;

def get_motherless_girls(httpheaders, httpcookie, httplibuse="urllib", getlinks=[0, -1]):
 mrtext = download_from_url("http://motherless.com/girls", httpheaders, httpcookie, httplibuse);
 mregex_getuname = re.escape("<a href=\"")+'?\'?([^"\'>]*)'+re.escape("\" rev=\"")+"([\w\/\?\&\=\.\-]+)"+re.escape("\" rel=\"")+"(.*)"+re.escape("\">");
 mlessuname = re.findall(mregex_getuname, mrtext);
 mregex_geturlname = re.escape("\n\t\t\t\t\t\t<a href=\"/m/")+"([\w\/\?\&\=\.\-]+)"+re.escape("\" target=\"_blank\">");
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
 returnval.update({'orginurltype': get_motherless_get_link_type("http://motherless.com/girls")});
 mlessrooturltype = get_motherless_get_link_type("http://motherless.com/girls");
 returnval.update({'urltype': mlessrooturltype});
 while(mli<mlil):
  avatarfilenameext = os.path.basename(urlparse.urljoin(mlessuname[mli][0], urlparse.urlparse(mlessuname[mli][0]).path));
  avatarfilename, avatarfileextension = os.path.splitext(avatarfilenameext);
  mlessurltype = get_motherless_get_link_type("http://motherless.com/"+mlessuname[mli][1]);
  returnval.update({mli: {'urltype': mlessurltype, 'url': "http://motherless.com/"+mlessuname[mli][1], 'username': mlessuname[mli][1], 'avatarurl': mlessuname[mli][0], 'avatarfullfilename': avatarfilenameext, 'avatarfilename': avatarfilename, 'avatarextension': avatarfileextension} });
  mli = mli + 1;
 return returnval;

def get_motherless_team(httpheaders, httpcookie, httplibuse="urllib", getlinks=[0, -1]):
 mrtext = download_from_url("http://motherless.com/about", httpheaders, httpcookie, httplibuse);
 mregex_getuname = re.escape("<a href=\"/m/")+"([\w\/\?\&\=\.\-]+)"+re.escape("\"");
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
 returnval.update({'orginurl': "http://motherless.com/girls"});
 returnval.update({'orginurltype': get_motherless_get_link_type("http://motherless.com/girls")});
 mlessrooturltype = get_motherless_get_link_type("http://motherless.com/girls");
 returnval.update({'urltype': mlessrooturltype});
 while(mli<mlil):
  avatarfilenameext = os.path.basename(urlparse.urljoin(mlessavatar[mli][0], urlparse.urlparse(mlessavatar[mli][0]).path));
  avatarfilename, avatarfileextension = os.path.splitext(avatarfilenameext);
  mlessurltype = get_motherless_get_link_type("http://motherless.com/"+mlessuname_odd[mli]);
  returnval.update({mli: {'urltype': mlessurltype, 'url': "http://motherless.com/"+mlessuname_odd[mli], 'username': mlessuname_odd[mli], 'avatarurl': mlessavatar[mli][0], 'avatarfullfilename': avatarfilenameext, 'avatarfilename': avatarfilename, 'avatarextension': avatarfileextension} });
  mli = mli + 1;
 return returnval;

def get_motherless_top_referrers(httpheaders, httpcookie, httplibuse="urllib", getlinks=[0, -1]):
 mrtext = download_from_url("http://motherless.com/referers", httpheaders, httpcookie, httplibuse);
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
 returnval.update({'orginurltype': get_motherless_get_link_type("http://motherless.com/referers")});
 mlessrooturltype = get_motherless_get_link_type("http://motherless.com/referers");
 returnval.update({'urltype': mlessrooturltype});
 while(mli<mlil):
  returnval.update({mli: {'urltype': "referer-links", 'url': mlessurlname[mli][1], 'title': mlessurlname[mli][2]} });
  mli = mli + 1;
 return returnval;

def get_motherless_top_referers(httpheaders, httpcookie, httplibuse="urllib", getlinks=[0, -1]):
 return get_motherless_top_referrers(httpheaders, httpcookie, httplibuse, getlinks);

def get_motherless_sample_links(httpheaders, httpcookie, httplibuse="urllib", numoflinks=10, urltype="video"):
 if(urltype=="video"):
  returnval = {'numoflinks': numoflinks, 'orginurl': "http://motherless.com/videos", 'orginurltype': get_motherless_get_link_type("http://motherless.com/videos"), 'videos': {'recent': get_motherless_galleries_links("http://motherless.com/videos/recent", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'favorited': get_motherless_galleries_links("http://motherless.com/videos/favorited", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'viewed': get_motherless_galleries_links("http://motherless.com/videos/viewed", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'commented': get_motherless_galleries_links("http://motherless.com/videos/commented", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'popular': get_motherless_galleries_links("http://motherless.com/videos/popular", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'live': get_motherless_galleries_links("http://motherless.com/live/videos", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'random': get_motherless_random_links(httpheaders, httpcookie, httplibuse, "video", [0, numoflinks]) } };
 if(urltype=="image"):
  returnval = {'numoflinks': numoflinks, 'orginurl': "http://motherless.com/images", 'orginurltype': get_motherless_get_link_type("http://motherless.com/images"), 'images': {'recent': get_motherless_galleries_links("http://motherless.com/images/recent", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'favorited': get_motherless_galleries_links("http://motherless.com/images/favorited", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'viewed': get_motherless_galleries_links("http://motherless.com/images/viewed", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'commented': get_motherless_galleries_links("http://motherless.com/images/commented", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'popular': get_motherless_galleries_links("http://motherless.com/images/popular", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'live': get_motherless_galleries_links("http://motherless.com/live/images", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'random': get_motherless_random_links(httpheaders, httpcookie, httplibuse, "image", [0, numoflinks]) } };
 if(urltype=="gallery"):
  returnval = {'numoflinks': numoflinks, 'orginurl': "http://motherless.com/galleries", 'orginurltype': get_motherless_get_link_type("http://motherless.com/galleries"), 'galleries': {'updated': get_motherless_galleries_links("http://motherless.com/galleries/updated", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'created': get_motherless_galleries_links("http://motherless.com/galleries/created", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'viewed': get_motherless_galleries_links("http://motherless.com/galleries/viewed", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'favorited': get_motherless_galleries_links("http://motherless.com/galleries/favorited", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'commented': get_motherless_galleries_links("http://motherless.com/galleries/commented", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]) } };
 if(urltype=="all"):
  returnval = {'numoflinks': numoflinks, 'orginurl': "http://motherless.com/", 'orginurltype': get_motherless_get_link_type("http://motherless.com/"), 'videos': {'recent': get_motherless_galleries_links("http://motherless.com/videos/recent", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'favorited': get_motherless_galleries_links("http://motherless.com/videos/favorited", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'viewed': get_motherless_galleries_links("http://motherless.com/videos/viewed", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'commented': get_motherless_galleries_links("http://motherless.com/videos/commented", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'popular': get_motherless_galleries_links("http://motherless.com/videos/popular", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'live': get_motherless_galleries_links("http://motherless.com/live/videos", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'random': get_motherless_random_links(httpheaders, httpcookie, httplibuse, "video", [0, numoflinks]) }, 'images': {'recent': get_motherless_galleries_links("http://motherless.com/images/recent", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'favorited': get_motherless_galleries_links("http://motherless.com/images/favorited", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'viewed': get_motherless_galleries_links("http://motherless.com/images/viewed", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'commented': get_motherless_galleries_links("http://motherless.com/images/commented", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'popular': get_motherless_galleries_links("http://motherless.com/images/popular", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'live': get_motherless_galleries_links("http://motherless.com/live/images", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'random': get_motherless_random_links(httpheaders, httpcookie, httplibuse, "image", [0, numoflinks]) }, 'galleries': {'updated': get_motherless_galleries_links("http://motherless.com/galleries/updated", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'created': get_motherless_galleries_links("http://motherless.com/galleries/created", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'viewed': get_motherless_galleries_links("http://motherless.com/galleries/viewed", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'favorited': get_motherless_galleries_links("http://motherless.com/galleries/favorited", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]), 'commented': get_motherless_galleries_links("http://motherless.com/galleries/commented", httpheaders, httpcookie, httplibuse, 1, [0, numoflinks]) } };
 return returnval;

def get_motherless_get_link_by_type(httpurl, httpheaders, httpcookie, httplibuse="urllib", page=1, getlinks=[0, -1]):
 returnval = False;
 if(get_motherless_get_link_type(httpurl)=="file"):
  returnval = get_motherless_links(httpurl, httpheaders, httpcookie, httplibuse);
 if(get_motherless_get_link_type(httpurl)=="gallery"):
  returnval = get_motherless_galleries_links(httpurl, httpheaders, httpcookie, httplibuse, page);
 if(get_motherless_get_link_type(httpurl)=="sample-videos"):
  returnval = get_motherless_sample_links(httpheaders, httpcookie, httplibuse, 10, "video");
 if(get_motherless_get_link_type(httpurl)=="sample-images"):
  returnval = get_motherless_sample_links(httpheaders, httpcookie, httplibuse, 10, "image");
 if(get_motherless_get_link_type(httpurl)=="sample-galleries"):
  returnval = get_motherless_sample_links(httpheaders, httpcookie, httplibuse, 10, "gallery");
 if(get_motherless_get_link_type(httpurl)=="sample" or get_motherless_get_link_type(httpurl)=="sample-all"):
  returnval = get_motherless_sample_links(httpheaders, httpcookie, httplibuse, 10, "all");
 if(get_motherless_get_link_type(httpurl)=="board"):
  returnval = get_motherless_boards_links(httpurl, httpheaders, httpcookie, httplibuse);
 if(get_motherless_get_link_type(httpurl)=="member"):
  returnval = get_motherless_search_members(httpurl, httpheaders, httpcookie, httplibuse, page);
 if(get_motherless_get_link_type(httpurl)=="girls"):
  returnval = get_motherless_girls(httpheaders, httpcookie, httplibuse);
 if(get_motherless_get_link_type(httpurl)=="download"):
  returnval = httpurl;
 return returnval;

def view_motherless_links(httpurl, httpheaders, httpcookie, httplibuse="urllib", viewerpro="mpv", prearg=[], proarg=[]):
 commandlist = [viewerpro] + prearg;
 commandlist = commandlist + [get_motherless_links(httpurl, httpheaders, httpcookie, httplibuse)['url']];
 commandlist = commandlist + proarg;
 mpvplaylistp = subprocess.Popen(commandlist, stdout=subprocess.PIPE, stderr=subprocess.PIPE);
 mpvplayout, mpvplayerr = mpvplaylistp.communicate();
 return True;

def download_motherless_links(httpurl, httpheaders, httpcookie, httplibuse="urllib", sleep=-1, outfile="-", outpath=os.getcwd(), usetitlename=False):
 global geturls_download_sleep;
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
 returnval = download_from_url_to_file(mlessurl['url'], httpheaders, httpcookie, httplibuse, outputname, outpath, sleep);
 return returnval;

def download_motherless_links_by_type(httpurl, httpheaders, httpcookie, httplibuse="urllib", sleep=-1, outfile="-", outpath=os.getcwd(), usetitlename=False, page=1, getlinks=[0, -1]):
 global geturls_download_sleep;
 if(sleep<0):
  sleep = geturls_download_sleep;
 mlessurl = get_motherless_get_link_by_type(httpurl, httpheaders, httpcookie, httplibuse, page);
 if(mlessurl['urltype']=="download"):
  outputname = mlessurl['fullfilename'];
  outpathname = outpath.rstrip(os.path.sep);
  if(usetitlename==True):
   outputname = mlessurl['title'];
  if(usetitlename=="-" and outfile[mli]=="-"):
   outputname = "-";
  if(usetitlename=="-" and not outfile[mli]=="-"):
   outputname = outfile;
  returnval = download_from_url_to_file(mlessurl['url'], httpheaders, httpcookie, httplibuse, outputname, outpathname, sleep);
 if(not mlessurl['urltype']=="download"):
  returnval = mlessurl;
 return returnval;

def download_motherless_galleries_links(httpurl, httpheaders, httpcookie, httplibuse="urllib", sleep=-1, outfile="-", outpath=os.getcwd(), usetitlename=False, page=1, getlinks=[0, -1]):
 global geturls_download_sleep;
 if(sleep<0):
  sleep = geturls_download_sleep;
 mlessgalleries = get_motherless_galleries_links(httpurl, httpheaders, httpcookie, httplibuse, page, getlinks);
 mli = 0;
 mlil = mlessgalleries['numoflinks'];
 returnval = {'pages': mlessgalleries['pages']};
 returnval.update({'numoflists': mlessgalleries['numoflinks']});
 returnval.update({'curpage': mlessgalleries['curpage']});
 returnval.update({'numoflinks': mlessgalleries['numoflinks']});
 returnval.update({'numofalllinks': mlessgalleries['numofalllinks']});
 returnval.update({'orginurl': httpurl});
 returnval.update({'orginurltype': get_motherless_get_link_type(httpurl)});
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
  returnval.update({mli: {'download': download_from_url_to_file(mlesslink['url'], httpheaders, httpcookie, httplibuse, outputname, outpath, sleep), 'linkinfo': mlesslink, 'outputfile': outputname} });
  mli = mli + 1;
 return returnval;

def download_get_motherless_boards_links(httpurl, httpheaders, httpcookie, httplibuse="urllib", sleep=-1, outfile="-", outpath=os.getcwd(), usetitlename=False, getlinks=[0, -1]):
 global geturls_download_sleep;
 if(sleep<0):
  sleep = geturls_download_sleep;
 mlessgalleries = get_motherless_boards_links(httpurl, httpheaders, httpcookie, httplibuse, getlinks);
 mli = 0;
 mlil = mlessgalleries['numoflinks'];
 returnval = {'numoflists': mlessgalleries['numoflinks']};
 returnval.update({'numofalllinks': mlessgalleries['numofalllinks']});
 returnval.update({'orginurl': httpurl});
 returnval.update({'orginurltype': get_motherless_get_link_type(httpurl)});
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
  returnval.update({mli: {'download': download_from_url_to_file(mlesslink['url'], httpheaders, httpcookie, httplibuse, outputname, outpath, sleep), 'linkinfo': mlesslink, 'outputfile': outputname} });
  mli = mli + 1;
 return returnval;

