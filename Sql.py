from Database import MysqlHelper


class MenberManage:
    def __init__(self):
        self.mysql = MysqlHelper()
        self.mysql.open_mysql()  # 连接数据库

    def __del__(self):
        self.mysql.close_mysql()  # 关闭数据库

    # 查找用户名是否存在
    def do_query_user(self, name):
        sql = "select * from user where user_name = '%s'" % name
        if self.mysql.select(sql):
            return True

    # 插入用户
    def do_insert_user(self, name, pwd):
        sql = "insert into user (user_name,user_passwd) values('%s','%s')" % (name, pwd)
        if self.mysql.update(sql):
            return True

    # 匹配用户名和密码
    def do_find_user(self, name, pwd):
        sql = "select user_passwd from user where user_name = '%s'" % name
        if self.mysql.select(sql)[0][0] == pwd:
            return True

    # 根据书名查找
    def do_query_by_bookname(self, book_name):
        sql = "select book_name,book_author from books where book_name='%s'" % book_name
        result = self.mysql.select(sql)
        return result

    # 根据作者查找
    def do_query_by_author(self, author):
        sql = "select book_name,book_author from books where book_author='%s'" % author
        result = self.mysql.select(sql)
        return result

    # 根据书名作者查找图书id
    def do_query_id(self, book_name, author):
        sql = "select book_id from books where book_author='%s' and book_name='%s'" % (author, book_name)
        result = self.mysql.select(sql)
        return result

    # 查找书简介
    def do_query_describ(self, book_id):
        sql = "select book_describ from books where book_id = %d" % book_id
        result = self.mysql.select(sql)
        return result

    # 根据书的编号获取所有章节
    def do_section(self, book_id):
        book_id = "B" + str(book_id)
        sql = "select section_name from %s" % book_id
        result = self.mysql.select(sql)
        return result

    # 根据章节名读取正文
    def do_read(self, book_id, section):
        book_id = "B" + str(book_id)
        sql = "select section_path from %s where section_name = '%s'" % (book_id, section)
        result = self.mysql.select(sql)
        return result

    # 读取整本书的路径
    def do_download(self, book_id):
        sql = "select book_path from books where book_id = %d" % book_id
        result = self.mysql.select(sql)
        return result

    # 查找章节编号
    def do_section_id(self, book_id, section):
        book_id = "B" + str(book_id)
        sql = "select section_id from %s where section_name = '%s' " % (book_id, section)
        result = self.mysql.select(sql)
        return result

    # 根据编号查找章节
    def do_query_section(self, book_id, section_id):
        book_id = "B" + str(book_id)
        sql = "select section_name from %s where section_id = %d" % (book_id, section_id)
        result = self.mysql.select(sql)
        return result

    # 热度增加
    def add_book_heat(self, user, book_author):
        sql = "insert into heat_book(user_name,book_author) values('%s','%s')" % (user, book_author)
        if self.mysql.update(sql):
            return True

    # 查询热度前５的小说
    def order_by_heat(self):
        sql = "select book_author,sum(times) from heat_book group by name_author order by sum(times) desc limit 5;"
        result = self.mysql.select(sql)
        return result

    # 查看是否已经存过
    def do_query_bookshelf(self, user, book_author):
        sql = "select * from bookshelf where user_name = '%s' and book_author = '%s'" % (user, book_author)
        result = self.mysql.select(sql)
        return result

    # 添加到书架
    def add_bookshelf(self, user, book_author):
        sql = "insert into bookshelf(user_name,book_author) values('%s','%s')" % (user, book_author)
        result = self.mysql.update(sql)
        return result

    # 查找书架
    def query_bookshelf(self, user):
        sql = "select book_author from bookshelf where user_name = '%s'" % user
        result = self.mysql.select(sql)
        return result
