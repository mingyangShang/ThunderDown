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

    def set_output(self,conn_output):
        self.output = conn_output

    def run(self):
        #start a urlrequest
        print self.name,"start"
        if not self.output:
            raise Exception("output must be set before thread run")
        self.request.set_output(self.output)
        if self.request:
            self.request.start()
        else:
            print 'request is None'
        print self.name,'finish'

    def get_completed_len(self):
        return self.request.total_len

    def getTaskQueue(self):
        return self.__task_queue__
