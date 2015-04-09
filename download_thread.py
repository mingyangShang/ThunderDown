#!/usr/bin/env python
# coding=utf-8
__author__ = 'smy'

import threading
import download_request

from download_request import DownloadRequest

__author__ = 'smy'

"""
download thread to download the resources from internet
"""
class DownloadThread(threading.Thread):

    thread_id = 0;
    __task_queue__ = [] # the blocking task queue

    def __init__(self,url,startPos,endPos):
        threading.Thread.__init__(self)
        # self.setDaemon(True)
        # self.setName("thread "+str(self.thread_id))
        # self.thread_id += 1

        self.downloadUrl = url
        self.startPos = startPos
        self.endPos = endPos

        self.request = DownloadRequest(url,startPos,endPos)

    def run(self):
        #start a urlrequest
        print self.name,"start"
        if self.request:
            self.request.start()
        else:
            print 'request is None'
        print self.name,'finish'
        #write to file

    def getTaskQueue(self):
        return self.__task_queue__
