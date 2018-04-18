#!/usr/bin/env python
# -*- codeing:UTF-8 -*-
# author caiqyxyx 20180315

import socketserver as socket_server
import socket
import os
import struct
import logging
import sys

log = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
file_handler = logging.FileHandler("socket.log")
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter
log.addHandler(file_handler)
log.addHandler(console_handler)
log.setLevel(logging.INFO)

STRUCT_FMT = '128sl'


class socket_server_handler(socket_server.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.buf = None
        self.filename = None
        self.filesize = None
        socket_server.BaseRequestHandler.__init__(
            self, request, client_address, server)

    def handle(self):
        log.info("replication connected from : %s", self.client_address)
        while True:
            file_info_size = struct.calcsize(STRUCT_FMT)
            self.buf = self.request.recv(file_info_size)
            if self.buf:
                self.filename, self.filesize = struct.unpack(
                    STRUCT_FMT, self.buf)
                self.filename = self.filename.decode('utf-8').strip('\\x00').replace('\0', '')
                recvd_size = 0
                file = open(self.filename, 'wb')
            while not recvd_size == self.filesize:
                if self.filesize - recvd_size > 1024:
                    rdata = self.request.recv(1024)
                    recvd_size += len(rdata)
                else:
                    rdata = self.request.recv(self.filesize - recvd_size)
                    recvd_size = self.filesize
                file.write(rdata)
            file.close()
            log.info("sync file [%s] success!", self.filename)


class replication(object):
    """
    address:(host,port)
    """

    def __init__(self, address):
        # TODO check address
        self.address = address

    def start_repl_server(self):
        tcpServ = socket_server.ThreadingTCPServer(
            self.address, socket_server_handler)
        tcpServ.serve_forever()

    @staticmethod
    def send_file(address, file_list):
        if len(file_list) == 0:
            log.error("there is no file to sync!")
        else:
            for file in file_list:
                replication.start_repl_client(address, file)

    @staticmethod
    def start_repl_client(address, file_path):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if os.path.isfile(file_path):
            s.connect(address)
            # 定义文件头信息，包含文件名和文件大小
            file_head = struct.pack(STRUCT_FMT, os.path.basename(
                file_path).encode('utf-8'), os.stat(file_path).st_size)
            s.send(file_head)
            file = open(file_path, 'rb')
            while True:
                filedata = file.read(1024)
                if not filedata:
                    break
                s.send(filedata)
            file.close()
            log.info("sync file [%s] success!", os.path.basename(file_path))

    @staticmethod
    def check_address(address):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(address)
            return True
        except Exception:
            return False