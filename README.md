# zlibrary-scrapy

# 项目简介
1. 该项目用于Python的Scrapy库的学习与练习。
2. 目标网站是爬取的zlib【最爱的网站之一】。
3. 代码可以直接pull使用。

# 安装scrapy库即可
``` python
pip install scrapy
```
# 结构简介
## 爬取逻辑在zlib文件
1. 爬取目录页
2. 爬取目录页中各分组
3. 爬取书的url，其保存在<div>标签中，单独再做拼接即可。
** 注意：设置zlib分配给你的私域url，并设置cookie登录**
## 保存数据的对象在items中
## 数据库操作在pipeline中
* 本案例通过mysql保存数据
## 在setting文件中配置你的本地环境
* 主要配置mysql数据库即可

**备注：第一次上传项目，大佬勿喷**
