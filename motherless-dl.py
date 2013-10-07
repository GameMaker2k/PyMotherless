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

    $FileInfo: motherless-dl.py - Last Update: 10/07/2013 Ver. 1.5.0 RC 1 - Author: cooldude2k $
'''

import re, os, sys, urllib, urllib2, cookielib, StringIO, gzip, time, datetime, argparse, urlparse;

__version_info__ = (1, 5, 0, "RC 1");
if(__version_info__[3]!=None):
 __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2])+" "+str(__version_info__[3]);
if(__version_info__[3]==None):
 __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2]);

parser = argparse.ArgumentParser();
parser.add_argument("url", nargs="*", help="motherless url");
parser.add_argument("--version", action='store_true', help="print program version and exit");
parser.add_argument("--update", action='store_true', help="update this program to latest version. Make sure that you have sufficient permissions (run with sudo if needed)");
parser.add_argument("--dump-user-agent", action='store_true', help="display the current browser identification");
parser.add_argument("--user-agent", nargs="?", default="Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0", help="specify a custom user agent");
parser.add_argument("--referer", nargs="?", default="http://motherless.com/", help="specify a custom referer, use if the video access");
parser.add_argument("--get-url", action='store_true', help="simulate, quiet but print URL");
parser.add_argument("--get-title", action='store_true', help="simulate, quiet but print title");
parser.add_argument("--get-id", action='store_true', help="simulate, quiet but print id");
parser.add_argument("--get-thumbnail", action='store_true', help="simulate, quiet but print thumbnail URL");
parser.add_argument("--get-filename", action='store_true', help="simulate, quiet but print output filename");
parser.add_argument("--get-format", action='store_true', help="simulate, quiet but print output format");
parser.add_argument("--verbose", action='store_true', help="print various debugging information");
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
   regex_altimg = re.escape("<link rel=\"image_src\" type=\"image/")+"(.*)"+re.escape("\" href=\"")+"(.*)"+re.escape("\">");
   altimg_text = re.findall(regex_altimg, subout_text);
   mlessaltimg = altimg_text[0][1];
   mlessid = re.sub("^"+re.escape("/"), "", mlessurllist[curlurl]);
   if(post_text>0):
    mlesslink = post_text[0];
    mlessext = os.path.splitext(urlparse.urlparse(mlesslink).path)[1];
    mlessext = mlessext.replace(".", "");
    mlessext = mlessext.lower();
    mlessfname = urlparse.urlsplit(mlesslink).path.split('/')[-1];
    if(not mlessext=="mp4" and not mlessext=="flv"):
     imginfo = {};
     regex_ii_dimensions = re.escape("style=\"width: ")+"([0-9]+)"+re.escape("px; height: ")+"([0-9]+)"+re.escape("px; border: none;\"");
     post_ii_dimensions = re.findall(regex_ii_dimensions, subout_text);
     post_ii_width = post_ii_dimensions[0][0];
     post_ii_height = post_ii_dimensions[0][1];
     imginfo = {"height": int(post_ii_width), "width": int(post_ii_height)};
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
     vidinfo = {"file": post_vi_file[0], "image": post_vi_image[0], "height": int(post_vi_height[0]), "width": int(post_vi_width[0]), "filethumb": post_vi_filethumb[0], "kind": post_vi_kind[0]};
    if(getargs.get_id==True):
     print(mlessid);
    if(getargs.get_title==True):
     print(mlesstitle);
    if(getargs.get_format==True):
     print(mlessext);
    if(getargs.get_filename==True):
     print(mlessfname);
    if(getargs.get_thumbnail==True):
     print(mlessthumb);
     if(mlessext=="mp4" or mlessext=="flv"):
      print(mlessimg);
    if(getargs.get_url==True or (getargs.get_id==False and getargs.get_title==False and getargs.get_format==False and getargs.get_filename==False and getargs.get_thumbnail==False)):
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
