#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# @File    :   pysql.py
# @Time    :   2021/02/05 00:34:31
# @Author  :   Allyx
# @Email   :   allyxmiko@163.com
# @Version :   1.0

# Here put the import lib
import pymysql
import os

class PySQL:
    __login_err = ""

    def __init__(self, options:dict):
        try:
            # 初始化数据库链接
            self.conn = pymysql.connect(
                host=options['host'],
                port=options['port'],
                user=options['user'],
                password=options['password'],
                database=options['database'],
                charset=options['charset'],
            )
            # 获得游标对象
            self.cursor = self.conn.cursor()
        except Exception as e:
            self.__login_err = e

    def description(self, sql):
        self.execute(sql)
        return self.cursor.description

    def get_filed(self, tableName):
        ''' 获取表的字段
            @tableName 表名
            @return 返回一个带有字段的列表
        '''
        self.execute("SELECT * FROM {};".format(tableName))
        return [tuple[0] for tuple in self.cursor.description]

    def fetch_all(self, sql):
        ''' 获取数据
            @sql sql语句
            @return 返回执行结果是一个元组
        '''
        self.execute(sql)
        return self.cursor.fetchall()

    def drop_table(self, tableName:str):
        ''' 删除数据表
            @tableName 数据表名称
            @return 删除成功返回0
        '''
        return self.execute("DROP TABLE IF EXISTS {};".format(tableName))


    @staticmethod
    def check_database_config(databaseconfig:dict):
        for i in databaseconfig:
            if(databaseconfig[i] == "" or databaseconfig == None):
                return False
        else:
            return True


    def check_sql_file(self, sql_file):
        ''' 判断是否为sql文件
            @sql_file 传入的sql文件路径
            @return 是sql文件返回True，否则返回False
        '''
        if(sql_file.split(".")[-1] == "sql"):
            return True
        else:
            return False

    def read_sql_file(self, sql_file):
        ''' 读取sql文件的内容
            @sql_file 传入sql文件的路径
            @return 返回sql文件的内容
        '''
        # 判断文件是否存在
        if(os.path.isfile(sql_file)):
            # 判断是否为sql文件
            if(self.check_sql_file(sql_file)):
                with open(sql_file, "r") as f:
                    return f.read()
            else:
                raise TypeError
        else:
            raise FileNotFoundError

    def execute(self, sql):
        ''' 执行sql语句
            @sql sql语句
            @return 执行成功返回受影响的行数，执行失败返回-1
        '''
        try:
            res = self.cursor.execute(sql)
            self.commit()
            return res
        except Exception:
            self.rollback()
            return -1


    def sql_file_execute(self, sql_file):
        ''' 执行sql文件
            @sql_file sql文件的路径
            @return 执行成功返回0，执行失败返回-1
        '''
        try:
            res = self.cursor.execute(self.read_sql_file(sql_file))
            self.commit()
            return res
        except Exception:
            self.rollback()
            return -1

    def rollback(self):
        '''回滚数据'''
        self.conn.rollback()

    def commit(self):
        '''提交数据'''
        self.conn.commit()

    def cur_close(self):
        '''关闭游标'''
        self.cursor.close()

    def db_close(self):
        '''关闭数据库'''
        self.conn.close()

    def check_table(self, tableName):
        stand = ['id', 'md5', 'url', 'save_name', 'create_time']
        # 数据表是否存在
        if(self.execute("SELECT * FROM {};".format(tableName)) == -1):
            return False
        else:
            if(self.get_filed(tableName) == stand):
                return True
            else:
                return False

    
    def __del__(self):
        '''对象销毁时自动调用关闭游标和数据库'''
        try:
            self.cur_close()
            self.db_close()
        except Exception:
            print("PySQL模块初始化失败！错误信息:{}".format(self.__login_err))


if __name__ == '__main__':
    # pysql = PySQL()
    pass
    