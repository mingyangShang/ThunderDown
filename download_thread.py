#!/usr/bin/env python
# coding=utf-8
__author__ = 'smy'

import threading
import settings
import download_request

from download_request import DownloadRequest

__author__ = 'smy'

"""
download thread to download the resources from internet
"""
class DownloadThread(threading.Thread):
    lock = threading.Lock()

    def __init__(self,url,startPos,endPos):
        threading.Thread.__init__(self)

        self.downloadUrl = url
        self.startPos = int(startPos)
        self.endPos = int(endPos)

        self.total_len = 0

        self.request = DownloadRequest(url,startPos,endPos)

    def run(self):
        #start a urlrequest
        print self.name,"start","startPos:",self.startPos
        if not self.output:
            raise Exception("output must be set before thread run")
        if self.request:
            response = self.request.start()
            if not response:
                raise Exception("response is null,so the download can\' be done")
            self.read(response)
        else:
            print 'request is None'
        print self.name,'finish'

    def get_completed_len(self):
        return self.request.total_len

    def set_output(self,conn_output):
        self.output = conn_output

    """read data from url connection"""
    def read(self,response):
         data = response.read(settings.BUFFER_SIZE)
         while data:
             self.save(data)
             if self.endPos-self.startPos+1<=self.total_len:
                break
             elif self.endPos-self.startPos+1<self.total_len+settings.BUFFER_SIZE:
                data = response.read(self.endPos-self.startPos+1-self.total_len)
                self.save(data)
                break
             else:
                 data = response.read(settings.BUFFER_SIZE)

    """save data to local file"""
    def save(self,data):
        DownloadThread.lock.acquire()
        print self.name,'seek:',self.startPos + self.total_len
        self.output.seek(self.startPos+self.total_len,0)
        print self.name,'write'
        self.output.write(data)
        self.total_len += len(data)
        DownloadThread.lock.release()