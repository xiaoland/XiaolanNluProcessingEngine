# -*- encoding=utf-8 -*-

import json
import os
import sys
import time
import logging



class Base(object):

    def __init__(self):


        self.pos = ['u', 'n', 'f', 'm', 'ns', 'nt', 'p', 'r', 'w', 'q', 'r', 's', 'a', 'nr']
        self.iflyappid = '5ace1bbb'
        self.iflyapikey = '9e1b8f6028b14b969cdec166eca127ea'


    def addLog(self, log, level):

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        log_path = os.path.dirname(os.getcwd()) + './'
        log_name = log_path + 'XiaolanNlu' + '.log'
        logfile = log_name
        fh = logging.FileHandler(logfile, mode='w')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        if level == 'debug':
            logger.debug(log)
        elif level == 'info':
            logger.info(log)
        elif level == 'warning':
            logger.warning(log)
        elif level == 'error':
            logger.error(log)
        elif level == 'critical':
            logger.critical(log)

def application(environ, start_response):

    from Nlu import XiaolanNlu
    method = environ.get('REQUEST_METHOD', 'HEAD')
    if method == "HEAD":
        response_headers = [('Content-Type', 'application/json'),
                                ('Content-Length', str(len("")))]
        start_response('200 OK', response_headers)
        return ""
    else:
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except(ValueError):
            request_body_size = 0
        request_body = environ['wsgi.input'].read(request_body_size).decode('utf-8')
        print('request_body = %s\n' % request_body)
        if not request_body:
            return ['未获取到请求数据']


        b = Base()
        b.addLog('TimeStamp' + request_body['ClientEvent']['Header']['TimeStamp'], "info")
        b.addLog('NameSpace' + request_body['ClientEvent']['Header']['NameSpace'], "info")
        b.addLog('Text' + request_body['Info']['Text'], "info")

        x = XiaolanNlu()

        body_str = x.start(request_body['Info']['Text'])

        body = body_str.encode('utf-8')

        print(body)

        response_headers = [('Content-Type', 'application/json'),
                            ('Content-Length', str(len(body)))]
        status = '200 OK'

        start_response(status, response_headers)

        return [body]