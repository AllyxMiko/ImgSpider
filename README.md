# ImgSpider使用方法
### 描述：
    本程序使用Python3.9.1编写，用于下载随机图片接口。
    由于程序最新开发，支持的功能较少，暂时仅支持通过随机图片接口下载图片。

### 使用方法：
    注意: 请自行下载Python环境，后期可能会出打包版本。
    1. 安装依赖文件
        1.1 进入项目根目录
        1.2 命令行运行 pip install -r requirements.txt
    2. 运行main.py
    3. 第一次运行请去根目录下的config文件夹中的database.py里配置数据库。

### 条目说明
    1. "请输入随机图片接口的URL" 这个地址必须是随机的图片API
    2. "请输入连续停止数(默认20)" 此项表示连续多少次随机的图片已保存后就停止程序运行，默认连续20次没有随机出现新图片后就停止程序。
    3. "请输入连续请求间隔时间(默认0.6秒)" 此项表示连续请求的间隔时间，间隔时间太长可能会导致IP被封禁
    4. 下载下来的图片会保存在项目根目录下的img文件夹下，并以数字命名。

### 更新日志
    1.0.3 更新日志
        1. 修复了由于命名问题导致的实际计数会比正常数量多1的bug

    1.0.2 更新日志
        1.更新了README.md文件内容
        2.添加了请求时间间隔控制

    1.0.1 更新日志
        1.修复了全局count导致的文件命名错误的BUG
