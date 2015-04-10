#!/usr/bin/env python
# coding=utf-8
__author__ = 'smy'
"""
the model for download file
"""
class DownloadFileInfo(object):

    def __init__(self,file_name,file_size):
        self.file_name = file_name
        if file_size<=0 or file_size==None:
            self.file_size = NO_SIZE
        else:
            self.file_size = FileSize(file_size)

    def get_filenamme(self):
        return self.file_name

    def get_filesize(self):
        return self.file_size

class FileSize(object):

    def __init__(self,size,unit="K"):
        self.size_kb = max(size,0)
        if unit!='K' and unit!='M' and unit!='G':
            raise Exception("the file size unit muse be one of K,M and G")
        if size<=0:
            self.size = 0
        elif size>1024 and size<1024*1024:
            self.size = (float)(size)/1024
            self.unit = "M"
        elif size>1024*1024:
            self.size = float(size)/(1024*1024)
            self.unit = "G"

    def __str__(self):
        return str(self.size)+self.unit

    """return the size by KB"""
    def to_kb(self):
      return self.size_kb

NO_SIZE = FileSize(-1)
