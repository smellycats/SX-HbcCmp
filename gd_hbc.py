# -*- coding: utf-8 -*-
import json

import requests


class GDHbc(object):
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

    def get_gdhbc_by_hphm(self, hphm, hpzl):
        """根据车牌号码，号牌种类获取六合一平台车辆信息"""
        url = u'http://{host}:{port}/hbc/{hphm}/{hpzl}'.format(
            host=self.host, port=self.port, hphm=hphm, hpzl=hpzl)
        try:
            r = requests.get(url, headers=self.headers)
            if r.status_code == 200:
                return json.loads(r.text)
            elif r.status_code == 404:
                return None
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.status = False
            raise

    def get_gdhbc_all(self):
        """获取所有黄标车信息"""
        url = u'http://{host}:{port}/hbc_all'.format(
            host=self.host, port=self.port)
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

    def get_gdhbc_all_by_hphm(self, hphm, hpzl):
        """根据车牌号码，号牌种类获取所有黄标车信息"""
        url = u'http://{host]}:{port}/hbc_all/{hphm}/{hpzl}'.format(
            host=self.host, self.port=port, hphm=hphm, hpzl=hpzl)
        try:
            r = requests.get(url, headers=self.headers)
            if r.status_code == 200:
                return json.loads(r.text)
            elif r.status_code == 404:
                return None
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.status = False
            raise
