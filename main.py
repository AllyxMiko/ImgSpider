#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# @File    :   main.py
# @Time    :   2021/02/05 12:27:51
# @Author  :   Allyx
# @Email   :   allyxmiko@163.com
# @Version :   1.0

# Here put the import lib
from time import sleep
from ImgSpider import ImgSpider
from config.database import DatabaseConfig

#程序入口，初始化ImgSpider对象
img = ImgSpider(DatabaseConfig)
count = img.get_img_count_from_db() + 1
in_count = 0

url = input("请输入随机图片接口的URL:")
in_count_input = input("请输入连续停止数(默认20):")

if(in_count_input == ""):
    in_count_input = 20
else:
    int(in_count_input)

while True:
    # 获取到响应对象
    res = img.send_request(url)
    # 判断状态码
    if(img.get_state_code(res) == 200):
        # 获取到文件md5
        file_md5 = img.cal_img_md5(res)
        # 根据md5查询数据库
        result = img.check_md5(file_md5)
        # 获取保存名
        filename = "{}.{}".format(count, img.get_img_type(res))
        if(result == -1):
            # 清除in_count计数
            in_count = 0
            # 保存图片
            if(img.save_img(res, filename)):
                print("图片保存成功！MD5:{}，原文件名:{}，保存名:{}".format(file_md5, img.get_img_name(res), filename))
                if(img.write_db(file_md5, img.get_url(res), filename)):
                    pass
                else:
                    # 为了保证同步，如果数据库写入失败则删除本地文件
                    img.del_img(filename)
                    print("数据库写入失败！图片网址:{}，请手动下载！".format(img.get_url(res)))
                    continue
            else:
                print("文件写入失败！")
                continue
        else:
            in_count += 1
            print("图片已存在！图片在数据库中的ID:{}，MD5:{}".format(result[0], result[1]))
            if(in_count == in_count_input):
                print("已到达连续停止条件，停止程序运行，已生成{}张图片".format(count))
                exit(1)
    else:
        print("请求错误！")
        continue
    count += 1
    sleep(0.6)
