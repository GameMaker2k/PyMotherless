#!/usr/bin/env python

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2013 Cool Dude 2k - http://idb.berlios.de/
    Copyright 2013 Game Maker 2k - http://intdb.sourceforge.net/
    Copyright 2013 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: motherless-dl.py - Last Update: 05/11/2013 Ver. 1.0.5 RC 5 - Author: cooldude2k $
'''

import re, os, sys, httplib, urllib, urllib2, cookielib, StringIO, gzip, time, datetime, argparse, urlparse;

parser = argparse.ArgumentParser();
parser.add_argument("url", help="motherless url");
getargs = parser.parse_args();
mlessvid = getargs.url;
mregex_text = re.escape("http://motherless.com/")+"([a-zA-Z0-9\/]+)";
if(re.findall(mregex_text, mlessvid)):
 mlessvid = re.findall(mregex_text, mlessvid);
 mlessvid = mlessvid[0];
fakeua = "Mozilla/5.0 (Windows NT 5.1; rv:20.0) Gecko/20100101 Firefox/20.0";
geturls_cj = cookielib.CookieJar();
geturls_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(geturls_cj));
geturls_opener.addheaders = [("Referer", "http://motherless.com/"), ("User-Agent", fakeua), ("Accept-Encoding", "gzip, deflate"), ("Accept-Language", "en-US,en-CA,en-GB,en-UK,en-AU,en-NZ,en-ZA,en;q=0.5"), ("Accept-Charset", "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7"), ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"), ("Connection", "close")];
geturls_text = geturls_opener.open("http://motherless.com/"+mlessvid);
if(geturls_text.info().get("Content-Encoding")=="gzip" or geturls_text.info().get("Content-Encoding")=="deflate"):
 strbuf = StringIO.StringIO(geturls_text.read());
 gzstrbuf = gzip.GzipFile(fileobj=strbuf);
 out_text = gzstrbuf.read()[:];
if(geturls_text.info().get("Content-Encoding")!="gzip" and geturls_text.info().get("Content-Encoding")!="deflate"):
 out_text = geturls_text.read()[:];

mlessvidid = urlparse.urlparse(mlessvid).path.split('/');
mlessurllist = [];
if(re.match("^G", mlessvidid[0]) and len(mlessvidid)==1):
 regex_text = re.escape("<a href=\"")+"([\w\/]+)"+re.escape("\" class=\"img-container\" target=\"_self\">");
 post_text = re.findall(regex_text, out_text);
 numurls = len(post_text);
 cururl = 0;
 while(cururl<numurls):
  mlessurllist.append(post_text[cururl]);
  cururl = cururl + 1;
if(not re.match("^G", mlessvidid[0]) or len(mlessvidid)>1):
 mlessurllist.append(mlessvid);

numlist = len(mlessurllist);
curlurl = 0;
while(curlurl<numlist):
 geturls_text = geturls_opener.open("http://motherless.com/"+mlessurllist[curlurl]);
 if(geturls_text.info().get("Content-Encoding")=="gzip" or geturls_text.info().get("Content-Encoding")=="deflate"):
  strbuf = StringIO.StringIO(geturls_text.read());
  gzstrbuf = gzip.GzipFile(fileobj=strbuf);
  subout_text = gzstrbuf.read()[:];
 if(geturls_text.info().get("Content-Encoding")!="gzip" and geturls_text.info().get("Content-Encoding")!="deflate"):
  subout_text = geturls_text.read()[:];
 regex_text = re.escape("__fileurl = '")+"(.*)"+re.escape("';");
 post_text = re.findall(regex_text, subout_text);
 if(post_text>0):
  mlesslink = post_text[0];
  mlessext = os.path.splitext(urlparse.urlparse(mlesslink).path)[1];
  mlessext = mlessext.replace(".", "");
  mlessext = mlessext.lower();
  if(mlessext=="mp4" or mlessext=="flv"):
   mlesslink = mlesslink+"?start=0";
  print(mlesslink);
 curlurl = curlurl + 1;
 '''
 getvidurls_cj = cookielib.CookieJar();
 getvidurls_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(getvidurls_cj));
 getvidurls_opener.addheaders = [("Referer", "http://motherless.com/"+mlessvid), ("User-Agent", fakeua), ("Accept-Encoding", "gzip, deflate"), ("Accept-Language", "en-US,en-CA,en-GB,en-UK,en-AU,en-NZ,en-ZA,en;q=0.5"), ("Accept-Charset", "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7"), ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"), ("Connection", "close")];
 getvidurls_text = getvidurls_opener.open(mlesslink);
 def chunk_report(bytes_so_far, chunk_size, total_size):
  percent = float(bytes_so_far) / total_size;
  percent = round(percent*100, 2);
  sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%)\r" % 
    (bytes_so_far, total_size, percent));
  if bytes_so_far >= total_size:
   sys.stdout.write("\n");
 def chunk_read(response, chunk_size=8192, report_hook=None):
  total_size = response.info().getheader("Content-Length").strip();
  total_size = int(total_size);
  bytes_so_far = 0;
  while 1:
   chunk = response.read(chunk_size);
   bytes_so_far += len(chunk);
   if not chunk:
    break;
   if report_hook:
    report_hook(bytes_so_far, chunk_size, total_size);
  return bytes_so_far;
 chunk_read(getvidurls_text, report_hook=chunk_report);
 vidfile = open(os.getcwd()+os.sep+os.path.basename(urllib2.urlparse.urlsplit(mlesslink)[2]), "wb");
 vidfile.write(getvidurls_text.read());
 vidfile.close();
 '''
