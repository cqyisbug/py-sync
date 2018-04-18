#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#         Constant
QUE_MAX = 999999

import os
import queue
import hashlib
import time


global q
global file_map
q = queue.Queue(QUE_MAX)
file_map = {}


def monitor(path):
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for d in dirs:
                monitor(d)
            for f in files:
                if file_map.__contains__(hash(f)) and file_map[f] == md5(f):
                    pass
                else:
                    print("{0} changed".format(f))
                    file_map.setdefault(f, md5(f))
                    q.put(f)
            # if os.path.isfile(f):
                
            # else:
            #     monitor(f)


def md5(file):
    md5file = open(file, 'rb')
    md5_ = hashlib.md5(md5file.read()).hexdigest()
    md5file.close()
    return md5_


while True:
    monitor(r"C:\Users\c15367\Desktop\github\py-sync")
    time.sleep(10)
    pass
