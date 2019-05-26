from Sql import *
from time import sleep


class ServerHelper:
    def __init__(self):
        self.mysql = MenberManage()
        self.book_id = None
        self.book_name = None
        self.book_author = None
        self.user = None

    @staticmethod
    def send_msg(connfd):
        try:
            connfd.send(b"OK")
            data = connfd.recv(1024).decode()
            if data == "OK":
                return True
        except KeyboardInterrupt:
            return
        except Exception as e:
            print(e)

    # 注册
    def get_register(self, connfd, name, pwd):  # 处理注册请求
        # 查询用户名是否存在
        if self.mysql.do_query_user(name):
            connfd.send("该用户已存在".encode())
            return
        elif self.mysql.do_insert_user(name, pwd):
            connfd.send(b"OK")
        else:
            connfd.send("创建失败".encode())

    # 登录
    def get_login(self, connfd, name, pwd):  # 处理登录请求
        # 匹配用户名和密码
        if self.mysql.do_find_user(name, pwd):
            data = self.mysql.order_by_heat()
            connfd.send(b"OK")
            for i in data:
                connfd.send(i[0], i[1])
            self.user = name
        else:
            connfd.send("登录失败,用户名或密码错误")

    # 根据书名查找
    def get_query(self, connfd, name):  # 处理查询请求
        r = self.mysql.do_query_by_bookname(name)
        if r and self.send_msg(connfd):
            for i in r:
                value = "%s %s" % (i[0], i[1])
                connfd.send(value.encode())
            connfd.send(b"##")
        else:
            connfd.send("查找失败".encode())

    # 根据作者查找
    def get_query_author(self, connfd, author):
        r = self.mysql.do_query_by_author(author)
        if r and self.send_msg(connfd):
            for i in r:
                value = "%s %s" % (i[0], i[1])
                connfd.send(value.encode())
            connfd.send(b"##")
        else:
            connfd.send("查找失败".encode())

    # 记录id
    def save_id(self, name, author):
        self.book_id = self.mysql.do_query_id(name, author)[0][0]
        self.book_name = name
        self.book_author = author
        name_author = "%s %s" % (name, author)
        self.mysql.add_book_heat(self.user, name_author)

    # 发送简介
    def get_describ(self, connfd):
        value = self.mysql.do_query_describ(self.book_id)[0][0]
        if value:
            connfd.send(b"OK")
            data = connfd.recv(1024).decode()
            if data == "OK":
                connfd.send(value.encode())
        else:
            connfd.send("查找失败".encode())

    # 根据编号查找章节目录
    def get_section(self, connfd):
        r = self.mysql.do_section(self.book_id)
        if r and self.send_msg(connfd):
            list01 = [i[0] for i in r]
            msg = "$".join(list01)
            connfd.send(msg.encode())
            sleep(0.1)
            connfd.send(b"##")
        else:
            connfd.send("查找失败".encode())

    # 判断请求
    def get_read_by(self, connfd, data):
        if len(data) == 4:
            section = "%s %s" % (data[2], data[3])
            section_id = self.mysql.do_section_id(self.book_id, section)[0][0]
            section_id = int(section_id)
            if data[1] == "N":
                section_id += 1
            elif data[1] == "L":
                section_id -= 1
            section = self.mysql.do_query_section(self.book_id, section_id)[0][0]
            self.get_read(connfd, section)
        else:
            section = "%s %s" % (data[1], data[2])
            self.get_read(connfd, section)

    # 根据章节名查找路径
    def get_read(self, connfd, section):
        r = self.mysql.do_read(self.book_id, section)[0][0]
        if r and self.send_msg(connfd):
            f = open("%s" % r, encoding="utf-8")
            while True:
                i = f.read(1024)
                connfd.send(i.encode())
                if len(i) < 1024:
                    break
            sleep(0.1)
            connfd.send(b"##")
            f.close()
        else:
            connfd.send("查找失败".encode())

    # 下载请求
    def get_download(self, connfd):  # 处理下载请求
        r = self.mysql.do_download(self.book_id)[0][0]
        if r and self.send_msg(connfd):
            f = open("%s" % r[0][0])
            while True:
                i = f.read(1024)
                if not i:
                    connfd.send(b"##")
                    break
                connfd.send(i.encode())
            f.close()
        else:
            connfd.send("查找失败".encode())

    # 添加书架
    def add_new_bookshelf(self, connfd):
        book_author = "%s %s" % (self.book_name, self.book_author)
        if self.mysql.do_query_bookshelf(self.user, book_author):
            connfd.send("书架已有此书".encode())
        elif self.mysql.add_bookshelf(self.book_name, self.book_author):
            connfd.send(b"OK")
        else:
            connfd.send("添加失败".encode())

    # 查找书架
    def get_bookshelf(self, connfd):
        r = self.mysql.query_bookshelf(self.user)
        if r and self.send_msg(connfd):
            for i in r:
                connfd.send(i[0].encode())
            connfd.send(b"##")
        else:
            connfd.send("查找失败".encode())
