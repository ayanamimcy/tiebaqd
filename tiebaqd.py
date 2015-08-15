#!/usr/bin/env python
#coding:utf-8

import requests
import re
import os

class QD:

    def __init__(self, name, cookie):
        self.name = name
        self.cookie = cookie
        self.session = requests.Session()

    def get_login(self):
        url = 'http://tieba.baidu.com/f/like/mylike?pn='
        try:
            page = self.session.get(url, cookies=self.cookie)
            return page.text
        except:
            print('登陆失败请检查cookies')
            return None

    def get_bar(self):
        page = self.get_login()
        result = []
        a = r'title="(.+?)">\1</a></td>'
        a = re.compile(a)
        result = re.findall(a, page)
        return result

    def add_sign(self, name):
        post = {
            'ie' : 'utf-8',
            'kw' : name,
            'tbs' : '6ac12c1c8431559d1424007047'
            }
        result = self.session.post('http://tieba.baidu.com/sign/add', data=post, cookies=self.cookie)
        return result

    def main(self):
        name = self.get_bar()
        if name == []:
            print('登陆失败请检查cookies')
            return None
        print(self.name)
        for index in name:
            print(index + '吧')
            result = self.add_sign(index)
            if result.text.find('success') == -1:
                print('已经签过到了')
            else:
                print('签到成功')

if os.path.isfile('/home/mcy/Templates/python/.tiebaconfig'):
    file = open('/home/mcy/Templates/python/.tiebaconfig', 'r')
    for line in file:
        args = line.split(':')
        cookie = dict(BDUSS=args[1])
        sss = QD(args[0], cookie)
        sss.main()
else:
    print('''
    你需要创建.tiebaconfig文件
    格式如下：
    ID:BDUSS
    ''')
