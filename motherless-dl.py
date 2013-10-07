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

    $FileInfo: motherless-dl.py - Last Update: 10/06/2013 Ver. 1.4.5 RC 1 - Author: cooldude2k $
'''

import re, os, sys, httplib, urllib, urllib2, cookielib, StringIO, gzip, time, datetime, argparse, urlparse;

__version_info__ = (1, 4, 5, "RC 1");
if(__version_info__[3]!=None):
 __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2])+" "+str(__version_info__[3]);
if(__version_info__[3]==None):
 __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2]);

parser = argparse.ArgumentParser();
parser.add_argument("url", nargs="*", help="motherless url");
parser.add_argument("--user-agent", nargs="?", default="Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0", help="specify a custom user agent");
parser.add_argument("--referer", nargs="?", default="http://motherless.com/", help="specify a custom referer, use if the video access");
parser.add_argument("--verbose", action='store_true', help="print various debugging information");
parser.add_argument("--dump-user-agent", action='store_true', help="display the current browser identification");
parser.add_argument("--version", action='store_true', help="print program version and exit");
parser.add_argument("--update", action='store_true', help="update this program to latest version. Make sure that you have sufficient permissions (run with sudo if needed)");
getargs = parser.parse_args();
if(getargs.version==True):
 print(__version__);
 sys.exit();
if(getargs.dump_user_agent==True):
 print(getargs.user_agent);
 sys.exit();
if(len(getargs.url)==0):
 parser.print_help();
 sys.exit();

fakeua = getargs.user_agent;
geturls_cj = cookielib.CookieJar();
geturls_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(geturls_cj));
geturls_opener.addheaders = [("Referer", getargs.referer), ("User-Agent", fakeua), ("Accept-Encoding", "gzip, deflate"), ("Accept-Language", "en-US,en-CA,en-GB,en-UK,en-AU,en-NZ,en-ZA,en;q=0.5"), ("Accept-Charset", "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7"), ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"), ("Connection", "close")];
per_gal_sleep = 0;
per_url_sleep = 0;

numurlarg = len(getargs.url);
cururlarg = 0;
while(cururlarg<numurlarg):
 mlessvid = getargs.url[cururlarg];
 mlessvid = re.sub(re.escape("http://motherless.com/"), "", mlessvid);
 mlessvid = re.sub(re.escape("http://www.motherless.com/"), "", mlessvid);
 mlessvid = re.sub(re.escape("motherless.com/"), "", mlessvid);
 mlessvid = re.sub(re.escape("www.motherless.com/"), "", mlessvid);
 mlessvid = re.sub("^"+re.escape("/"), "", mlessvid);
 mlessvid = "http://motherless.com/"+mlessvid;
 mregex_text = re.escape("http://motherless.com/")+"([\w\/]+)";
 if(re.findall(mregex_text, mlessvid)):
  mlessvid = re.findall(mregex_text, mlessvid);
  mlessvid = "/"+mlessvid[0];
 mlessvidid = urlparse.urlparse(mlessvid).path.split('/');
 mlessgallist = [];
 if((re.match("^random", mlessvidid[1]) and len(mlessvidid)==2) or (re.match("^random", mlessvidid[1]) and len(mlessvidid)==3) and (re.match("^image", mlessvidid[2]) or re.match("^video", mlessvidid[2]))):
  geturls_text = geturls_opener.open("http://motherless.com"+mlessvid);
  mlessvid = geturls_text.geturl();
  if(re.findall(mregex_text, mlessvid)):
   mlessvid = re.findall(mregex_text, mlessvid);
   mlessvid = mlessvid[0];
 if((re.match("^galleries", mlessvidid[1]) and len(mlessvidid)==4) or (re.match("^f", mlessvidid[1]) and re.match("^galleries", mlessvidid[2]) and len(mlessvidid)==4)):
  geturls_text = geturls_opener.open("http://motherless.com"+mlessvid+"?page=1");
  if(geturls_text.info().get("Content-Encoding")=="gzip" or geturls_text.info().get("Content-Encoding")=="deflate"):
   strbuf = StringIO.StringIO(geturls_text.read());
   gzstrbuf = gzip.GzipFile(fileobj=strbuf);
   out_text = gzstrbuf.read()[:];
  if(geturls_text.info().get("Content-Encoding")!="gzip" and geturls_text.info().get("Content-Encoding")!="deflate"):
   out_text = geturls_text.read()[:];
  out_text = re.sub(re.escape("http://motherless.com"), "", out_text);
  out_text = re.sub(re.escape("http://www.motherless.com"), "", out_text);
  regex_ptext = re.escape("class=\"pop\" rel=\"")+"([0-9]+)"+re.escape("\">")+"([0-9]+)"+re.escape("</a>");
  page_text = re.findall(regex_ptext, out_text);
  try:
   numpages = int(page_text[-1][0]);
  except IndexError:
   numpages = 1;
  curpage = 1;
  while(curpage<=numpages):
   if(curpage>1):
    geturls_text = geturls_opener.open("http://motherless.com/"+mlessvid+"?page="+str(curpage));
    if(geturls_text.info().get("Content-Encoding")=="gzip" or geturls_text.info().get("Content-Encoding")=="deflate"):
     strbuf = StringIO.StringIO(geturls_text.read());
     gzstrbuf = gzip.GzipFile(fileobj=strbuf);
     out_text = gzstrbuf.read()[:];
    if(geturls_text.info().get("Content-Encoding")!="gzip" and geturls_text.info().get("Content-Encoding")!="deflate"):
     out_text = geturls_text.read()[:];
    out_text = re.sub(re.escape("http://motherless.com"), "", out_text);
    out_text = re.sub(re.escape("http://www.motherless.com"), "", out_text);
   regex_text = re.escape("")+"([\w\/]+)"+re.escape("\" class=\"img-container\" target=\"_self\">");
   post_text = re.findall(regex_text, out_text);
   numgal = len(post_text);
   curgal = 0;
   while(curgal<numgal):
    mlessgallist.append(post_text[curgal]);
    curgal = curgal + 1;
   curpage = curpage + 1;
 if(not re.match("^galleries", mlessvidid[1]) or (re.match("^galleries", mlessvidid[1]) and len(mlessvidid)<4) or (re.match("^galleries", mlessvidid[1]) and len(mlessvidid)>5)):
  mlessgallist.append(mlessvid);
 numusrgal = len(mlessgallist);
 curusrgal = 0;
 while(curusrgal<numusrgal):
  mlessvid = mlessgallist[curusrgal];
  if(not re.match("^\/", mlessvid)):
   mlessvid = "/"+mlessvid;
  mlessvidid = urlparse.urlparse(mlessvid).path.split('/');
  mlessurllist = [];
  if((re.match("^G", mlessvidid[1]) and len(mlessvidid)==2) or (re.match("^V", mlessvidid[1]) and len(mlessvidid)==2) or (re.match("^g", mlessvidid[1]) and len(mlessvidid)==3) or (re.match("^f", mlessvidid[1]) and len(mlessvidid)==4 and (re.match("^videos", mlessvidid[3]) or re.match("^images", mlessvidid[3]))) or (re.match("^live", mlessvidid[1]) and len(mlessvidid)==3 and (re.match("^images", mlessvidid[2]) or re.match("^videos", mlessvidid[2]))) or (re.match("^images", mlessvidid[1]) and len(mlessvidid)==3 and (re.match("^favorited", mlessvidid[2]) or re.match("^viewed", mlessvidid[2]) or re.match("^commented", mlessvidid[2]) or re.match("^popular", mlessvidid[2]))) or (re.match("^videos", mlessvidid[1]) and len(mlessvidid)==3 and (re.match("^favorited", mlessvidid[2]) or re.match("^viewed", mlessvidid[2]) or re.match("^commented", mlessvidid[2]) or re.match("^popular", mlessvidid[2])))):
   geturls_text = geturls_opener.open("http://motherless.com"+mlessvid+"?page=1");
   if(geturls_text.info().get("Content-Encoding")=="gzip" or geturls_text.info().get("Content-Encoding")=="deflate"):
    strbuf = StringIO.StringIO(geturls_text.read());
    gzstrbuf = gzip.GzipFile(fileobj=strbuf);
    out_text = gzstrbuf.read()[:];
   if(geturls_text.info().get("Content-Encoding")!="gzip" and geturls_text.info().get("Content-Encoding")!="deflate"):
    out_text = geturls_text.read()[:];
   out_text = re.sub(re.escape("http://motherless.com"), "", out_text);
   out_text = re.sub(re.escape("http://www.motherless.com"), "", out_text);
   regex_ptext = re.escape("class=\"pop\" rel=\"")+"([0-9]+)"+re.escape("\">")+"([0-9]+)"+re.escape("</a>");
   page_text = re.findall(regex_ptext, out_text);
   try:
    numpages = int(page_text[-1][0]);
   except IndexError:
    numpages = 1;
   curpage = 1;
   while(curpage<=numpages):
    if(curpage>1):
     geturls_text = geturls_opener.open("http://motherless.com"+mlessvid+"?page="+str(curpage));
     if(geturls_text.info().get("Content-Encoding")=="gzip" or geturls_text.info().get("Content-Encoding")=="deflate"):
      strbuf = StringIO.StringIO(geturls_text.read());
      gzstrbuf = gzip.GzipFile(fileobj=strbuf);
      out_text = gzstrbuf.read()[:];
     if(geturls_text.info().get("Content-Encoding")!="gzip" and geturls_text.info().get("Content-Encoding")!="deflate"):
      out_text = geturls_text.read()[:];
    out_text = re.sub(re.escape("http://motherless.com"), "", out_text);
    out_text = re.sub(re.escape("http://www.motherless.com"), "", out_text);
    if(re.match("^V", mlessvidid[1])):
     out_text = re.sub(re.escape("class=\"img-container\" target=\"_self\""), "title=\"motherless link\"", out_text);
     out_text = re.sub(re.escape("class=\"pop plain\" target=\"_blank\""), "title=\"motherless link\"", out_text);
     regex_text = re.escape("<a href=\"")+"([\w\/]+)"+re.escape("\" title=\"motherless link\">");
    if(not re.match("^V", mlessvidid[1])):
     regex_text = re.escape("")+"([\w\/]+)"+re.escape("\" class=\"img-container\" target=\"_self\">");
    post_text = re.findall(regex_text, out_text);
    numurls = len(post_text);
    cururl = 0;
    while(cururl<numurls):
     mlessurllist.append(post_text[cururl]);
     cururl = cururl + 1;
    curpage = curpage + 1;
  if((re.match("^G", mlessvidid[1]) and len(mlessvidid)==3 and re.match("([0-9A-F]+)", mlessvidid[2])) or (len(mlessvidid)==2 and re.match("([0-9A-F]+)", mlessvidid[1]))):
   mlessurllist.append(mlessvid);
  numlist = len(mlessurllist);
  curlurl = 0;
  while(curlurl<numlist):
   geturls_text = geturls_opener.open("http://motherless.com"+mlessurllist[curlurl]);
   if(geturls_text.info().get("Content-Encoding")=="gzip" or geturls_text.info().get("Content-Encoding")=="deflate"):
    strbuf = StringIO.StringIO(geturls_text.read());
    gzstrbuf = gzip.GzipFile(fileobj=strbuf);
    subout_text = gzstrbuf.read()[:];
   if(geturls_text.info().get("Content-Encoding")!="gzip" and geturls_text.info().get("Content-Encoding")!="deflate"):
    subout_text = geturls_text.read()[:];
   subout_text = re.sub(re.escape("http://motherless.com"), "", subout_text);
   subout_text = re.sub(re.escape("http://www.motherless.com"), "", subout_text);
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
   if(curlurl<(numlist - 1)):
    time.sleep(per_url_sleep);
   curlurl = curlurl + 1;
  if(curusrgal<(numusrgal - 1)):
   time.sleep(per_gal_sleep);
  curusrgal = curusrgal + 1;
 cururlarg = cururlarg + 1;

 '''
 getvidurls_cj = cookielib.CookieJar();
 getvidurls_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(getvidurls_cj));
 getvidurls_opener.addheaders = [("Referer", getargs.referer+mlessvid), ("User-Agent", fakeua), ("Accept-Encoding", "gzip, deflate"), ("Accept-Language", "en-US,en-CA,en-GB,en-UK,en-AU,en-NZ,en-ZA,en;q=0.5"), ("Accept-Charset", "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7"), ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"), ("Connection", "close")];
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
