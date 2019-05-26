from socket import *
from Seversetting import *
from multiprocessing import Process
from ServerHelper import *


class Server:
    def __init__(self):
        self.sockfd = socket()
        self.sockfd.bind(ADDR)
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.serverhelper = ServerHelper()

    def operation(self):
        self.sockfd.listen(5)
        while True:
            try:
                connfd, addr = self.sockfd.accept()
                print(addr)
            except KeyboardInterrupt:
                self.sockfd.close()
            except Exception as e:
                print(e)
            else:
                p = Process(target=self.handle, args=(connfd,))
                p.daemon = True
                p.start()

    def handle(self, connfd):  # 接收客户端请求,解析并处理的方法
        while True:
            # 接收客户端请求
            msg = connfd.recv(1024).decode()
            data = msg.split(" ")
            if not data or data[0] == "E":
                connfd.close()
                return
            elif data[0] == "R":
                self.serverhelper.get_register(connfd, data[1], data[2])
            elif data[0] == "L":
                self.serverhelper.get_login(connfd, data[1], data[2])
            elif data[0] == "H":
                pass
            elif data[0] == "B":
                self.serverhelper.get_query(connfd, data[1])
            elif data[0] == "A":
                self.serverhelper.get_query_author(connfd, data[1])
            elif data[0] == "O":
                self.serverhelper.save_id(data[1], data[2])
                self.serverhelper.get_section(connfd)
            elif data[0] == "C":
                self.serverhelper.get_section(connfd)
            elif data[0] == "P":
                self.serverhelper.get_read_by(connfd, data)
            elif data[0] == "E":
                self.serverhelper.add_new_bookshelf(connfd)
            elif data[0] == "F":
                self.serverhelper.get_bookshelf(connfd)
            elif data[0] == "D":
                self.serverhelper.get_download(connfd)
