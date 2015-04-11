#!/usr/bin/env python
# coding=utf-8
__author__ = 'smy'

import urllib
import urllib2
import threading
import settings
import download_file_info
__author__ = 'smy'

"""
download request that implements request to url,read data from network and save data to local,
"""

class DownloadRequest(object):
    def __init__(self,url,startPos,endPos):
        self.downloadUrl = url
        self.startPos = int(startPos)
        self.endPos = int(endPos)


    def start(self):
        request = urllib2.Request(self.downloadUrl)
        request.add_header('Range','bytes=%s-%s' %(self.startPos,self.endPos)) # key point:add the range info to http header
        try:
            reader = urllib2.urlopen(request,None,settings.TIMEOUT)
            return reader
        except urllib2.HTTPError,e:
            print 'httperror:',e.code
            return None
        except urllib2.URLError,e:
            print 'urlerror:',e.message
            return None
        except Exception,e:
            print 'error:',e.message
            return None
        else:
            print 'succeed'
        finally:
            print 'completed'

"""get the internet file's info"""
def get_netfile_info(url):
    try:
        # conn = urllib2.urlopen(url,None,settings.TIMEOUT)
        request = urllib2.Request(url)
        request.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36")
        conn = urllib2.urlopen(request)
        # file size，count by kb
        if conn.info().has_key("Content-Length"):
            length = int(conn.info()['Content-Length'])
        else:
            length = 0
        # file name
        print 'info:',conn.info().dict
        if conn.info().has_key("Content-Disposition"):
            content_disposition = conn.info()['Content-Disposition']
            name = content_disposition[content_disposition.index("\"")+1:content_disposition.rindex("\"")]
        else:
            name = url[url.rindex("/")+1:url.rindex("?")]

        file_info = download_file_info.DownloadFileInfo(name,length)
        return file_info
    except urllib2.HTTPError,e:
        print 'httperror:',e.code
    except urllib2.URLError,e:
        print 'urlerror:',e.message
    except Exception,e:
        print 'error:',e.message
    else:
        if conn:
           conn.close()
    return None