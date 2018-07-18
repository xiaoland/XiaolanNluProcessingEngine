# -*- encoding=utf-8 -*-

# description:
# author: xiaoland
# create_time: 2018/7/18

"""
    desc:pass
"""

from wsgiref.simple_server import make_server
# 导入我们自己编写的application函数:
from Base import application
httpd = make_server('', 8000, application)
print('Serving HTTP on port 8000...')
# 开始监听HTTP请求:
httpd.serve_forever()