#!/usr/bin/env python
# coding=utf-8
__author__ = 'smy'
import threading
import  download_request
import download_thread
import download_file_info
import settings
import math
import os

"""
a class for download file from network
"""
class ThunderDown:
    def __init__(self,url):
        self.downloadUrl = url
        self.file_info = download_request.get_netfile_info(self.downloadUrl)
        if not self.file_info:
            raise Exception('sorry,download can\'t start because resources is unreachable')
        self.file_abspath = self.generate_file_name()
        self.lock = threading.Lock()
        self.__initThreads__()

    def __initThreads__(self):
        self.downloadThreads = []

        if self.file_info.file_size == download_file_info.NO_SIZE:
            thread_size = settings.MAX_THREAD_SIZE
            thread_capacity = settings.DEFAULT_THREAD_CAPACITY
        else:
            thread_capacity = settings.DEFAULT_THREAD_CAPACITY
            thread_size = int(min( math.ceil(self.file_info.file_size.to_kb()/float(thread_capacity)),settings.MAX_THREAD_SIZE))
            if thread_size == settings.MAX_THREAD_SIZE:
                thread_capacity = math.ceil(self.file_info.file_size.to_kb()/float(thread_size)) # recalculate the thread download capacity

        start_pos = 0
        print 'thread_size:',thread_size,",thread_capacity:",thread_capacity
        for i in range(thread_size):
            normal_end_pos = start_pos + thread_capacity - 1
            end_pos = min(normal_end_pos,self.file_info.file_size.to_kb()-1)
            new_download_thread = download_thread.DownloadThread(self.downloadUrl,start_pos,end_pos)
            start_pos += thread_capacity
            self.downloadThreads.append(new_download_thread)

    """start download file"""
    def start_download(self):
        fileconn = open(self.file_abspath,self.judge_open_mode(self.downloadUrl))
        # self.downloadThreads[1] = download_thread.DownloadThread(self.downloadUrl,0,self.file_info.file_size.to_kb()-1)
        # self.downloadThreads[1].set_output(fileconn)
        # self.downloadThreads[1].start()
        for download_thread in self.downloadThreads:
            download_thread.set_output(fileconn)
            download_thread.start()
        for download_thread in self.downloadThreads:
            download_thread.join()
        if fileconn:
            fileconn.close()

    """return completed size"""
    def get_total_downloaded(self):
        total_size = 0
        for thread in self.downloadThreads:
            total_size += thread.get_completed_len
        return total_size

    """pause download to wait restart"""
    def pause_download(self):
        pass

    """cancel the download anyway"""
    def cancel_download(self):
        pass

    """restart the paused download"""
    def restart_download(self):
        pass

    """invoked when the download finished"""
    def on_finish(self):
        pass

    """generate the downloadfilename"""
    def generate_file_name(self):
        default_file_path = settings.DEFAULT_FILE_PATH
        if not os.path.exists(default_file_path):
            os.mkdir(default_file_path)
        default_file_name = self.file_info.file_name
        file_path = default_file_path + default_file_name
        max_try = 10
        if os.path.exists(file_path):
            file_name = file_path
            suffix_index = file_path.find('.')
            suffix = ''
            if suffix_index != -1:
                file_name = file_path[0:suffix_index]
                suffix = file_path[suffix_index+1:]
            for i in range(max_try):
                if not len(suffix)==0:
                    new_file_path = file_name+"("+str(i+1)+")"+"."+suffix
                else:
                    new_file_path = file_name+"("+str(i+1)+")"
                if not os.path.exists(new_file_path):
                    return new_file_path
                if i == max_try-1:
                    os.remove(new_file_path)
                    return new_file_path
        else:
            return file_path

    """judge mode to open file by the download file's type of the url"""
    def judge_open_mode(self,url):
        return "wb"

# test the ThunderDown
if __name__ == '__main__':
    ThunderDown("https://github.com/mingyangShang/csdn_blog_visitor/blob/master/csdn_blog_vistor/visiting.pyc?raw=true").start_download()
    # ThunderDown("http://image.baidu.com/i?tn=download&ipn=dwnl&word=download&ie=utf8&fr=result&url=http%3A%2F%2Fwww.siweiw.com%2FUpload%2Fsy%2F2013616%2F20136161831938.jpg").start_download()
    # ThunderDown("http://localhost:8000/test.php").start_download()

