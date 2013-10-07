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

    $FileInfo: get_ylp.py - Last Update: 10/07/2013 Ver. 1.0.5 RC 6 - Author: cooldude2k $
'''

import re, os, sys, urllib, urllib2, cookielib, StringIO, gzip, time, datetime, argparse, urlparse;

fakeua = "Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0"";
geturls_cj = cookielib.CookieJar();
geturls_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(geturls_cj));
geturls_opener.addheaders = [("Referer", "http://www.google.com/search?q=younglegalporn"), ("User-Agent", fakeua), ("Accept-Encoding", "gzip, deflate"), ("Accept-Language", "en-US,en-CA,en-GB,en-UK,en-AU,en-NZ,en-ZA,en;q=0.5"), ("Accept-Charset", "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7"), ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"), ("Connection", "close")];
print("0 Reading URL: http://photos.younglegalporn.com/");
geturls_text = geturls_opener.open("http://photos.younglegalporn.com/");
if(geturls_text.info().get("Content-Encoding")=="gzip" or geturls_text.info().get("Content-Encoding")=="deflate"):
 strbuf = StringIO.StringIO(geturls_text.read());
 gzstrbuf = gzip.GzipFile(fileobj=strbuf);
 out_text = gzstrbuf.read()[:];
if(geturls_text.info().get("Content-Encoding")!="gzip" and geturls_text.info().get("Content-Encoding")!="deflate"):
 out_text = geturls_text.read()[:];
regex_text = re.escape("<li><a href=\"http://photos.younglegalporn.com/")+"([a-fA-F0-9]{8})"+re.escape("/")+"([a-zA-Z0-9]{14})"+re.escape("/\"><img title=\"");
post_text = re.findall(regex_text, out_text);
wait_time1 = 4;
wait_time2 = wait_time1 + 4;
i = 0;
il = len(post_text);
print("0 Found "+str(il)+" Image Galleries.");
if(not os.path.exists("./younglegalporn/")):
 print("0 Making Directory: ./younglegalporn/");
 os.mkdir("./younglegalporn/");
while(i < il):
 if(not os.path.exists("./younglegalporn/"+post_text[i][0]+"/")):
  print(str(i+1)+" Making Directory: ./younglegalporn/"+post_text[i][0]+"/");
  os.mkdir("./younglegalporn/"+post_text[i][0]+"/");
 getsuburls_cj = geturls_cj;
 getsuburls_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(getsuburls_cj));
 getsuburls_opener.addheaders = [("Referer", "http://photos.younglegalporn.com/"), ("User-Agent", fakeua), ("Accept-Encoding", "gzip, deflate"), ("Accept-Language", "en-US,en-CA,en-GB,en-UK,en-AU,en-NZ,en-ZA,en;q=0.5"), ("Accept-Charset", "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7"), ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"), ("Connection", "close")];
 print(str(i+1)+" Start Downloading Image Gallery: "+str(i+1)+" of "+str(il));
 print(str(i+1)+" Start Downloading Image Gallery: "+post_text[i][0]);
 print(str(i+1)+" Reading Image Gallery: http://photos.younglegalporn.com/"+post_text[i][0]+"/"+post_text[i][1]+"/");
 getsuburls_text = getsuburls_opener.open("http://photos.younglegalporn.com/"+post_text[i][0]+"/"+post_text[i][1]+"/");
 if(getsuburls_text.info().get("Content-Encoding")=="gzip" or getsuburls_text.info().get("Content-Encoding")=="deflate"):
  substrbuf = StringIO.StringIO(getsuburls_text.read());
  gzsubstrbuf = gzip.GzipFile(fileobj=substrbuf);
  subout_text = gzsubstrbuf.read()[:];
 if(getsuburls_text.info().get("Content-Encoding")!="gzip" and getsuburls_text.info().get("Content-Encoding")!="deflate"):
  subout_text = getsuburls_text.read()[:];
 subout_text = subout_text.replace("://", ":///");
 subout_text = subout_text.replace("//", "/");
 subout_text = subout_text.replace("//pics/", "/pics/");
 subout_text = subout_text.replace("/pics//", "/pics/");
 subregex_text = re.escape("<a href=\"http://content1.sexforsure.com/")+"([0-9]+)"+re.escape("/")+"([0-9]+)"+re.escape("/")+"([0-9]+)"+re.escape("/")+"([0-9]+)"+re.escape("/pics/")+"([0-9]+)"+re.escape(".jpg\"><img src=\"");
 subpost_text = re.findall(subregex_text, subout_text);
 if(len(subpost_text)==0):
  subregex_text = re.escape("<a href=\"http://content1.sexforsure.com/")+"([0-9]+)"+re.escape("/")+"([0-9]+)"+re.escape("/")+"([0-9]+)"+re.escape("/")+"([0-9]+)"+re.escape("//pics/")+"([0-9]+)"+re.escape(".jpg\"><img src=\"");
  subpost_text = re.findall(subregex_text, subout_text);
 subi = int(subpost_text[0][4]) - 1;
 subil = int(subpost_text[-1][4]);
 print(str(i+1)+" Found "+subpost_text[-1][4]+" JPEG Images.");
 while(subi < subil):
  getsub2xurls_cj = geturls_cj;
  getsub2xurls_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(getsub2xurls_cj));
  getsub2xurls_opener.addheaders = [("Referer", "http://photos.younglegalporn.com/"+post_text[i][0]+"/"+post_text[i][1]+"/"), ("User-Agent", fakeua), ("Accept-Encoding", "gzip, deflate"), ("Accept-Language", "en-US,en-CA,en-GB,en-UK,en-AU,en-NZ,en-ZA,en;q=0.5"), ("Accept-Charset", "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7"), ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"), ("Connection", "close")];
  print(str(i+1)+","+str(subi+1)+" Start Downloading Image File: "+str(subi+1)+" of "+str(subil));
  print(str(i+1)+","+str(subi+1)+" Downloading Image: http://content1.sexforsure.com/"+subpost_text[subi][0]+"/"+subpost_text[subi][1]+"/"+subpost_text[subi][2]+"/"+subpost_text[subi][3]+"/pics/"+subpost_text[subi][4]+".jpg");
  getsub2xurls_text = getsub2xurls_opener.open("http://content1.sexforsure.com/"+subpost_text[subi][0]+"/"+subpost_text[subi][1]+"/"+subpost_text[subi][2]+"/"+subpost_text[subi][3]+"/pics/"+subpost_text[subi][4]+".jpg");
  print(str(i+1)+","+str(subi+1)+" Finished Downloading Image: http://content1.sexforsure.com/"+subpost_text[subi][0]+"/"+subpost_text[subi][1]+"/"+subpost_text[subi][2]+"/"+subpost_text[subi][3]+"/pics/"+subpost_text[subi][4]+".jpg");
  print(str(i+1)+","+str(subi+1)+" Saving File: ./younglegalporn/"+post_text[i][0]+"/"+subpost_text[subi][4]+".jpg");
  jpegf = open("./younglegalporn/"+post_text[i][0]+"/"+subpost_text[subi][4]+".jpg", "wb");
  jpegf.write(getsub2xurls_text.read());
  jpegf.close();
  print(str(i+1)+","+str(subi+1)+" Finished Saving File: ./younglegalporn/"+post_text[i][0]+"/"+subpost_text[subi][4]+".jpg");
  time.sleep(wait_time1);
  subi = subi + 1;
 print(str(i+1)+" Finished Downloading Image Gallery: "+post_text[i][0]);
 time.sleep(wait_time2);
 i = i + 1;
 if(i < il):
  print(str(i+1)+" Next Image Gallery Download: "+post_text[i][0]);
print("Full Download Completed Successfully");
