# -*- coding: utf-8 -*-
import json

import requests


class HbcStore(object):

    def __init__(self, **kwargs):
        self.host = kwargs['host']
        self.port = kwargs['port']
        self.headers = {
            'content-type': 'application/json'
        }
        # 连接状态
        self.status = False

    def __del__(self):
        pass

    def check_hbc_img_exist(self, date, hphm, kkdd):
        """查询当天黄标车图片是否存在，1天1个车牌号码只保存1张图片"""
        url = u'http://{0}:{1}/hbc/img/{2}/{3}/{4}'.format(
            self.host, self.port, date, hphm, kkdd)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.status = False
            raise

    def add_hbc(self, data):
        """添加黄标车信息"""
        url = u'http://{0}:{1}/hbc'.format(self.host, self.port)
        try:
            r = requests.post(url, headers=self.headers, data=json.dumps(data))
            if r.status_code == 201:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.status = False
            raise

    def get_hbc_img(self, kkdd):
        """获取违章黄标车路标图片"""
        url = u'http://{0}:{1}/wzimg/{2}'.format(
            self.host, self.port, kkdd)
        try:
            r = requests.get(url, headers=self.headers)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.status = False
            raise

    def get_kkdd(self, kkdd):
        """获取卡口地点代码"""
        url = u'http://{0}:{1}/kkdd/{2}'.format(
            self.host, self.port, kkdd)
        try:
            r = requests.get(url, headers=self.headers)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.status = False
            raise

    def get_white_list(self):
        """白名单"""
        url = u'http://{0}:{1}/whitelist'.format(self.host, self.port)
        try:
            r = requests.get(url, headers=self.headers)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.status = False
            raise     

##
##if __name__ == '__main__':
##    hs = HbcStore(**{'host': 123, 'cat': '345'})
    
