# -*- coding:UTF-8 -*-

from replication import replication as repl
from replication import socket_server_handler as ssh
import _thread
import time

address = ('192.168.8.218',8088)

repl_instance = repl(address)

# repl_instance.start_repl_server()

_thread.start_new_thread(repl_instance.start_repl_server,())

while True:
    time.sleep(60)