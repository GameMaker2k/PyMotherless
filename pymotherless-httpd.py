#!/usr/bin/env python

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2015 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2015 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: httpd.py - Last Update: 1/30/2019 Ver. 0.4.7 RC 4  - Author: cooldude2k $
'''

import tempfile, uuid, re, os, sys, cherrypy, pymotherless, argparse, time, datetime;
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

parser = argparse.ArgumentParser(description="A web server that draws barcodes with PyUPC-EAN powered by CherryPy web server.");
parser.add_argument("--port", "--port-number", default=8080, help="port number to use for server.");
parser.add_argument("--host", "--host-name", default="127.0.0.1", help="host name to use for server.");
parser.add_argument("--verbose", "--verbose-mode", help="show log on terminal screen.", action="store_true");
parser.add_argument("--gzip", "--gzip-mode", help="enable gzip http requests.", action="store_true");
parser.add_argument("--gzipfilter", "--gzipfilter-mode", help="enable gzipfilter mode.", action="store_true");
parser.add_argument("--accesslog", "--accesslog-file", help="location to store access log file.");
parser.add_argument("--errorlog", "--errorlog-file", help="location to store error log file.");
parser.add_argument("--timeout", "--response-timeout", default=6000, help="the number of seconds to allow responses to run.");
parser.add_argument("--environment", "--server-environment", default="production", help="The server.environment entry controls how CherryPy should run.");
getargs = parser.parse_args();
if(getargs.verbose==True):
 log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG);
if(getargs.port is not None):
 port = int(getargs.port);
else:
 port = 8080;
if(getargs.host is not None):
 host = str(getargs.host);
else:
 host = "127.0.0.1";
if(getargs.timeout is not None):
 timeout = int(getargs.timeout);
else:
 timeout = 6000;
if(getargs.accesslog is not None):
 accesslog = str(getargs.accesslog);
else:
 accesslog = "./access.log";
if(getargs.errorlog is not None):
 errorlog = str(getargs.errorlog);
else:
 errorlog = "./errors.log";
if(getargs.environment is not None):
 serv_environ = str(getargs.environment);
else:
 serv_environ = "production";
pro_app_name = "Barcode Generator 2k";
pro_app_subname = "(PyUPC-EAN)";
pro_app_version = pymotherless.__version__;
radsta=0;
radmax=360;
radinc=5;
radout="\n";
while(radsta<=radmax):
 if(radsta==0):
  radout += "<option value=\""+str(radsta)+"\" selected=\"selected\">"+str(radsta)+" &#176;</option>\n";
 if(radsta>0):
  radout += "<option value=\""+str(radsta)+"\">"+str(radsta)+" &#176;</option>\n";
 radsta = radsta + radinc;
ServerSignature = "<address><a href=\"https://github.com/GameMaker2k/PyUPC-EAN\" title=\"PyUPC-EAN barcode generator\">PyUPC-EAN</a>/%s (<a href=\"http://www.cherrypy.org/\" title=\"CherryPy python web server\">CherryPy</a>/%s)</address>" % (pymotherless.__version__, cherrypy.__version__);
IndexHTMLCode = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"en\" xml:lang=\"en\">\n<head>\n<title> "+pro_app_name+" "+pro_app_subname+" </title><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />\n<meta http-equiv=\"Content-Language\" content=\"en\" />\n<meta name=\"generator\" content=\"CherryPy\" />\n<meta name=\"author\" content=\"Game Maker 2k\" />\n<meta name=\"keywords\" content=\"barcode,upc,ean,stf,itf,itf14,upca,upce,ean2,ean5,ean8,ean13,code11,code39,code93,codabar,msi\" />\n<meta name=\"description\" content=\"Barcode Generator with PyUPC-EAN\" /><meta name=\"resource-type\" content=\"document\" />\n<meta name=\"distribution\" content=\"global\" />\n<link rel=\"Generator\" href=\"http://www.cherrypy.org/\" title=\"CherryPy\" />\n</head>\n<body>\n<form name=\"pymotherless\" id=\"pymotherless\" method=\"get\" action=\"/pymotherless/\" onsubmit=\"location.href='/generate/'+pymotherless.bctype.value+'/'+pymotherless.size.value+'/'+pymotherless.rotate.value+'/'+pymotherless.upc.value+'.'+pymotherless.imgtype.value; return false;\">\n<fieldset>\n<legend>Barcode Info: </legend>\n<label style=\"cursor: pointer;\" for=\"upc\">Enter UPC/EAN: </label><br />\n<input type=\"text\" id=\"upc\" name=\"upc\" /><br />\n<label style=\"cursor: pointer;\" for=\"imgtype\">Select a image type: </label><br />\n<select id=\"imgtype\" name=\"imgtype\">\n<option value=\"png\" selected=\"selected\">PNG Image</option>\n<option value=\"gif\">GIF Image</option>\n<option value=\"jpeg\">JPEG Image</option>\n<option value=\"bmp\">BMP Image</option>\n<option value=\"tiff\">TIFF Image</option>\n</select><br />\n<label style=\"cursor: pointer;\" for=\"size\">Select barcode size: </label><br />\n<select id=\"size\" name=\"size\">\n<option value=\"1\" selected=\"selected\">1x</option>\n<option value=\"2\">2x</option>\n<option value=\"3\">3x</option>\n<option value=\"4\">4x</option>\n<option value=\"5\">5x</option>\n<option value=\"6\">6x</option>\n<option value=\"7\">7x</option>\n<option value=\"8\">8x</option>\n<option value=\"9\">9x</option>\n<option value=\"10\">10x</option>\n</select><br />\n<label style=\"cursor: pointer;\" for=\"bctype\">Select barcode type: </label><br />\n<select id=\"bctype\" name=\"bctype\">\n<option value=\"upca\" selected=\"selected\">UPC-A</option>\n<option value=\"upce\">UPC-E</option>\n<option value=\"ean13\">EAN-13</option>\n<option value=\"ean8\">EAN-8</option>\n<option value=\"ean2\">EAN-2</option>\n<option value=\"ean5\">EAN-5</option>\n<option value=\"stf\">STF</option>\n<option value=\"itf\">ITF</option>\n<option value=\"itf14\">ITF-14</option>\n<option value=\"code11\">Code 11</option>\n<option value=\"code39\">Code 39</option>\n<option value=\"code93\">Code 93</option>\n<option value=\"codabar\">Codabar</option>\n<option value=\"msi\">MSI</option>\n</select><br />\n<label style=\"cursor: pointer;\" for=\"rotate\">Select degrees to rotate image by: </label><br />\n<select id=\"rotate\" name=\"rotate\">"+radout+"</select><br />\n<input type=\"submit\" value=\"Generate\" />\n</fieldset>\n</form><br />\n"+ServerSignature+"\n</body>\n</html>";
class GenerateIndexPage(object):
 @cherrypy.expose
 def default(self, *args, **kwargs):
  cherrypy.response.headers['Content-Type'] = 'text/html; charset=UTF-8';
  getpyurlpath = urlparse.urlparse(cherrypy.url()).path;
  getpymotherless = "http://motherless.com"+getpyurlpath;
  pymotherlessinfo = pymotherless.get_motherless_link_type_alt(getpymotherless);
  IndexHTMLCode = getpyurlpath+" - "+pymotherlessinfo['motherlessinfo'];
  if(pymotherlessinfo['motherlessinfo']=="sample" or pymotherlessinfo['motherlessinfo']=="sample-videos"):
   IndexHTMLCode = "";
   getpyurlinfo = pymotherless.get_motherless_sample_links(geturls_headers, geturls_cj, numoflinks=15, urltype="video");
   counti = 0;
   while(counti<15):
    IndexHTMLCode = IndexHTMLCode+" <a href=\""+getpyurlinfo['videos']['recent'][counti]['url'].replace('http://motherless.com', '')+"\"><img src=\""+getpyurlinfo['videos']['recent'][counti]['thumbnail']+"\" alt=\""+getpyurlinfo['videos']['recent'][counti]['title']+"\" title=\""+getpyurlinfo['videos']['recent'][counti]['title']+"\" /></a>\n";
    counti = counti + 1;
   IndexHTMLCode = IndexHTMLCode+"<div><br />&nbsp;<br /></div>\n";
   counti = 0;
   while(counti<15):
    IndexHTMLCode = IndexHTMLCode+" <a href=\""+getpyurlinfo['videos']['favorited'][counti]['url'].replace('http://motherless.com', '')+"\"><img src=\""+getpyurlinfo['videos']['favorited'][counti]['thumbnail']+"\" alt=\""+getpyurlinfo['videos']['favorited'][counti]['title']+"\" title=\""+getpyurlinfo['videos']['favorited'][counti]['title']+"\" /></a>\n";
    counti = counti + 1;
   IndexHTMLCode = IndexHTMLCode+"<div><br />&nbsp;<br /></div>\n";
   counti = 0;
   while(counti<15):
    IndexHTMLCode = IndexHTMLCode+" <a href=\""+getpyurlinfo['videos']['viewed'][counti]['url'].replace('http://motherless.com', '')+"\"><img src=\""+getpyurlinfo['videos']['viewed'][counti]['thumbnail']+"\" alt=\""+getpyurlinfo['videos']['viewed'][counti]['title']+"\" title=\""+getpyurlinfo['videos']['viewed'][counti]['title']+"\" /></a>\n";
    counti = counti + 1;
   IndexHTMLCode = IndexHTMLCode+"<div><br />&nbsp;<br /></div>\n";
   counti = 0;
   while(counti<15):
    IndexHTMLCode = IndexHTMLCode+" <a href=\""+getpyurlinfo['videos']['commented'][counti]['url'].replace('http://motherless.com', '')+"\"><img src=\""+getpyurlinfo['videos']['commented'][counti]['thumbnail']+"\" alt=\""+getpyurlinfo['videos']['commented'][counti]['title']+"\" title=\""+getpyurlinfo['videos']['commented'][counti]['title']+"\" /></a>\n";
    counti = counti + 1;
   IndexHTMLCode = IndexHTMLCode+"<div><br />&nbsp;<br /></div>\n";
   counti = 0;
   while(counti<15):
    IndexHTMLCode = IndexHTMLCode+" <a href=\""+getpyurlinfo['videos']['popular'][counti]['url'].replace('http://motherless.com', '')+"\"><img src=\""+getpyurlinfo['videos']['popular'][counti]['thumbnail']+"\" alt=\""+getpyurlinfo['videos']['popular'][counti]['title']+"\" title=\""+getpyurlinfo['videos']['popular'][counti]['title']+"\" /></a>\n";
    counti = counti + 1;
   IndexHTMLCode = IndexHTMLCode+"<div><br />&nbsp;<br /></div>\n";
   counti = 0;
   while(counti<15):
    IndexHTMLCode = IndexHTMLCode+" <a href=\""+getpyurlinfo['videos']['live'][counti]['url'].replace('http://motherless.com', '')+"\"><img src=\""+getpyurlinfo['videos']['live'][counti]['thumbnail']+"\" alt=\""+getpyurlinfo['videos']['live'][counti]['title']+"\" title=\""+getpyurlinfo['videos']['live'][counti]['title']+"\" /></a>\n";
    counti = counti + 1;
   IndexHTMLCode = IndexHTMLCode+"<div><br />&nbsp;<br /></div>\n";
   counti = 0;
   while(counti<15):
    IndexHTMLCode = IndexHTMLCode+" <a href=\""+getpyurlinfo['videos']['random'][counti]['url'].replace('http://motherless.com', '')+"\"><img src=\""+getpyurlinfo['videos']['random'][counti]['thumbnail']+"\" alt=\""+getpyurlinfo['videos']['random'][counti]['title']+"\" title=\""+getpyurlinfo['videos']['random'][counti]['title']+"\" /></a>\n";
    counti = counti + 1;
  if(pymotherlessinfo['motherlessinfo']=="sample-images"):
   IndexHTMLCode = "";
   getpyurlinfo = pymotherless.get_motherless_sample_links(geturls_headers, geturls_cj, numoflinks=15, urltype="image");
   counti = 0;
   while(counti<15):
    IndexHTMLCode = IndexHTMLCode+" <a href=\""+getpyurlinfo['images']['recent'][counti]['url'].replace('http://motherless.com', '')+"\"><img src=\""+getpyurlinfo['images']['recent'][counti]['thumbnail']+"\" alt=\""+getpyurlinfo['images']['recent'][counti]['title']+"\" title=\""+getpyurlinfo['images']['recent'][counti]['title']+"\" /></a>\n";
    counti = counti + 1;
   IndexHTMLCode = IndexHTMLCode+"<div><br />&nbsp;<br /></div>\n";
   counti = 0;
   while(counti<15):
    IndexHTMLCode = IndexHTMLCode+" <a href=\""+getpyurlinfo['images']['favorited'][counti]['url'].replace('http://motherless.com', '')+"\"><img src=\""+getpyurlinfo['images']['favorited'][counti]['thumbnail']+"\" alt=\""+getpyurlinfo['images']['favorited'][counti]['title']+"\" title=\""+getpyurlinfo['images']['favorited'][counti]['title']+"\" /></a>\n";
    counti = counti + 1;
   IndexHTMLCode = IndexHTMLCode+"<div><br />&nbsp;<br /></div>\n";
   counti = 0;
   while(counti<15):
    IndexHTMLCode = IndexHTMLCode+" <a href=\""+getpyurlinfo['images']['viewed'][counti]['url'].replace('http://motherless.com', '')+"\"><img src=\""+getpyurlinfo['images']['viewed'][counti]['thumbnail']+"\" alt=\""+getpyurlinfo['images']['viewed'][counti]['title']+"\" title=\""+getpyurlinfo['images']['viewed'][counti]['title']+"\" /></a>\n";
    counti = counti + 1;
   IndexHTMLCode = IndexHTMLCode+"<div><br />&nbsp;<br /></div>\n";
   counti = 0;
   while(counti<15):
    IndexHTMLCode = IndexHTMLCode+" <a href=\""+getpyurlinfo['images']['commented'][counti]['url'].replace('http://motherless.com', '')+"\"><img src=\""+getpyurlinfo['images']['commented'][counti]['thumbnail']+"\" alt=\""+getpyurlinfo['images']['commented'][counti]['title']+"\" title=\""+getpyurlinfo['images']['commented'][counti]['title']+"\" /></a>\n";
    counti = counti + 1;
   IndexHTMLCode = IndexHTMLCode+"<div><br />&nbsp;<br /></div>\n";
   counti = 0;
   while(counti<15):
    IndexHTMLCode = IndexHTMLCode+" <a href=\""+getpyurlinfo['images']['popular'][counti]['url'].replace('http://motherless.com', '')+"\"><img src=\""+getpyurlinfo['images']['popular'][counti]['thumbnail']+"\" alt=\""+getpyurlinfo['images']['popular'][counti]['title']+"\" title=\""+getpyurlinfo['images']['popular'][counti]['title']+"\" /></a>\n";
    counti = counti + 1;
   IndexHTMLCode = IndexHTMLCode+"<div><br />&nbsp;<br /></div>\n";
   counti = 0;
   while(counti<15):
    IndexHTMLCode = IndexHTMLCode+" <a href=\""+getpyurlinfo['images']['live'][counti]['url'].replace('http://motherless.com', '')+"\"><img src=\""+getpyurlinfo['images']['live'][counti]['thumbnail']+"\" alt=\""+getpyurlinfo['images']['live'][counti]['title']+"\" title=\""+getpyurlinfo['images']['live'][counti]['title']+"\" /></a>\n";
    counti = counti + 1;
   IndexHTMLCode = IndexHTMLCode+"<div><br />&nbsp;<br /></div>\n";
   counti = 0;
   while(counti<15):
    IndexHTMLCode = IndexHTMLCode+" <a href=\""+getpyurlinfo['images']['random'][counti]['url'].replace('http://motherless.com', '')+"\"><img src=\""+getpyurlinfo['images']['random'][counti]['thumbnail']+"\" alt=\""+getpyurlinfo['images']['random'][counti]['title']+"\" title=\""+getpyurlinfo['images']['random'][counti]['title']+"\" /></a>\n";
    counti = counti + 1;
  if(pymotherlessinfo['motherlessinfo']=="gallery"):
   IndexHTMLCode = "";
   try: 
    getpage=int(cherrypy.request.params.get('page', None));
   except TypeError:
    getpage=1;
   except ValueError:
    getpage=1;
   getpyurlinfo = pymotherless.get_motherless_galleries_links(getpymotherless, geturls_headers, geturls_cj, page=getpage);
   counti = 0;
   maxi = getpyurlinfo['numoflinks'];
   while(counti<maxi):
    IndexHTMLCode = IndexHTMLCode+" <a href=\""+getpyurlinfo[counti]['url'].replace('http://motherless.com', '')+"\"><img src=\""+getpyurlinfo[counti]['thumbnail']+"\" alt=\""+getpyurlinfo[counti]['title']+"\" title=\""+getpyurlinfo[counti]['title']+"\" /></a>\n";
    counti = counti + 1;
   IndexHTMLCode = IndexHTMLCode+"<div><br />&nbsp;<br /></div>\n";
   counti = 1;
   maxi = getpyurlinfo['pages'];
   print(str(maxi));
   while(counti<maxi):
    IndexHTMLCode = IndexHTMLCode+" <a href=\"?page="+str(counti)+"\">"+str(counti)+"</a>\n";
    counti = counti + 1;
  if(pymotherlessinfo['motherlessinfo']=="group"):
   IndexHTMLCode = "";
   try: 
    getpage=int(cherrypy.request.params.get('page', None));
   except TypeError:
    getpage=1;
   except ValueError:
    getpage=1;
   getpyurlinfo = pymotherless.get_motherless_groups(getpymotherless, geturls_headers, geturls_cj, page=getpage);
   counti = 0;
   maxi = getpyurlinfo['numoflinks'];
   while(counti<maxi):
    IndexHTMLCode = IndexHTMLCode+" <a href=\""+getpyurlinfo[counti]['url'].replace('http://motherless.com', '')+"\"><img src=\""+getpyurlinfo[counti]['thumbnail']+"\" alt=\""+getpyurlinfo[counti]['title']+"\" title=\""+getpyurlinfo[counti]['title']+"\" /></a>\n";
    counti = counti + 1;
   IndexHTMLCode = IndexHTMLCode+"<div><br />&nbsp;<br /></div>\n";
   counti = 1;
   maxi = getpyurlinfo['pages'];
   print(str(maxi));
   while(counti<maxi):
    IndexHTMLCode = IndexHTMLCode+" <a href=\"?page="+str(counti)+"\">"+str(counti)+"</a>\n";
    counti = counti + 1;
  if(pymotherlessinfo['motherlessinfo']=="member"):
   IndexHTMLCode = "";
   try: 
    getpage=int(cherrypy.request.params.get('page', None));
   except TypeError:
    getpage=1;
   except ValueError:
    getpage=1;
   getpyurlinfo = pymotherless.get_motherless_search_members(getpymotherless, geturls_headers, geturls_cj, page=getpage);
   counti = 0;
   maxi = getpyurlinfo['numoflinks'];
   while(counti<maxi):
    IndexHTMLCode = IndexHTMLCode+" <a href=\""+getpyurlinfo[counti]['url'].replace('http://motherless.com', '')+"\"><img src=\""+getpyurlinfo[counti]['avatarurl']+"\" alt=\""+getpyurlinfo[counti]['username']+"\" title=\""+getpyurlinfo[counti]['username']+"\" /></a>\n";
    counti = counti + 1;
   IndexHTMLCode = IndexHTMLCode+"<div><br />&nbsp;<br /></div>\n";
   counti = 1;
   maxi = getpyurlinfo['pages'];
   print(str(maxi));
   while(counti<maxi):
    IndexHTMLCode = IndexHTMLCode+" <a href=\"?page="+str(counti)+"\">"+str(counti)+"</a>\n";
    counti = counti + 1;
  if(pymotherlessinfo['motherlessinfo']=="link"):
   IndexHTMLCode = "";
   getpyurlinfo = pymotherless.get_motherless_links(getpymotherless, geturls_headers, geturls_cj);
   if(getpyurlinfo['type']=="images"):
    IndexHTMLCode = "<img src=\""+getpyurlinfo['url']+"\" alt=\""+getpyurlinfo['title']+"\" title=\""+getpyurlinfo['title']+"\" style=\"width: "+str(getpyurlinfo['width'])+"px; height: "+str(getpyurlinfo['height'])+"px;\" />";
   if(getpyurlinfo['type']=="videos"):
    IndexHTMLCode = "<video width=\"632\" height=\"432\" controls><source src=\""+getpyurlinfo['url']+"\" type=\"video/mp4\">Your browser does not support the video tag.</video>";
   IndexHTMLCode = IndexHTMLCode+"<div><br />&nbsp;<br /></div>\n";
   getpyurlcomet = pymotherless.get_motherless_links_comments(getpymotherless, geturls_headers, geturls_cj);
   counti = 0;
   maxi = getpyurlcomet['numofallposts'];
   while(counti<maxi):
    IndexHTMLCode = IndexHTMLCode+"<fieldset><legend>"+getpyurlcomet[counti]['username']+"</legend><img src=\""+getpyurlcomet[counti]['avatarurl']+"\" alt=\""+getpyurlcomet[counti]['username']+"\" title=\""+getpyurlcomet[counti]['username']+"\" /><br />"+getpyurlcomet[counti]['post']+"</fieldset>";
    counti = counti + 1;
  return IndexHTMLCode;
 default.exposed = True;

cherrypy.config.update({"environment": serv_environ,
                        "log.error_file": errorlog,
                        "log.access_file": accesslog,
                        "log.screen": getargs.verbose,
                        "gzipfilter.on": getargs.gzipfilter,
                        "tools.gzip.on": getargs.gzip,
                        "tools.gzip.mime_types": ['text/*'],
                        "server.socket_host": host,
                        "server.socket_port": port,
                        "response.timeout": timeout,
                        });
cherrypy.quickstart(GenerateIndexPage());
