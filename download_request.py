#!/usr/bin/env python
# coding=utf-8
__author__ = 'smy'

import urllib
import urllib2
import settings
__author__ = 'smy'

"""
download request that implements request to url,read data from network and save data to local,
"""

class DownloadRequest():
    def __init__(self,url,startPos,endPos):
        self.downloadUrl = url
        self.startPos = startPos
        self.endPos = endPos

    def start(self):
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
        print data
        pass


"""get the internet file's size"""
def getNetFileSize(url):
    try:
        conn = urllib2.urlopen(url,None,settings.TIMEOUT)
        return conn.info()['Content-Length']
    finally:
        if conn:
           conn.close()
    return None