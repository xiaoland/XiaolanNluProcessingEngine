# -*- encoding=utf-8 -*-

import json
import os
import sys
from Nlp import XiaolanNlp

class Base(object):

    def __init__(self):

        self.intentlist = []
        self.pos = ['u', 'n', 'f', 'm', 'ns', 'nt', 'p', 'r', 'w', 'q', 'r', 's', 'a', 'nr']
        self.iflyappid = '5ace1bbb'
        self.iflyapikey = '9e1b8f6028b14b969cdec166eca127ea'
        self.XiaolanNlp = XiaolanNlp()