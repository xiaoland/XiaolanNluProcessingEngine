# -*- encoding=utf-8 -*-

import json
import time
import base64
import hashlib
import requests
import urllib
import urllib2
from Base import Base
from Nlp import XiaolanNlp

class XiaolanNlu(Base):

    def __init__(self):

        super(XiaolanNlu, self).__init__()
        self.XiaolanNlp = XiaolanNlp()
        self.turn = 0

    def start(self, text):

        """
        小蓝语义理解引擎
        :return:
        """
        IntentInfo = {}
        text = self.XiaolanNlp.BaiduTextErrorFix(text)
        wordlexer = self.XiaolanNlp.BaiduWordLexicalAnalysis(text)
        wordlexer = self.WordTypeOut(wordlexer)
        # self.addLog('FixText' + text, 'info')
        # self.addLog('wordlexer' + wordlexer, 'info')
        a = 0
        b = 0
        c = 0
        pos = self.pos
        while 1 == 1:

            if self.XiaolanNlp.BaiduTextLikeInfo(text, self.intentlist[a][2][b]['text'][c]) > 0.5:
                if self.XiaolanNlp.BaiduWordLikeInfo(wordlexer['n'], self.intentlist[a][2][b]['n'][c]) >= 0.48 and self.XiaolanNlp.BaiduWordLikeInfo(wordlexer['v'], self.intentlist[a][2][b]['v']) > 0.48:
                    IntentInfo = {
                        'MainIntent': self.intentlist[a][0],
                        'Intent': self.intentlist[a][1][b],
                        'Skill': self.intentlist[a][-1],
                        'Slots': self.get_slots(self.intentlist[a][3][b], text),
                        'WordLexer': wordlexer,
                        'KeyWord': self.XiaolanNlp.BaiduKeyWordGet(text),
                        'Text': text
                    }
                    break
                else:
                    pass
            else:
                c = c + 1
                if c > len(self.intentlist[a][2][b]['text']) or c > len(self.intentlist[a][2][b]['n']):
                    c = 0
                    b = b + 1
                    if b > len(self.intentlist[a][2]):
                        a = a + 1
                        b = 0
                        c = 0
                        if a > len(self.intentlist):
                            break
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            if IntentInfo == {} or IntentInfo == '':
                return {
                    'MainIntent': 'tuling',
                    'Intent': 'tuling',
                    'Skill': 'tuling',
                    'Slots': None,
                    'WordLexer': wordlexer,
                    'KeyWord': None,
                    'Text': text
                }
            else:
                pass
        return IntentInfo


    def get_slots(self, slotslist, text):

            """
            小蓝语义理解引擎槽位识别
            :param slotslist: 槽位列表
            :param text: 用户输入文本
            :return:
            """
            slotname = []
            slotvalue = []
            a = 0
            b = 0
            if len(slotslist) != None or slotslist != []:
                while self.turn == 0:
                    try:
                        var = slotslist[a][1]
                    except IndexError:
                        break
                    else:
                        if var['dict'][b] in text or var['same_means'][b] in text:
                            slotname.append(slotslist[a][0])
                            slotvalue.append(var['dict'][b])
                        if len(var['dict']) == b:
                            a = a + 2
                            b = 0
                        else:
                            b = b + 1
            else:
                print('slots read error')
                return {}
            return {
                'SlotName': slotname,
                'SlotValue': slotvalue
            }

    def WordTypeOut(self, lists):

            """
            将type与word重新组合
            :param lists: 处理列表
            :return:
            """
            b = 1
            v = [];f = [];m = [];a = [];ns = [];s = [];nr = [];nt = [];d = [];p = [];q = [];r = [];w = [];u = [];c = [];n = []
            while 1 == 1:

                if lists[b] == 'n':
                    n.append(lists[b - 1])
                elif lists[b] == 'v':
                    v.append(lists[b - 1])
                elif lists[b] == 'f':
                    f.append(lists[b - 1])
                elif lists[b] == 'm':
                    m.append(lists[b - 1])
                elif lists[b] == 'a':
                    a.append(lists[b - 1])
                elif lists[b] == 'ns':
                    ns.append(lists[b - 1])
                elif lists[b] == 's':
                    s.append(lists[b - 1])
                elif lists[b] == 'nr':
                    nr.append(lists[b - 1])
                elif lists[b] == 'nt':
                    nt.append(lists[b - 1])
                elif lists[b] == 'd':
                    d.append(lists[b - 1])
                elif lists[b] == 'p':
                    p.append(lists[b - 1])
                elif lists[b] == 'q':
                    q.append(lists[b - 1])
                elif lists[b] == 'r':
                    r.append(lists[b - 1])
                elif lists[b] == 'w':
                    w.append(lists[b - 1])
                elif lists[b] == 'u':
                    u.append(lists[b - 1])
                elif lists[b] == 'c':
                    c.append(lists[b - 1])
                else:
                    b = b + 2
                    try:
                        test = lists[b]
                    except:
                        break
            return {
                'u': u,
                'm': m,
                'n': n,
                'v': v,
                'f': f,
                'a': a,
                'ns': ns,
                's': s,
                'nr': nr,
                'nt': nt,
                'd': d,
                'p': p,
                'q': q,
                'r': r,
                'w': w,
                'c': c
            }





class IflyNlu(Base):

    def __init__(self, text):

        super(IflyNlu, self).__init__()

    def start(self, text):

            """
            讯飞语义理解引擎
            :param text: 用户输入文本
            :return:
            """
            curtimeo = int(time.time())
            curtimef = str(curtimeo)

            try:
                textl = base64.b64encode(text)
            except TypeError:
                return {
                    'intent': None,
                    'skill': None,
                    'commands': [
                        'speaker', 'speacilrecorder'
                    ],
                    'states': [
                        'nlu_intent_back_none'
                    ]
                }

            csumc = self.iflyapikey + curtimef + 'eyJ1c2VyaWQiOiIxMyIsInNjZW5lIjoibWFpbiJ9' + 'text=' + textl

            c = hashlib.md5()
            c.update(csumc)
            checksuml = c.hexdigest()

            headers = {'X-Appid': self.iflyappid, 'Content-type': 'application/x-www-form-urlencoded; charset=utf-8',
                       'X-CurTime': curtimef, 'X-Param': 'eyJ1c2VyaWQiOiIxMyIsInNjZW5lIjoibWFpbiJ9',
                       'X-CheckSum': checksuml}
            url = 'http://api.xfyun.cn/v1/aiui/v1/text_semantic?text=' + textl

            r = requests.post(url,
                              headers=headers)
            json = r.json()
            try:
                intent = json['data']['service']
            except KeyError:
                return {
                    'intent': None,
                    'skill': None,
                    'commands': [
                        'tts', '对不起，我无法理解您的意思'
                    ],
                    'states': [
                        'nlu_intent_back_none'
                    ]
                }
            except TypeError:
                return {
                    'intent': None,
                    'skill': None,
                    'commands': [
                        'tts', '对不起，我无法理解您的意思'
                    ],
                    'states': [
                        'nlu_intent_back_none'
                    ]

                }
            else:
                if intent != None or intent != '':
                    return {
                        'intent': intent,
                        'skill': intent,
                        'commands': [
                            'skills_requests'
                        ],
                        'states': [
                            'nlu_intent_back_none'
                        ]
                    }
                else:
                    return {
                        'intent': None,
                        'skill': None,
                        'commands': [
                            'tts', '对不起，我无法理解您的意思'
                        ],
                        'states': [
                            'nlu_intent_back_none'
                        ]
                    }


