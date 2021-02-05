#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# @File    :   ImgSpider.py
# @Time    :   2021/02/05 00:42:54
# @Author  :   Allyx
# @Email   :   allyxmiko@163.com
# @Version :   1.0.1

# Here put the import lib
from os import remove
import time
from hashlib import md5
from requests import get
from modules.PySQL import PySQL

class ImgSpiderMain:
    sql = '''CREATE TABLE `img` (
  `id` int NOT NULL AUTO_INCREMENT,
  `md5` varchar(255) NOT NULL,
  `url` varchar(255) DEFAULT NULL,
  `save_name` varchar(255) NOT NULL,
  `create_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;'''

    def __init__(self, config):
        # 初始化数据库链接对象
        self.pysql = PySQL(config)
        # 检查数据库
        if(not self.pysql.check_table("img")):
            # 删除原先数据表
            self.pysql.drop_table('img')
            # 创建新的数据表
            self.pysql.execute(self.sql)


    def cal_img_md5(self, res):
        return md5(res.content).hexdigest()

    def send_request(self, url, headers={}):
        ''' 请求URL
            @url 请求的地址
            @headers 请求头，默认为空
            @return 返回请求对象
        '''
        return get(url, headers=headers)

    def get_img_count_from_db(self):
        self.pysql.execute("SELECT count(`id`) FROM `img`;")
        count = self.pysql.cursor.fetchone()
        return count[0]

    def check_md5(self, md5):
        if(self.pysql.execute("SELECT * FROM `img` WHERE `md5`=\'{}\'".format(md5)) == 0):
            data = self.pysql.cursor.fetchone()
            if(data is None):
                return -1
            else:
                return data
        else:
            return self.pysql.cursor.fetchone()

    def get_img_type(self, res):
        return self.get_img_name(res).split(".")[-1]

    def get_img_name(self, res):
        return self.get_url(res).split("/")[-1]

    def get_state_code(self, res):
        return res.status_code

    def write_db(self, md5, url, save_name):
        # 需要md5， url， 保存的名称
        localtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        sql = "INSERT INTO `img` (`md5`, `url`, `save_name`, `create_time`) VALUES (\'{}\', \'{}\', \'{}\', \'{}\');".format(md5, url, save_name, localtime)
        res = self.pysql.execute(sql)
        if(res == 1):
            return True
        else:
            return False

    def save_img(self, res, filename):
        with open(filename, "wb") as f:
            if(f.write(res.content) == int(self.get_header_value(res, "Content-Length"))):
                return True
            else:
                return False

    def get_url(self, res):
        return res.url

    def del_img(self, filename):
        return remove('img/{}'.format(filename))

    def get_header_value(self, res, key=""):
        ''' 通过key取出headers中的值
            @res 请求的响应
            @key 其中的键，默认为空，如果为空则返回整个headers
            @return key为空返回整个headers，key不为空返回对应的值
        '''
        if(key == ""):
            return res.headers
        else:
            if(key in res.headers):
                return res.headers[key]
            else:
                raise KeyError

    