# -*- coding: UTF-8 -*-
import socket, time, socketserver, struct, os

host = '172.27.24.43'
port = 12307
address = (host, port)


class socket_server_handler(socketserver.BaseRequestHandler):
    def handle(self):
        print('connected from:', self.client_address)
        while True:
            fileinfo_size = struct.calcsize('128sl')  # 定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
            self.buf = self.request.recv(fileinfo_size)
            if self.buf:  # 如果不加这个if，第一个文件传输完成后会自动走到下一句
                self.filename, self.filesize = struct.unpack('128sl', self.buf)  # 根据128sl解包文件信息，与client端的打包规则相同
                print('filesize is: ', self.filesize, 'filename size is: ', len(self.filename))  # 文件名长度为128，大于文件名实际长度
                print(self.filename.decode("utf-8"))
                self.filenewname = os.path.join('c:\\', ("asd"+self.filename.decode("utf-8")).strip("\\x00").replace('\0',''))  # 使用strip()删除打包时附加的多余空字符
                print(self.filenewname)
                recvd_size = 0  # 定义接收了的文件大小
                file = open(self.filenewname, 'wb')
                print('stat receiving...')
                while not recvd_size == self.filesize:
                    if self.filesize - recvd_size > 1024:
                        rdata = self.request.recv(1024)
                        recvd_size += len(rdata)
                    else:
                        rdata = self.request.recv(self.filesize - recvd_size)
                        recvd_size = self.filesize
                    file.write(rdata)
                file.close()
                print('receive done')


tcpServ = socketserver.ThreadingTCPServer(address, socket_server_handler)
tcpServ.serve_forever()
