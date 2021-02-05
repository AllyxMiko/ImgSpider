#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# @File    :   ImgSpider.py
# @Time    :   2021/02/05 20:53:07
# @Author  :   Allyx
# @Email   :   allyxmiko@163.com
# @Version :   1.2.1

# Here put the import lib
from time import sleep
from tkinter import StringVar, Tk,Text,Label,Entry,Button
from tkinter.constants import END
from modules.ImgSpiderRun import ImgSpiderRun
from threading import Thread

VERSION = "1.2.1"
# 根窗口
root = Tk()
var = StringVar()
msg_box = Text(root, relief="groove", width=90, height=24)

def run():
    img.main()

def start_download():
    msg_box.insert(END, "开始下载......\r\n")
    img.input_url = var.get()
    img.tag = False
    Thread(target=run, daemon=True).start()

    
def stop_download():
    img.tag = True
    msg_box.insert(END, '停止下载......\r\n')

def init_img():
    global img
    img = ImgSpiderRun(msg_box)


Thread(target=init_img, daemon=True).start()
sleep(0.5)
# 设置标题
root.title("随机图片接口爬取 by Allyx  ver {}".format(VERSION))
# 设置窗口大小
# 窗口宽高
ww = 660
wh = 400
# 设定窗口大小和位置
root.geometry("{}x{}+{}+{}".format(ww, wh, int(root.winfo_screenwidth() / 2 - ww / 2), int(root.winfo_screenheight() / 2 - wh / 2 - 50)))
# 地址提示框
Label(root, text="接口地址:").place(x=52, y=20, anchor="nw")
# 输入框
Entry(root, width=45, textvariable=var).place(x=117, y=22, anchor="nw")
# 开始按钮
Button(root, text="开始下载", command=start_download).place(x=452, y=17, anchor="nw")
# 停止按键
Button(root, text="停止下载", command=stop_download).place(x=527, y=17, anchor="nw")
# 下载显示
msg_box.place(x=14, y=65, anchor="nw")
root.mainloop()