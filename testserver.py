# -*- coding:UTF-8 -*-

from replication import replication as repl
from replication import socket_server_handler as ssh


address = ('192.168.8.218',8088)

repl_instance = repl(address)

repl_instance.start_repl_server()