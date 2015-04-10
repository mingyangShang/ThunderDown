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
        self.startPos = startPos
        self.endPos = endPos
        self.total_len = 0

    def start(self):
        if not self.output:
            raise Exception("the requesy must be set output")
        request = urllib2.Request(self.downloadUrl)
        request.add_header('Range','bytes=%s-%s' %(self.startPos,self.endPos)) # key point:add the range info to http header
        try:
            reader = urllib2.urlopen(request,None,settings.TIMEOUT)
            data = reader.read(settings.BUFFER_SIZE)
            while data:
                self.__saveData__(data)
                data = reader.read(settings.BUFFER_SIZE)
        except urllib2.HTTPError,e:
            print 'httperror:',e.code
        except urllib2.URLError,e:
            print 'urlerror:',e.message
        else:
            print 'succeed'
        finally:
            print 'completed'

    def __saveData__(self,data):
        # thread_lock = threading.Lock()
        # thread_lock.acquire()
        self.output.seek(self.startPos+self.total_len)
        print "start",str(self.startPos),"total:",self.total_len
        self.output.write(data)
        self.total_len += len(data)
        # thread_lock.release()

    def set_output(self,output):
        self.output = output




"""get the internet file's info"""
def get_netfile_info(url):
    try:
        conn = urllib2.urlopen(url,None,settings.TIMEOUT)
        # file size，count by kb
        if conn.info().has_key("Content-Length"):
            length = int(conn.info()['Content-Length'])
        else:
            length = 0

        # file name
        if conn.info().has_key("Content-Disposition"):
            name = conn.info()['Content-Disposition']
        else:
            name = url[url.rindex("/")+1:url.rindex("?")]

        file_info = download_file_info.DownloadFileInfo(name,length)
        return file_info
    finally:
        if conn:
           conn.close()
    return None