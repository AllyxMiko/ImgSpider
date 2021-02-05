#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# @File    :   main.py
# @Time    :   2021/02/05 12:27:51
# @Author  :   Allyx
# @Email   :   allyxmiko@163.com
# @Version :   1.0.3

# Here put the import lib
from configparser import ConfigParser
from os.path import exists,join
from os import mkdir
from time import sleep
from sys import exit
from tkinter.constants import END
from modules.ImgSpiderMain import ImgSpiderMain



class ImgSpiderRun:
    tag = True
    input_url = ""

    def __init__(self, msg_box):
        # 初始化消息盒子
        self.msg_box = msg_box
        # 初始化配置文件路径
        self.config_path = "config.conf"
        # 检查config.conf文件是否存在
        self.check_config_file(self.config_path)
        # 初始化configparser
        self.config = ConfigParser()
        # 读取配置文件
        self.config.read(self.config_path, encoding="UTF-8")
        # 获取到db_config并转为字典
        db_config = dict(self.config.items("mysql"))
        # 进行config检查
        for i in db_config:
            if(db_config[i] == "" or db_config[i] is None):
                self.msg_box.insert(END, "config.conf没有配置，请配置后再试！\r\n")
                exit(0)
        # 初始化imgSpider
        self.img = ImgSpiderMain(db_config)
        # 获取到imgspider配置
        img_config = dict(self.config.items("imgspider"))
        # 获取图片保存路径
        self.__img_path = img_config['imgpath']
        # 判断路径是否为空
        if(self.__img_path == ""):
            # 判断当前目录下是否有img文件夹
            if(not exists("img")):
                mkdir("img")
        else:
            # 判断用户自定义图片路径是否为空
            if(not exists(self.__img_path)):
                mkdir(self.__img_path)
        # 配置项赋值
        self.__url = img_config['url']
        self.__stopcount = int(img_config['stopcount'])
        self.__reqtime = float(img_config['reqtime'])
        self.__lastcount = int(img_config['lastcount'])
        self.__reqcount = 0
        self.newcount = 0



    def check_config_file(self, configPath):
        if(not exists(configPath)):
            tmp = '''
[mysql]
host = 127.0.0.1
port = 3306
user = 
password = 
database = 
charset = utf8

[imgspider]
url = 
stopcount = 
reqtime = 
imgpath = 
lastcount = 0
                '''
            with open(configPath, "w", encoding="UTF-8") as f:
                f.write(tmp.strip())



    def main(self):
        if(self.input_url != ""):
            self.__url = self.input_url
        while True:
            if(self.tag):
                self.msg_box.insert(END, "已手动停止，本次下载{}张图片。\r\n".format(self.newcount))
                # 回写配置文件
                self.config['imgspider']['lastcount'] = str(self.__lastcount + self.newcount)
                with open(self.config_path, "w", encoding="UTF-8") as f:
                    self.config.write(f)
                break
            # 获取到响应对象
            res = self.img.send_request(self.__url)
            # 判断状态码
            if(self.img.get_state_code(res) == 200):
                # 获取到文件md5
                file_md5 = self.img.cal_img_md5(res)
                # 根据md5查询数据库
                result = self.img.check_md5(file_md5)
                # 获取保存名
                filename = join(self.__img_path, "{}.{}".format(self.__lastcount + self.newcount + 1, self.img.get_img_type(res)))
                if(result == -1):
                    # 清除in_count计数
                    self.__reqcount = 0
                    # 保存图片
                    if(self.img.save_img(res, filename)):
                        self.msg_box.insert(END, "下载成功！MD5:{}，原文件名:{}，保存路径:{}\r\n".format(file_md5, self.img.get_img_name(res), filename))
                        if(self.img.write_db(file_md5, self.img.get_url(res), filename)):
                            self.newcount += 1
                        else:
                            # 为了保证同步，如果数据库写入失败则删除本地文件
                            self.img.del_img(filename)
                            self.msg_box.insert(END, "数据库写入失败！图片网址:{}，请手动下载！\r\n".format(self.img.get_url(res)))
                            continue
                    else:
                        self.msg_box.insert(END, "文件写入失败！\r\n")
                        continue
                else:
                    self.__reqcount += 1
                    self.msg_box.insert(END, "图片已存在！图片数据库ID:{}，MD5:{}\r\n".format(result[0], result[1]))
                    if(self.__reqcount == self.__stopcount):
                        self.msg_box.insert(END, "已到达连续停止条件，停止程序运行，本次已下载{}张图片。\r\n".format(self.newcount))
                        # 回写配置文件
                        self.config['imgspider']['lastcount'] = str(self.__lastcount + self.newcount)
                        with open(self.config_path, "w", encoding="UTF-8") as f:
                            self.config.write(f)
            else:
                self.msg_box.insert(END, "请求错误！\r\n")
                continue
            sleep(self.__reqtime)
            self.msg_box.see(END)



if __name__ == '__main__':
    a = ImgSpiderRun()
    a.main()
    