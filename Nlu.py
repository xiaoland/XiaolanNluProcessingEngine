# -*- encoding=utf-8 -*-

import json
import os
import sys
import time
import base64
import hashlib
import requests
import intentlist
from Base import Base

class XiaolanNlu(Base):

    def __init__(self):

        super(XiaolanNlu, self).__init__()
        self.turn = 0

    def Input(self, mode ,text):

        if mode == 'IntentDo':
            self.xl_intent(text)
        elif mode == 'IflyIntentDo':
            self.ifly_intent(text)

    def ifly_intent(self, text):

            appid = '5ace1bbb'
            apikey = '9e1b8f6028b14b969cdec166eca127ea'
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

            csumc = apikey + curtimef + 'eyJ1c2VyaWQiOiIxMyIsInNjZW5lIjoibWFpbiJ9' + 'text=' + textl

            c = hashlib.md5()
            c.update(csumc)
            checksuml = c.hexdigest()

            headers = {'X-Appid': appid, 'Content-type': 'application/x-www-form-urlencoded; charset=utf-8',
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

    def get_slots(self, slotslist, text):

            returndict = {}
            a = 1
            b = 1
            if len(slotslist) != None or slotslist != []:
                while self.turn == 0:
                    try:
                        var = slotslist[a]
                    except IndexError:
                        break
                    else:
                        if var['dict'][b] in text or var['same_means'][b] in text:
                            returndict['slotname'] = slotslist[a - 1]
                            returndict['value'] = var['dict'][b]
                        if len(var['dict']) == b:
                            a = a + 2
                            b = 0
                        else:
                            b = b + 1
            else:
                print('slots read error')
                return returndict
            return returndict

    def xl_intent(self, text):

            b = 0
            a = 0
            c = 0
            data = {}
            if self.turn == 0:
                while self.turn == 0:
                    try:
                        var = [a][1]
                    except IndexError:
                        data = None
                        break
                    else:
                        pass
                    if var[b][c] in text:
                        slots = self.get_slots(self.intentlist[a][2], text)
                        data = {
                            'intent': self.intentlist[a][0][b],
                            'skill': self.intentlist[a][3],
                            'slots': slots,
                            'commands': [
                                'skill', 'start'
                            ],
                            'states': [
                                'xiaolan_nlu_intent_back'
                            ]
                        }
                        if len(var[b]) == c:
                            b = b + 1
                            c = 0
                        elif len(var) == b:
                            a = a + 1
                            b = 0
                            c = 0
                        elif len(self.intentlist) == a:
                            return data
                        else:
                            c = c + 1

                if data == None:
                    return {
                        'intent': self.ifly_intent(text),
                        'skill': self.ifly_intent(text),
                        'slots': None,
                        'commands': [
                            'skill', 'start'
                        ],
                        'states': [
                            'ifly_nlu_intent_back'
                        ]
                    }
                else:
                    return data


