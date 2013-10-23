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

    $FileInfo: motherless-dl.py - Last Update: 10/23/2013 Ver. 1.6.5 RC 3 - Author: cooldude2k $
'''

from __future__ import division, absolute_import, print_function;
import re, os, sys, urllib, urllib2, cookielib, StringIO, gzip, time, datetime, argparse, urlparse;
if(__name__ == "__main__"):
 sys.tracebacklimit = 0;
__version_info__ = (1, 6, 5, "RC 3");
__version_date__ = "2013.10.23";
if(__version_info__[3]!=None):
 __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2])+" "+str(__version_info__[3]);
if(__version_info__[3]==None):
 __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2]);

parser = argparse.ArgumentParser(description="get urls of images/videos from motherless.com", conflict_handler="resolve", add_help=True);
parser.add_argument("url", nargs="*", help="motherless url");
parser.add_argument('-v', '--version', action='version', version=__version__)
parser.add_argument("--update", action='store_true', help="update this program to latest version. Make sure that you have sufficient permissions (run with sudo if needed)");
parser.add_argument("--dump-user-agent", action='store_true', help="display the current browser identification");
parser.add_argument("--user-agent", nargs="?", default="Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0", help="specify a custom user agent");
parser.add_argument("--referer", nargs="?", default="http://motherless.com/", help="specify a custom referer, use if the video access");
parser.add_argument("--proxy", nargs="?", default=None, help="Use the specified HTTP/HTTPS proxy");
parser.add_argument("--id", action='store_true', help="use only video ID in file name");
parser.add_argument("--get-url", action='store_true', help="simulate, quiet but print URL");
parser.add_argument("--get-pageurl", action='store_true', help="simulate, quiet but print URL");
parser.add_argument("--get-title", action='store_true', help="simulate, quiet but print title");
parser.add_argument("--get-posts", action='store_true', help="simulate, quiet but print user posts");
parser.add_argument("--get-id", action='store_true', help="simulate, quiet but print id");
parser.add_argument("--get-thumbnail", action='store_true', help="simulate, quiet but print thumbnail URL");
parser.add_argument("--get-filename", action='store_true', help="simulate, quiet but print output filename");
parser.add_argument("--get-format", action='store_true', help="simulate, quiet but print file format");
parser.add_argument("--get-type", action='store_true', help="simulate, quiet but print file type");
parser.add_argument("--get-username", action='store_true', help="simulate, quiet but print uploaders username");
parser.add_argument("--get-bbcode", action='store_true', help="simulate, quiet but print bbcode");
parser.add_argument("--get-html", action='store_true', help="simulate, quiet but print html code");
parser.add_argument("--get-dimensions", action='store_true', help="simulate, quiet but print dimensions (width x height)");
parser.add_argument("--get-width", action='store_true', help="simulate, quiet but print width");
parser.add_argument("--get-height", action='store_true', help="simulate, quiet but print height");
parser.add_argument("--get-views", action='store_true', help="simulate, quiet but print number of views");
parser.add_argument("--get-favorites", action='store_true', help="simulate, quiet but print number of favorites");
parser.add_argument("--verbose", action='store_true', help="print various debugging information");
getargs = parser.parse_args();

if(getargs.update==True):
 from distutils.version import LooseVersion as VerCheck;
 fakeua = getargs.user_agent;
 proxycfg = None;
 if(getargs.proxy!=None):
  proxycfg = urllib2.ProxyHandler({"http": getargs.proxy});
 geturls_cj = cookielib.CookieJar();
 if(proxycfg==None):
  geturls_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(geturls_cj));
 if(proxycfg!=None):
  geturls_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(geturls_cj), proxycfg);
 geturls_opener.addheaders = [("Referer", "https://github.com/GameMaker2k/Python-Scripts/"), ("User-Agent", fakeua), ("Accept-Encoding", "gzip, deflate"), ("Accept-Language", "en-US,en;q=0.8,en-CA,en-GB;q=0.6"), ("Accept-Charset", "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7"), ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"), ("Connection", "close")];
 urllib2.install_opener(geturls_opener);
 geturls_text = geturls_opener.open("https://raw.github.com/GameMaker2k/Python-Scripts/master/MiniScripts/motherless-dl.py");
 if(geturls_text.info().get("Content-Encoding")=="gzip" or geturls_text.info().get("Content-Encoding")=="deflate"):
  strbuf = StringIO.StringIO(geturls_text.read());
  gzstrbuf = gzip.GzipFile(fileobj=strbuf);
  pyfile_text = gzstrbuf.read()[:];
 if(geturls_text.info().get("Content-Encoding")!="gzip" and geturls_text.info().get("Content-Encoding")!="deflate"):
  pyfile_text = geturls_text.read()[:];
 regex_finddate_text = re.escape("__version_date__ = \"")+"([0-9\.]+)"+re.escape("\"");
 finddate_text = re.findall(regex_finddate_text, pyfile_text);
 regex_findver_text = re.escape("__version_info__ = (")+"([0-9]+)"+re.escape(", ")+"([0-9]+)"+re.escape(", ")+"([0-9]+)"+re.escape(", \"")+"([A-Z0-9 ]+)"+re.escape("\");");
 findver_text = re.findall(regex_findver_text, pyfile_text);
 ProVerStr = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2])+__version_info__[3].replace(" ", "").lower();
 ProVerCheck = VerCheck(ProVerStr);
 ProDateCheck = VerCheck(__version_date__);
 NewVerStr = findver_text[0][0]+"."+findver_text[0][1]+"."+findver_text[0][2]+findver_text[0][3].replace(" ", "").lower();
 NewVerCheck = VerCheck(NewVerStr);
 NewDateCheck = VerCheck(finddate_text[0]);
 if(ProVerStr < NewVerCheck and ProDateCheck <= NewDateCheck):
  fileopen = open(__file__, "w+");
  fileopen.write(pyfile_text);
  fileopen.close();
 print();
 sys.exit();

if(getargs.dump_user_agent==True):
 print(getargs.user_agent);
 sys.exit();
if(len(getargs.url)==0):
 parser.print_help();
 sys.exit();
def motherless_dl(mtlessgetargs=vars(getargs)):
 fakeua = mtlessgetargs["user_agent"];
 proxycfg = None;
 if(mtlessgetargs["proxy"]!=None):
  proxycfg = urllib2.ProxyHandler({"http": mtlessgetargs["proxy"]});
 geturls_cj = cookielib.CookieJar();
 if(proxycfg==None):
  geturls_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(geturls_cj));
 if(proxycfg!=None):
  geturls_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(geturls_cj), proxycfg);
 geturls_opener.addheaders = [("Referer", mtlessgetargs["referer"]), ("User-Agent", fakeua), ("Accept-Encoding", "gzip, deflate"), ("Accept-Language", "en-US,en;q=0.8,en-CA,en-GB;q=0.6"), ("Accept-Charset", "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7"), ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"), ("Connection", "close")];
 urllib2.install_opener(geturls_opener);
 per_gal_sleep = 0;
 per_url_sleep = 0;
 numurlarg = len(mtlessgetargs["url"]);
 cururlarg = 0;
 while(cururlarg<numurlarg):
  mlessvid = mtlessgetargs["url"][cururlarg];
  if(re.match("^s([0-9]+)"+re.escape(".motherlessmedia.com"), urlparse.urlparse(mlessvid).hostname)):
   geturls_text = geturls_opener.open("http://motherless.com/mogile_api.php?path="+urllib.quote_plus(mlessvid)+"&redirect=1");
   mlessvid = geturls_text.geturl();
   mregex_text = re.escape("http://motherless.com/")+"([\w\/\?\&\=]+)";
   if(re.findall(mregex_text, mlessvid)):
    mlessvid = re.findall(mregex_text, mlessvid);
    mlessvid = "http://motherless.com/"+mlessvid[0];
    if(mtlessgetargs["verbose"]==True):
     print(mlessvid);
  if(re.match("^"+re.escape("thumbs.motherlessmedia.com"), urlparse.urlparse(mlessvid).hostname)):
   mlessvid = re.sub(re.escape("-zoom"), "", mlessvid);
   mlessvid = re.sub(re.escape("-strip"), "", mlessvid);
   mlessvidtmp = urlparse.urlparse(mlessvid).path.split("/");
   mlessvid = "http://motherless.com/"+mlessvidtmp[2];
   mregex_text = re.escape("http://motherless.com/")+"([\w\/\?\&\=]+)";
   if(re.findall(mregex_text, mlessvid)):
    mlessvid = re.findall(mregex_text, mlessvid);
    mlessvid = "http://motherless.com/"+mlessvid[0];
  mlessvid = re.sub(re.escape("http://motherless.com/"), "", mlessvid);
  mlessvid = re.sub(re.escape("http://www.motherless.com/"), "", mlessvid);
  mlessvid = re.sub(re.escape("https://motherless.com/"), "", mlessvid);
  mlessvid = re.sub(re.escape("https://www.motherless.com/"), "", mlessvid);
  mlessvid = re.sub(re.escape("motherless.com/"), "", mlessvid);
  mlessvid = re.sub(re.escape("www.motherless.com/"), "", mlessvid);
  mlessvid = re.sub("^"+re.escape("/"), "", mlessvid);
  mlessvid = "http://motherless.com/"+mlessvid;
  mregex_text = re.escape("http://motherless.com/")+"([\w\/\?\&\=]+)";
  if(re.findall(mregex_text, mlessvid)):
   mlessvid = re.findall(mregex_text, mlessvid);
   mlessvid = "/"+mlessvid[0];
  mlessvidqstr = urlparse.parse_qs(urlparse.urlparse(mlessvid).query);
  mlessvidid = urlparse.urlparse(mlessvid).path.split("/");
  mlessgallist = [];
  if((re.match("^random", mlessvidid[1]) and len(mlessvidid)==2) or (re.match("^random", mlessvidid[1]) and len(mlessvidid)==3) and (re.match("^image", mlessvidid[2]) or re.match("^video", mlessvidid[2]))):
   geturls_text = geturls_opener.open("http://motherless.com"+mlessvid);
   mlessvid = geturls_text.geturl();
   if(re.findall(mregex_text, mlessvid)):
    mlessvid = re.findall(mregex_text, mlessvid);
    mlessvid = mlessvid[0];
    if(mtlessgetargs["verbose"]==True):
     print(mlessvid);
  if((re.match("^galleries", mlessvidid[1]) and len(mlessvidid)==4) or (re.match("^f", mlessvidid[1]) and re.match("^galleries", mlessvidid[2]) and len(mlessvidid)==4) or (re.match("^term", mlessvidid[1]) and re.match("^galleries", mlessvidid[2]) and len(mlessvidid)==4)):
   geturls_text = geturls_opener.open("http://motherless.com"+mlessvid+"?page=1");
   if(geturls_text.info().get("Content-Encoding")=="gzip" or geturls_text.info().get("Content-Encoding")=="deflate"):
    strbuf = StringIO.StringIO(geturls_text.read());
    gzstrbuf = gzip.GzipFile(fileobj=strbuf);
    out_text = gzstrbuf.read()[:];
   if(geturls_text.info().get("Content-Encoding")!="gzip" and geturls_text.info().get("Content-Encoding")!="deflate"):
    out_text = geturls_text.read()[:];
   out_text = re.sub(re.escape("http://motherless.com"), "", out_text);
   out_text = re.sub(re.escape("http://www.motherless.com"), "", out_text);
   out_text = re.sub(re.escape("https://motherless.com"), "", out_text);
   out_text = re.sub(re.escape("https://www.motherless.com"), "", out_text);
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
     out_text = re.sub(re.escape("http://motherless.com"), "", out_text);
     out_text = re.sub(re.escape("http://www.motherless.com"), "", out_text);
    regex_text = re.escape("")+"([\w\/]+)"+re.escape("\" class=\"img-container\" target=\"_self\">");
    post_text = re.findall(regex_text, out_text);
    numgal = len(post_text);
    curgal = 0;
    while(curgal<numgal):
     mlessgallist.append(post_text[curgal]);
     if(mtlessgetargs["verbose"]==True):
      print(post_text[curgal]);
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
   mlessvidqstr = urlparse.parse_qs(urlparse.urlparse(mlessvid).query);
   mlessvidid = urlparse.urlparse(mlessvid).path.split("/");
   mlessurllist = [];
   if((re.match("^G", mlessvidid[1]) and len(mlessvidid)==2) or (re.match("^H", mlessvidid[1]) and len(mlessvidid)==2) or (re.match("^V", mlessvidid[1]) and len(mlessvidid)==2) or (re.match("^live", mlessvidid[1]) and len(mlessvidid)==2) or (re.match("^g", mlessvidid[1]) and len(mlessvidid)==3) or (re.match("^u", mlessvidid[1]) and len(mlessvidid)==3) or (re.match("^term", mlessvidid[1]) and (re.match("^videos", mlessvidid[2]) or re.match("^images", mlessvidid[2])) and len(mlessvidid)==4) or (re.match("^f", mlessvidid[1]) and len(mlessvidid)==4 and (re.match("^videos", mlessvidid[3]) or re.match("^images", mlessvidid[3]))) or (re.match("^live", mlessvidid[1]) and len(mlessvidid)==3 and (re.match("^images", mlessvidid[2]) or re.match("^videos", mlessvidid[2]))) or (re.match("^images", mlessvidid[1]) and len(mlessvidid)==3 and (re.match("^favorited", mlessvidid[2]) or re.match("^viewed", mlessvidid[2]) or re.match("^commented", mlessvidid[2]) or re.match("^popular", mlessvidid[2]))) or (re.match("^videos", mlessvidid[1]) and len(mlessvidid)==3 and (re.match("^favorited", mlessvidid[2]) or re.match("^viewed", mlessvidid[2]) or re.match("^commented", mlessvidid[2]) or re.match("^popular", mlessvidid[2])))):
    addtvar = False;
    tvaradd = "";
    if(re.match("^u", mlessvidid[1]) and len(mlessvidid)==3):
     try:
      if(mlessvidqstr["t"][0]=="i" or mlessvidqstr["t"][0]=="v"):
       tvaradd = "&t="+mlessvidqstr["t"][0];
       addtvar = True;
     except KeyError:
      addtvar = False;
     except IndexError:
      addtvar = False;
    geturls_text = geturls_opener.open("http://motherless.com"+mlessvid+"?page=1"+tvaradd);
    if(geturls_text.info().get("Content-Encoding")=="gzip" or geturls_text.info().get("Content-Encoding")=="deflate"):
     strbuf = StringIO.StringIO(geturls_text.read());
     gzstrbuf = gzip.GzipFile(fileobj=strbuf);
     out_text = gzstrbuf.read()[:];
    if(geturls_text.info().get("Content-Encoding")!="gzip" and geturls_text.info().get("Content-Encoding")!="deflate"):
     out_text = geturls_text.read()[:];
    out_text = re.sub(re.escape("http://motherless.com"), "", out_text);
    out_text = re.sub(re.escape("http://www.motherless.com"), "", out_text);
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
      geturls_text = geturls_opener.open("http://motherless.com"+mlessvid+"?page="+str(curpage)+tvaradd);
      if(geturls_text.info().get("Content-Encoding")=="gzip" or geturls_text.info().get("Content-Encoding")=="deflate"):
       strbuf = StringIO.StringIO(geturls_text.read());
       gzstrbuf = gzip.GzipFile(fileobj=strbuf);
       out_text = gzstrbuf.read()[:];
      if(geturls_text.info().get("Content-Encoding")!="gzip" and geturls_text.info().get("Content-Encoding")!="deflate"):
       out_text = geturls_text.read()[:];
     out_text = re.sub(re.escape("http://motherless.com"), "", out_text);
     out_text = re.sub(re.escape("http://www.motherless.com"), "", out_text);
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
      if(mtlessgetargs["verbose"]==True):
       print(post_text[cururl]);
      cururl = cururl + 1;
     curpage = curpage + 1;
   if((re.match("^G", mlessvidid[1]) and len(mlessvidid)==3 and re.match("([0-9A-F]+)", mlessvidid[2])) or (re.match("^g", mlessvidid[1]) and len(mlessvidid)==4) or (len(mlessvidid)==2 and re.match("([0-9A-F]+)", mlessvidid[1]))):
    mlessurllist.append(mlessvid);
   numlist = len(mlessurllist);
   curlurl = 0;
   mlessoutlist = [];
   while(curlurl<numlist):
    skiplnk = False;
    try:
     geturls_text = geturls_opener.open("http://motherless.com"+mlessurllist[curlurl]);
    except urllib2.HTTPError:
     skiplnk = True;
    if(skiplnk==False):
     if(geturls_text.info().get("Content-Encoding")=="gzip" or geturls_text.info().get("Content-Encoding")=="deflate"):
      strbuf = StringIO.StringIO(geturls_text.read());
      gzstrbuf = gzip.GzipFile(fileobj=strbuf);
      subout_text = gzstrbuf.read()[:];
     if(geturls_text.info().get("Content-Encoding")!="gzip" and geturls_text.info().get("Content-Encoding")!="deflate"):
      subout_text = geturls_text.read()[:];
     subout_text = re.sub(re.escape("http://motherless.com"), "", subout_text);
     subout_text = re.sub(re.escape("http://www.motherless.com"), "", subout_text);
     subout_text = re.sub(re.escape("http://motherless.com"), "", subout_text);
     subout_text = re.sub(re.escape("http://www.motherless.com"), "", subout_text);
     regex_title = re.escape("<title>")+"(.*)"+re.escape("</title>");
     title_text = re.findall(regex_title, subout_text);
     mlesstitle = re.sub(re.escape(" - MOTHERLESS.COM"), "", title_text[0]);
     regex_thumb = re.escape("src=&quot;")+"(.*)"+re.escape("&quot;");
     thumb_text = re.findall(regex_thumb, subout_text);
     mlessthumb = thumb_text[0];
     regex_text = re.escape("__fileurl = '")+"(.*)"+re.escape("';");
     post_text = re.findall(regex_text, subout_text);
     regex_img = re.escape("<meta property=\"og:image\" content=\"")+"(.*)"+re.escape("\">");
     img_text = re.findall(regex_img, subout_text);
     mlessimg = img_text[0];
     regex_mediatype = re.escape("__mediatype = '")+"(.*)"+re.escape("',");
     mediatype_text = re.findall(regex_mediatype, subout_text);
     regex_altimg = re.escape("<link rel=\"image_src\" type=\"image/")+"(.*)"+re.escape("\" href=\"")+"(.*)"+re.escape("\">");
     altimg_text = re.findall(regex_altimg, subout_text);
     mlessaltimg = altimg_text[0][1];
     regex_usrname = re.escape("<a href=\"/u/")+"([\w]+)"+re.escape("\" class=\"pop plain thumb-member-link-uploads\">Uploads</a>");
     usrname_text = re.findall(regex_usrname, subout_text);
     mlessusrname = usrname_text[0];
     mlessid = re.sub("^"+re.escape("/"), "", mlessurllist[curlurl]);
     mlesspurl = "http://motherless.com"+mlessurllist[curlurl];
     regex_numviews = re.escape("<strong>Views</strong>")+"\n+\t+([^\t]+)\t+"+re.escape("</h2>");
     numviews_text = re.findall(regex_numviews, subout_text);
     mlessnumviews = numviews_text[0];
     mlessnumviews = re.sub(re.escape(","), "", mlessnumviews);
     regex_numfavs = re.escape("<strong>Favorited</strong>")+"\n+\t+([^\t]+)\t+"+re.escape("</h2>");
     numfavs_text = re.findall(regex_numfavs, subout_text);
     mlessnumfavs = numfavs_text[0];
     mlessnumfavs = re.sub(re.escape(","), "", mlessnumfavs);
     ''' some good regex "!-%'-?A-~ " "!-%'-?A-~ \<\>\"\'\@\#" '''
     regex_postdata = re.escape("<div class=\"media-comment-contents\">")+"\n\t+"+re.escape("<h4>")+"\n\t+"+re.escape("<a href=\"/m/")+"([\w]+)"+re.escape("\" class=\"pop plain\" target=\"_blank\">")+"\n\t+([^\t]+)\t+"+re.escape("</a>")+"\n\t+"+re.escape("</h4>")+"\n\t+"+re.escape("<div class=\"media-comment-meta\">")+"\n\t+([^\t]+)\t+"+re.escape("</div>")+"\n\t+"+re.escape("<div style=\"text-align: justify;\">")+"\n\t+([^\t]+)\t+"+re.escape("</div>");
     postdata_text = re.findall(regex_postdata, subout_text);
     numpost = len(postdata_text);
     regex_servsecs = re.escape("Served by web")+"([0-9]+)"+re.escape(" in ")+"([0-9\.]+)"+re.escape(" seconds");
     servsecs_text = re.findall(regex_servsecs, subout_text);
     servname = "web"+servsecs_text[0][0];
     servsecs = float(servsecs_text[0][1]);
     curpost = 0;
     mlesspostlist = [];
     ''' From Amber @ http://stackoverflow.com/a/9662362 '''
     TAG_RE = re.compile(r'<[^>]+>');
     while(numpost>0 and curpost<numpost):
      newpostext = re.sub(re.escape("<br>"), "\n", postdata_text[curpost][3]);
      newpostext = re.sub(re.escape("<br/>"), "\n", newpostext);
      newpostext = re.sub(re.escape("<br />"), "\n", newpostext);
      newpostext = TAG_RE.sub('', newpostext);
      newpostext = re.sub(re.escape("/")+"([\w\/]+)", r"http://motherless.com/\1", newpostext);
      mlesspostlist.append({"username": postdata_text[curpost][0], "avatar": "http://avatars.motherlessmedia.com/avatars/member/"+postdata_text[curpost][0]+".jpg", "smallavatar": "http://avatars.motherlessmedia.com/avatars/member/"+postdata_text[curpost][0]+"-small.jpg", "post": newpostext});
      curpost = curpost + 1;
     if(post_text>0):
      mlesslink = post_text[0];
      mlessext = os.path.splitext(urlparse.urlparse(mlesslink).path)[1];
      mlessext = mlessext.replace(".", "");
      mlessext = mlessext.lower();
      if(mtlessgetargs["id"]==False):
       mlessfname = urlparse.urlsplit(mlesslink).path.split("/")[-1];
      if(mtlessgetargs["id"]==True):
       mlessfname = re.sub(re.escape("/"), "_", mlessid)+"."+mlessext;
      if(not mlessext=="mp4" and not mlessext=="flv"):
       imginfo = {};
       regex_ii_dimensions = re.escape("style=\"width: ")+"([0-9]+)"+re.escape("px; height: ")+"([0-9]+)"+re.escape("px; border: none;\"");
       post_ii_dimensions = re.findall(regex_ii_dimensions, subout_text);
       post_ii_width = post_ii_dimensions[0][0];
       post_ii_height = post_ii_dimensions[0][1];
       imginfo = {"width": int(post_ii_height), "height": int(post_ii_width), "views": int(mlessnumviews), "favorites": int(mlessnumfavs)};
      if(mlessext=="mp4" or mlessext=="flv"):
       vidinfo = {};
       mlesslink = mlesslink+"?start=0";
       regex_vi_file = re.escape("\"file\"      : \"")+"(.*)"+re.escape("\",");
       post_vi_file = re.findall(regex_vi_file, subout_text);
       regex_vi_image = re.escape("\"image\"     : \"")+"(.*)"+re.escape("\",");
       post_vi_image = re.findall(regex_vi_image, subout_text);
       regex_vi_height = re.escape("\"height\"    : ")+"([0-9]+)"+re.escape(",");
       post_vi_height = re.findall(regex_vi_height, subout_text);
       regex_vi_width = re.escape("\"width\"     : ")+"([0-9]+)"+re.escape(",");
       post_vi_width = re.findall(regex_vi_width, subout_text);
       regex_vi_filethumb = re.escape("\"file\": ")+"(.*)"+re.escape(",");
       post_vi_filethumb = re.findall(regex_vi_filethumb, subout_text);
       regex_vi_kind = re.escape("\"kind\": \"")+"(.*)"+re.escape("\"");
       post_vi_kind = re.findall(regex_vi_kind, subout_text);
       vidinfo = {"file": post_vi_file[0], "image": post_vi_image[0], "width": int(post_vi_width[0]), "height": int(post_vi_height[0]), "views": int(mlessnumviews), "favorites": int(mlessnumfavs), "filethumb": post_vi_filethumb[0], "thumbstrip": "http://thumbs.motherlessmedia.com/thumbs/"+mlessid+"-strip.jpg", "kind": post_vi_kind[0]};
      if(mtlessgetargs["verbose"]==True):
       print(mlesslink);
      mlesslistitms = {};
      mlesslistitms.update({"id": mlessid});
      mlesslistitms.update({"title": mlesstitle});
      mlesslistitms.update({"format": mlessext});
      mlesslistitms.update({"filename": mlessfname});
      mlesslistitms.update({"thumbnail": mlessthumb});
      mlesslistitms.update({"servername": servname});
      mlesslistitms.update({"servingtime": servsecs});
      mlesslistitms.update({"mediatype": mediatype_text[0]});
      if(not mlessext=="mp4" and not mlessext=="flv"):
       mlesslistitms.update({"vidpic": mlesslink});
       mlesslistitms.update({"type": "image"});
       mlesslistitms.update({"info": imginfo});
       mlesslistitms.update({"dimensions": str(imginfo["width"])+"x"+str(imginfo["height"])});
       mlesslistitms.update({"width": imginfo["width"]});
       mlesslistitms.update({"height": imginfo["height"]});
       mlesslistitms.update({"views": imginfo["views"]});
       mlesslistitms.update({"favorites": imginfo["favorites"]});
      if(mlessext=="mp4" or mlessext=="flv"):
       mlesslistitms.update({"vidpic": mlessimg});
       mlesslistitms.update({"type": "video"});
       mlesslistitms.update({"info": vidinfo});
       mlesslistitms.update({"dimensions": str(vidinfo["width"])+"x"+str(vidinfo["height"])});
       mlesslistitms.update({"width": vidinfo["width"]});
       mlesslistitms.update({"height": vidinfo["height"]});
       mlesslistitms.update({"views": vidinfo["views"]});
       mlesslistitms.update({"favorites": vidinfo["favorites"]});
      mlesslistitms.update({"username": mlessusrname});
      mlesslistitms.update({"avatar": "http://avatars.motherlessmedia.com/avatars/member/"+mlessusrname+".jpg"});
      mlesslistitms.update({"smallavatar": "http://avatars.motherlessmedia.com/avatars/member/"+mlessusrname+"-small.jpg"});
      mlesslistitms.update({"posts": mlesspostlist});
      mlesslistitms.update({"pageurl": mlesspurl});
      mlesslistitms.update({"url": mlesslink});
      mlessoutlist.append(mlesslistitms);
    if(curlurl<(numlist - 1)):
     time.sleep(per_url_sleep);
    curlurl = curlurl + 1;
   if(curusrgal<(numusrgal - 1)):
    time.sleep(per_gal_sleep);
   curusrgal = curusrgal + 1;
  cururlarg = cururlarg + 1;
 return mlessoutlist;
if(__name__ == "__main__"):
 mtlesslinks = motherless_dl();
 mtlesslncount = len(mtlesslinks);
 mtlesscurln = 0;
 while(mtlesscurln<mtlesslncount):
  if(getargs.get_id==True):
   print(mtlesslinks[mtlesscurln]["id"]);
  if(getargs.get_title==True):
   print(mtlesslinks[mtlesscurln]["title"]);
  if(getargs.get_posts==True):
   numpost = len(mtlesslinks[mtlesscurln]["posts"]);
   curpost = 0;
   mlesspostlist = [];
   while(numpost>0 and curpost<numpost):
    print(mtlesslinks[mtlesscurln]["posts"][curpost]["username"]+": "+mtlesslinks[mtlesscurln]["posts"][curpost]["post"]);
    curpost = curpost + 1;
  if(getargs.get_format==True):
   print(mtlesslinks[mtlesscurln]["format"]);
  if(getargs.get_type==True):
   print(mtlesslinks[mtlesscurln]["type"]);
  if(getargs.get_filename==True):
   print(mtlesslinks[mtlesscurln]["filename"]);
  if(getargs.get_thumbnail==True):
   print(mtlesslinks[mtlesscurln]["thumbnail"]);
   if(mtlesslinks[mtlesscurln]["format"]=="mp4" or mtlesslinks[mtlesscurln]["format"]=="flv"):
    print(mtlesslinks[mtlesscurln]["vidpic"]);
  if(getargs.get_username==True):
   print(mtlesslinks[mtlesscurln]["username"]);
  if(getargs.get_pageurl==True):
   print(mtlesslinks[mtlesscurln]["pageurl"]);
  if(getargs.get_bbcode==True):
   print("[URL="+mtlesslinks[mtlesscurln]["pageurl"]+"][IMG]"+mtlesslinks[mtlesscurln]["thumbnail"]+"[/IMG][/URL]");
  if(getargs.get_html==True):
   print("<a href=\""+mtlesslinks[mtlesscurln]["pageurl"]+"\"><img src=\""+mtlesslinks[mtlesscurln]["thumbnail"]+"\"></a>");
  if(getargs.get_dimensions==True):
   print(mtlesslinks[mtlesscurln]["dimensions"]);
  if(getargs.get_width==True):
   print(str(mtlesslinks[mtlesscurln]["width"]));
  if(getargs.get_height==True):
   print(str(mtlesslinks[mtlesscurln]["height"]));
  if(getargs.get_views==True):
   print(mtlesslinks[mtlesscurln]["views"]);
  if(getargs.get_favorites==True):
   print(mtlesslinks[mtlesscurln]["favorites"]);
  if(getargs.get_url==True or (getargs.get_id==False and getargs.get_title==False and getargs.get_posts==False and getargs.get_format==False and getargs.get_filename==False and getargs.get_thumbnail==False and getargs.get_username==False and getargs.get_pageurl==False and getargs.get_bbcode==False and getargs.get_html==False and getargs.get_dimensions==False and getargs.get_width==False and getargs.get_height==False and getargs.get_views==False and getargs.get_favorites==False and getargs.get_type==False)):
   print(mtlesslinks[mtlesscurln]["url"]);
  mtlesscurln = mtlesscurln + 1;
