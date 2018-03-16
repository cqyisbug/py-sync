# -*- coding:UTF-8 -*-

from replication import replication as repl
from replication import socket_server_handler as ssh 

address = ('192.168.8.218',8088)

repl.send_file(address,["C:\\Users\\Administrator\\Downloads\\apache-tomcat-9.0.6-windows-x64.zip"])