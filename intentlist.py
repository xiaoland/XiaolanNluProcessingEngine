# -*- coding: utf-8 -*-

import sys
import os
import time
import requests
import json

def intentlistturn():

    turnback = []
    return turnback

def xl_intent(self, text):

            """
            小蓝语义理解引擎
            :param text: 用户输入文本
            :return:
            """
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