import pymysql
from Seversetting import *


class MysqlHelper:
    def __init__(self):
        self.mysql = None

    def open_mysql(self):
        try:
            self.mysql = pymysql.connect(HOST, USER, PWD, DBNAME, use_unicode=True, charset="utf8")
        except Exception as e:
            print("连接数据库失败", e)

    def close_mysql(self):
        try:
            self.mysql.close()
        except Exception as e:
            print("关闭数据库失败", e)

    def select(self, mysql):
        """
        查询方法
        :param mysql:
        :return:
        """
        try:
            cursor = self.mysql.cursor()
            cursor.execute(mysql)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print("查找数据失败", e)

    def update(self, mysql):
        """
        修改方法
        :param mysql:
        :return:
        """
        try:
            cursor = self.mysql.cursor()
            result = cursor.execute(mysql)
            self.mysql.commit()
            cursor.close()
            return result
        except Exception as e:
            print("数据修改失败", e)
