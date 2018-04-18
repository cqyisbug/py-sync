# !/usr/bin/env python
# -  *  - coding:UTF-8 -  *  - 


import os
import queue
import hashlib

#         Constant
QUE_MAX = 999999

global q
global file_map
q = queue.Queue(QUE_MAX)
file_map =  {}


def monitor(path):
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for d in dirs:
                pass
                # monitor(os.path.join(path, d))
            for f in files:
                if file_map.__contains__(hash(os.path.join(root, f)))and file_map[os.path.join(root, f)] == md5(os.path.join(root, f)):
                    pass
                else:
                    print("{0} changed".format(os.path.join(root, f)))
                    file_map.setdefault(os.path.join(root, f), md5(os.path.join(root, f)))
                    q.put(os.path.join(root, f))


def md5(file):
    md5file = open(file, 'rb')
    md5_ = hashlib.md5(md5file.read()).hexdigest()
    md5file.close()
    return md5_


# print(os.list)
monitor(r"C:\Users\Administrator\Desktop\github\py-sync")
print(file_map)
