#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# @File    :   ImgSpider.py
# @Time    :   2021/02/05 00:42:54
# @Author  :   Allyx
# @Email   :   allyxmiko@163.com
# @Version :   1.0

# Here put the import lib
import requests
from module.pysql import PySQL
from config.database import DatabaseConfig

class ImgSpider:

    def __init__(self, config):
        # 检查数据库配置文件
        if(not self.check_config_finish(config)):
            print("数据库未配置，请先配置数据库。")
            exit(0)
        # 初始化数据库链接对象
        self.pysql = PySQL(config)

    def main(self):
        self.print_help()
        # url = input("请输入需要爬取的URL：")

        



    def check_config_finish(self, config):
        return PySQL.check_database_config(config)

    def print_help(self):
        print('''本程序可以爬取随机图片的接口，目前仅支持随机图片接口。
注意：由于程序需要使用数据库保存相关数据，请先配置数据库''')

    def send_request(self, url, headers={}):
        ''' 请求URL
            @url 请求的地址
            @headers 请求头，默认为空
            @return 返回请求的二进制数据
        '''
        return requests.get(url, headers=headers)


if __name__ == '__main__':
    img = ImgSpider(DatabaseConfig)
    img.main()
    