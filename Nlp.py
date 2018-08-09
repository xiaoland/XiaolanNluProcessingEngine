# -*- encoding=utf-8 -*-

import json
import requests
import urllib

from Base import Base

class XiaolanNlp(Base):

    def __init__(self):

        super(XiaolanNlp, self).__init__()
        self.AK = 'TSFp0BKH547h7Agjf2WkV2Ll'
        self.SK = 'c9RZ1ZLxPe6wQVWOUwjaWOLvM7EpXHwe'
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
        url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer?charset=UTF-8&access_token=' + self.token

        body = {
            "text": text.decode('UTF-8').encode('GBK')
        }

        r = requests.post(url,
                          data = body,
                          headers = {'Content-Type': '	application/json'})

        result = r.json()

        trunlist = []

        a = 1
        while 1 == 1:
            word = []
            try:
                word.append(result['items'][len(result['itmes']) - a]['item'])
                if result['items'][len(result['itmes']) - a]['pos'] != None or result['items'][len(result['itmes']) - a]['pos'] != "":
                    word.append(result['items'][len(result['itmes']) - a]['pos'])
                else:
                    word.append(result['items'][len(result['itmes']) - a]['ne'])
                trunlist.append(word)
            except:
                break
            else:
                a = a + 1

        return trunlist

    def BaiduTextLikeInfo(self, text_1, text_2):

        """
        百度短文本相似度分析
        :param text_1: 分析文本1
        :param text_2: 分析文本2
        :return:
        """
        url = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/simnet?charset=UTF-8&access_token=' + self.token

        body = {
            'text_1': text_1.decode('UTF-8').encode('GBK'),
            'text_2': text_2.decode('UTF-8').encode('GBK')
        }

        r = requests.post(url,
                          data = body,
                          headers = {'Content-Type':	'application/json'})

        result = r.json()

        if result['score'] > 0.5:
            return True
        else:
            return False

    def BaiduWordLikeInfo(self, word_1, word_2):

        """
        百度词语相似度分析
        :param word_1: 分析词语1
        :param word_2: 分析词语2
        :return:
        """
        url = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/word_emb_sim?charset=UTF-8&access_token=' + self.token

        body = {
            'word_1': word_1.decode('UTF-8').encode('GBK'),
            'word_2': word_2.decode('UTF-8').encode('GBK')
        }

        r = requests.post(url,
                          data = body,
                          headers = {'Content-Type': 'application/json'})


        result = r.json()

        if result['score'] > 0.5:
            return True
        else:
            return False

    def BaiduTextDepparser(self, text):

        """
        百度依存词法分析
        :param text: 用户输入文本
        :return:
        """
        url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/depparser?charset=UTF-8&access_token=' + self.token

        body = {
            "text": text.decode('UTF-8').encode('GBK'),
            "mode": 1
        }

        r = requests.post(url,
                          data=body,
                          headers={'Content-Type': 'application/json'})

        result = r.json()

        trunlist = []

        a = 1
        while 1 == 1:
            word = []
            try:
                word.append(result['items'][len(result['itmes']) - a]['item'])
                word.append(result['items'][len(result['itmes']) - a]['postag'])
                word.append(result['items'][len(result['itmes']) - a]['deprel'])
                trunlist.append(word)
            except:
                break
            else:
                a = a + 1

        return trunlist

    def BaiduTextErrorFix(self, text):

        """
        百度文本纠错
        :param text: 用户输入文本
        :return:
        """
        url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/ecnet?charset=UTF-8&access_token=' + self.token

        body = {
            'text': text
        }
        body = json.dumps(body)
        r = requests.post(url,
                          data = body,
                          headers = {'Content-Type': 'application/json'})

        result = r.json()
        print(result)
        if result['item']['score'] > 0.5:
            return result['item']['correct_query']
        else:
            return text

    def BaiduKeyWordGet(self, text):

        """
        百度关键字提取
        :param text: 用户输入文本
        :return:
        """
        url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/keyword?charset=UTF-8&access_token=' + self.token

        body = {
            'title': text.decode('UTF-8').encode('GBK'),
            'content': text.decode('UTF-8').encode('GBK')
        }

        r = requests.post(url,
                          data = body,
                          headers = {'Content-Type': 'application/json'})

        return r.json()['items']

