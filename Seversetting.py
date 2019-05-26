PORT = 10085
IP = '0.0.0.0'
ADDR = (IP, PORT)

# 数据库连接地址
HOST = "localhost"
USER = "root"
PWD = "123456"
DBNAME = "books"

# 建库语句
# create database books default charset=utf8;

# 用户列表
# create table user (user_id int(8) primary key auto_increment,user_name varchar(32) not null,user_passwd varchar(32)
# not null, user_type int(4) default 1)default charset=utf8;

# 统计用户查询
# create table heat_book (data_id int(8) primary key auto_increment,user_name varchar(32),book_author varchar(32),
# times int(4) default 1,time datetime default now())default charset=utf8;

# 用户书架表
# create table bookshelf (user_name varchar(32),book_author varchar(32),time datetime default now())
# default charset=utf8;

# 书总表
# create table books(book_id int(8) primary key auto_increment,book_name varchar(32) not null,book_author varchar(32),
# book_path varchar(64) not null,book_describ varchar(264),book_heat int(8) default 0)default charset=utf8;

# 动态创建的书章节表
# create table 表明(section_id int(8) primary key auto_increment,section_name varchar(64) not null,
# section_path varchar(64) not null)default charset=utf8;
