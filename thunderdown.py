#!/usr/bin/env python
# coding=utf-8
__author__ = 'smy'
import  download_request
import download_thread
import settings
import math

"""
a class for download file from network
"""
class ThunderDown:
    def __init__(self,url):
        self.downloadUrl = url
        self.__initThreads__()

    def __initThreads__(self):
        self.downloadThreads = []

        # get the file size
        fileSize = int(download_request.getNetFileSize(self.downloadUrl))
        print 'fileSize:',fileSize

        # create the download threads
        thread_capacity = settings.DEFAULT_THREAD_CAPACITY
        thread_size = int(min( math.ceil(fileSize/thread_capacity),settings.MAX_THREAD_SIZE))
        if(thread_size == settings.MAX_THREAD_SIZE):
            thread_capacity = math.ceil(fileSize/thread_size) # recalculate the thread download capacity

        print 'thread_size:',thread_size
        startPos = 0
        for i in range(thread_size):
            normalEndPos = startPos + thread_capacity - 1
            endPos = min(normalEndPos,fileSize-1)
            downloadThread = download_thread.DownloadThread(self.downloadUrl,startPos,endPos)
            startPos += thread_capacity
            self.downloadThreads.append(downloadThread)

    """start download file"""
    def startDownload(self):
        for downloadThread in self.downloadThreads:
            downloadThread.start()

    """pause download to wait restart"""
    def pauseDownload(self):
        pass

    """cancel the download anyway"""
    def cancelDownload(self):
        pass

    """restart the paused download"""
    def restartDownload(self):
        pass

    """invoked when the download finished"""
    def onFinish(self):
        pass

# test the ThunderDown
if __name__ == '__main__':
    ThunderDown("https://github.com/mingyangShang/csdn_blog_visitor/blob/master/csdn_blog_vistor/visiting.pyc?raw=true").startDownload()



