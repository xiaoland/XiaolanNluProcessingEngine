# -*- encoding=utf-8 -*-

import json
import requests
import os
import sys

from Base import Base

class XiaolanNlp(Base):

    def __init__(self):

        super(XiaolanNlp, self).__init__(self)
        self.AK = 'EzSEdCoje0SVvCUsFmI7bLwG'
        self.SK = 'Zsyx4x9LiuzNMfhyAH2B4yCBluYCRnS2'
        self.token = self.get_token()

    def get_token(self):

        """
        获取token
        :return:
        """
        AK = self.AK
        SK = self.SK
        URL = 'http://openapi.baidu.com/oauth/2.0/token'

        params = urllib.urlencode({'grant_type': 'client_credentials',
                                   'client_id': AK,
                                   'client_secret': SK})
        r = requests.get(URL, params=params)
        try:
            r.raise_for_status()
            token = r.json()['access_token']
            return token
        except requests.exceptions.HTTPError:
            self._logger.critical('Token request failed with response: %r',
                                  r.text,
                                  exc_info=True)

    def BaiduWordLexicalAnalysis(self, text):

        """
        百度词法分析
        :param text: 用户输入文本
        :return:
        """
        url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer?access_token=' + self.token

        body = {
            "text": text.decode('UTF-8').encode('GBK')
        }

        r = requests.post(url,
                          body = body,
                          headers = {'Content-Type': '	application/json'})

        json = r.json()

        trunlist = []

        a = 1
        while 1 == 1:
            word = []
            try:
                word.append(json['items'][len(json['itmes']) - a]['item'])
                if json['items'][len(json['itmes']) - a]['pos'] != None or json['items'][len(json['itmes']) - a]['pos'] != "":
                    word.append(json['items'][len(json['itmes']) - a]['pos'])
                else:
                    word.append(json['items'][len(json['itmes']) - a]['ne'])
                trunlist.append(word)
            except:
                break
            else:
                a = a + 1

        return trunlist

    def BaiduTextLikeInfo(self, text_1, text_2):

        url = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/simnet?access_token=' + self.token

        body = {
            'text_1': text_1,
            'text_2': text_2
        }

        r = requests.post(url,
                          body = body,
                          headers = {'Content-Type':	'application/json'})

        json = r.json()

        if json['score'] > 0.5:
            return True
        else:
            return False

    def BaiduWordLikeInfo(self, word_1, word_2):

        url = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/word_emb_sim?access_token=' + self.token

        body = {
            'word_1': word_1,
            'word_2': word_2
        }

        r = requests.post(url,
                          body = body,
                          headers = {'Content-Type': 'application/json'})


        json = r.json()

        if json['score'] > 0.5:
            return True
        else:
            return False

    def BaiduTextDepparser(self, text):

        url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/depparser?access_token=' + self.token

        body = {
            "text": text,
            "mode": 1
        }

        r = requests.post(url,
                          body = body,
                          headers = {'Content-Type': 'application/json'})

        json = r.json()

        trunlist = []

        a = 1
        while 1 == 1:
            word = []
            try:
                word.append(json['items'][len(json['itmes']) - a]['item'])
                word.append(json['items'][len(json['itmes']) - a]['postag'])
                word.append(json['items'][len(json['itmes']) - a]['deprel'])
                trunlist.append(word)
            except:
                break
            else:
                a = a + 1

        return trunlist