# ImgSpider使用方法
### 描述：
    本程序使用Python3.9.1编写，用于下载随机图片接口。
    由于程序最新开发，支持的功能较少，暂时仅支持通过随机图片接口下载图片。

### 使用方法：
    1. 通过运行ImgSider.exe运行
        1.1 双击运行ImgSider.exe
        1.2 第一次运行会生成配置文件，配置config.conf
        1.3 再次打开
    2. 源码运行
        2.1 安装Python环境
        2.2 使用pip install -r requirements.txt 命令安装依赖
        2.3 在项目目录运行ImgSpider.py
        2.4 第一次运行会生成配置文件，配置config.conf
        2.5 在项目目录使用命令 python ImgSpider.py --start开始

### config.conf配置说明：
    数据库配置参数说明:
        host: 数据库地址，默认127.0.0.1
        port: 数据库端口，默认3306
        user: 数据库用户名
        password: 数据库密码
        database: 数据库名称
        charset: 数据库编码，默认utf8
    
    程序配置参数说明:
        url: 随机图片的接口地址
        stopcount: 连续停止数，默认20次，当连续随机到的图片都已保存达到该数时程序停止运行
        reqtime: 连续请求间隔，默认0.6，太低的间隔可能会被封IP
        imgpath: 图片保存地址，请输入绝对路径，留空则默认为当前目录的img文件夹
        lastcount: 最后图片计数，此项如无必要，请勿修改，程序会自动写入

### 命令行:
    --start 开始运行程序
    --version 查看版本

### 更新日志:
    1.2.1 更新日志
        1. 打包的exe版本增加了GUI界面

    1.1.0 更新日志
        1. 重构项目结构
        2. 打包出exe版本
        3. 删除了原先的database.py配置方式
        4. 采用configparser的conf配置文件方式配置
        5. 删除了命令行输入
        6. 加入了--start和--version参数，后期会继续添加

    1.0.3 更新日志
        1. 修复了由于命名问题导致的实际计数会比正常数量多1的bug

    1.0.2 更新日志
        1.更新了README.md文件内容
        2.添加了请求时间间隔控制

    1.0.1 更新日志
        1.修复了全局count导致的文件命名错误的BUG
