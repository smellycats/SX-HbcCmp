# -*- coding: utf-8 -*-
import os
import time
import json
import Queue
import logging
import threading

import arrow
import requests
#from PIL import Image

import helper
import helper_wm
import img_builder
from ini_conf import MyIni
from my_logger import debug_logging
from application import app

debug_logging(u'logs/error.log')

logger = logging.getLogger('root')


class HbcCompare(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.myini = MyIni()
        self.hbc_conf = self.myini.get_hbc()

        self.cgs_ini = {'host': '10.47.222.51', 'port': 8084,
                        'username': 'test1', 'password': 'test12345'}
        self.hbc_ini = {'host': '10.47.222.51', 'port': 8083,
                        'username': 'test1', 'password': 'test12345'}

        self.cgs_status = False
        self.hbc_status = False
        # 黄标车集合 dict
        self.gdhbc_dict = {}
        # 号牌颜色字典 dict
        self.hpys_dict = {
            'WT': u'白底黑字',
            'YL': u'黄底黑字',
            'BU': u'蓝底白字',
            'BK': u'黑底白字',
            'QT': u'其他'
        }
        # 机号字典 dict
        self.jh_dict = {}
        # 设备代号 dict
        self.sbdh_dict = {}
        # 方向编号 dict
        self.fxbh_dict = {
            'NS': u'北向南',
            'SN': u'南向北',
            'EW': u'东向西',
            'WE': u'西向东',
            'IN': u'东向西',
            'OT': u'西向东'
        }
        self.city_dict = {
            '441302': u'惠州市惠城区',
            '441303': u'惠州市惠阳区',
            '441305': u'惠州市大亚湾',
            '441322': u'惠州市博罗县',
            '441323': u'惠州市惠东县',
            '441324': u'惠州市龙门县',
        }
        self.hbc_img_path = self.hbc_conf['hbc_img_path']#u'd://videoandimage'
        self.wz_img_path = self.hbc_conf['wz_img_path']
        #self.hbc_img_dict = {}
        self.hbc_img_dict = helper.hbc_img()

    def __del__(self):
        print 'quit cmp_hbc'
        
    def get_gdhbc_by_hphm(self, hphm, hpzl):
        headers = {
            'content-type': 'application/json'
        }
        url = u'http://{0[host]}:{0[port]}/hbc/{hphm}/{hpzl}'.format(
            self.cgs_ini, hphm=hphm, hpzl=hpzl)
        try:
            r = requests.get(url, headers)
            #print r.text
            if r.status_code == 200:
                return json.loads(r.text)
            elif r.status_code == 404:
                return None
            else:
                self.cgs_status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            #print e
            self.cgs_status = False
            raise

    def get_gdhbc_all(self):
        headers = {
            'content-type': 'application/json'
        }
        url = u'http://{0[host]}:{0[port]}/hbc_all'.format(self.cgs_ini)
        try:
            r = requests.get(url, headers)
            if r.status_code == 200:
                items = json.loads(r.text)['items']
                print 'hbc_num:%s' % len(items)
                for i in items:
                    self.gdhbc_dict[(i['hphm'], i['hpzl'])] = i['ccdjrq']
            else:
                self.cgs_status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.cgs_status = False
            raise

    def get_kkdd(self, kkdd):
        """获取卡口地点代码"""
        url = u'http://{0[host]}:{0[port]}/kkdd/{1}'.format(
            self.hbc_ini, kkdd)
        headers = {
            'content-type': 'application/json'
        }
        try:
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                items = json.loads(r.text)['items']
                for i in items:
                    self.jh_dict[i['kkdd_id']] = i['cf_id']
                    self.sbdh_dict[i['kkdd_id']] = i['sbdh']
            else:
                self.hbc_status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.hbc_status = False
            raise

    def get_hbc_img(self, kkdd):
        """获取违章黄标车路标图片"""
        url = u'http://{0[host]}:{0[port]}/wzimg/{1}'.format(
            self.hbc_ini, kkdd)
        headers = {
            'content-type': 'application/json'
        }
        try:
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                for i in json.loads(r.text)['items']:
                    self.hbc_img_dict[(i['kkdd_id'], i['fxbh_code'])] = os.path.join(self.wz_img_path, kkdd, i['mg_path'])
            else:
                self.hbc_status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.hbc_status = False
            raise

    def check_hbc_img_exist(self, date, hphm, kkdd):
        """查询当天黄标车图片是否存在，1天1个车牌号码只保存1张图片"""
        headers = {
            'content-type': 'application/json'
        }
        url = u'http://{0[host]}:{0[port]}/hbc/img/{1}/{2}/{3}'.format(
            self.hbc_ini, date, hphm, kkdd)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.hbc_status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.hbc_status = False
            raise

    def check_hbc(self, hphm, hpzl):
        """检测是否黄标车"""
        ccdjrq = self.gdhbc_dict.get((hphm, hpzl), None)
        if not ccdjrq:
            return False
        #print hphm, ccdjrq
        h = self.get_gdhbc_by_hphm(hphm, hpzl)
        if not h:
            return False

        if arrow.get(ccdjrq).date() != arrow.get(h['ccdjrq']).date():
            return False
        return True

    def add_hbc(self, data):
        """添加黄标车信息"""
        url = u'http://{0[host]}:{0[port]}/hbc'.format(self.hbc_ini)
        headers = {
            'content-type': 'application/json'
        }
        try:
            r = requests.post(url, headers=headers, data=json.dumps(data))
            if r.status_code == 201:
                return json.loads(r.text)
            else:
                self.hbc_status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.hbc_status = False
            raise

    def cmpare_hbc(self, i):
        """根据车辆信息比对黄标车"""
        # 机号不存在则退出
        if not self.jh_dict.get(i['kkdd_id'], None):
            return
        # 判断车牌是否需要黄标车查询
        f_hphm = helper.fix_hphm(i['hphm'], i['hpys_code'])
        if f_hphm['hpzl'] == '00':
            return
        # 是否在黄标车集合里面
        if not self.check_hbc(f_hphm['hphm'], f_hphm['hpzl']):
            return
        jgsj = arrow.get(i['jgsj'])
        #print u'黄表车: %s, 号牌颜色: %s' % (i['hphm'], i['hpys'])
        # 判断黄标车图片是否存在
        hbc_img = self.check_hbc_img_exist(
            jgsj.format('YYYY-MM-DD'), i['hphm'], i['kkdd_id'][:6])

        imgpath = ''
        if hbc_img['total_count'] == 0:
            try:
                path = u'{0}/{1}/违章图片目录'.format(
                    self.hbc_img_path, jgsj.format(u'YYYY年MM月DD日'))
                # 图片名称
                name = u'机号%s车道A%s%sR454DOK3T%sC%sP%s驶向%s违章黄标车违反禁令标志' % (
                    self.jh_dict[i['kkdd_id']], i['cdbh'],
                    jgsj.format(u'YYYY年MM月DD日HH时mm分ss秒'),
                    f_hphm['cpzl'], self.hpys_dict[i['hpys_code']],
                    i['hphm'], self.fxbh_dict.get(i['fxbh_code'], u'其他'))
                # 水印内容
                text = u'违法时间:%s 违法地点:%s%s\n违法代码:13441 违法行为:违章黄标车 设备编号:%s\n防伪码:%s' % (
                    i['jgsj'], self.city_dict[i['kkdd_id'][:6]], i['kkdd'],
                    self.sbdh_dict[i['kkdd_id']], helper.get_sign())
                # 违章路标图片
                wz_img = self.hbc_img_dict.get((i['kkdd_id'], i['fxbh_code']), None)
                if wz_img is not None:
                    wz_img = u'{0}/{1}/{2}'.format(self.wz_img_path,
                                                   i['kkdd_id'][:6], wz_img)
                imgpath = img_builder.get_img_by_url(
                    i['imgurl'], path, name, text, wz_img)
            except Exception as e:
                logger.error('url: %s' % i['imgurl'])
                logger.error(e)
                imgpath = ''
        #print 'test123'
        data = {
            'jgsj': i['jgsj'],
            'hphm': i['hphm'],
            'kkdd_id': i['kkdd_id'],
            'hpys_code': i['hpys_code'],
            'fxbh_code': i['fxbh_code'],
            'cdbh': i['cdbh'],
            'imgurl': i['imgurl'],
            'imgpath': imgpath
        }
        # 添加黄标车信息到数据库
        self.add_hbc(data)

    def fetch_data(self):
        """获取卡口车辆信息"""
        #print 'fetch_data'
        try:
            carinfo = app.config['QUE'].get(timeout=1)
            for i in carinfo:
                if i['kkdd_id'] is not None:
                    self.cmpare_hbc(i)
        except Queue.Empty:
            pass

    def run(self):
        print 'run!!'
        # 时间戳标记
        time_flag = time.time()
        # 加载初始化数据
        init_flag = False
        while 1:
            #print 'test'
            if app.config['QUE'].qsize() == 0 and app.config['IS_QUIT']:
                break
            if not init_flag:
                try:
                    # 获取黄标车数据
                    self.get_gdhbc_all()
                    self.cgs_status = True
                    # 获取卡口地点数据和违章路标图片
                    for i in self.city_dict.keys():
                        self.get_kkdd(i)
                        #self.get_hbc_img(i)
                    self.hbc_status = True

                    init_flag = True
                    #print 'Init Finish'
                except Exception as e:
                    #print e
                    logger.error(e)
                    time.sleep(1)
            elif self.cgs_status and self.hbc_status:
                try:
                    # 当前时间大于时间戳标记时间2小时则更新黄标车数据
                    if time.time() - time_flag > 3600:
                        self.get_gdhbc_all()
                        time_flag = time.time()
                    self.fetch_data()
                except Exception as e:
                    print e
                    logger.error(e)
                    time.sleep(1)
            else:
                try:
                    if not self.cgs_status:
                        self.get_gdhbc_by_hphm(u'L12345', '02')
                        self.cgs_status = True
                    if not self.hbc_status:
                        self.check_hbc_img_exist('2015-09-26', u'粤L12345', '441302')
                        self.hbc_status = True
                except Exception as e:
                    #print (e)
                    time.sleep(1)


if __name__ == "__main__":
    hbc = HbcCompare()
    hbc.get_hbc_img()
    del hbc

