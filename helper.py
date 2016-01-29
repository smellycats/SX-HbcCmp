# -*- coding: utf-8 -*-
import os
import shutil
from random import Random

import requests
from itsdangerous import Signer


def fix_hphm(hphm, hpys):
    if hphm != None and hphm != '-':
        header = hphm[:1] # 车牌头
        tail = hphm[-1] #车牌尾
        if header == u'粤':
            if tail == u'学':
                return {'hphm': hphm[1:], 'hpzl': '16', 'cpzl': u'标准车牌'}
            if hpys == 2 or hpys == u'BU': #蓝牌
                return {'hphm': hphm[1:], 'hpzl': '02', 'cpzl': u'标准车牌'}
            if hpys == 3 or hpys == u'YL': #黄牌
                return {'hphm': hphm[1:], 'hpzl': '01', 'cpzl': u'双层车牌'}
            if hpys == 5 or hpys == u'BK': #黑牌
                return {'hphm': hphm[1:], 'hpzl': '06', 'cpzl': u'标准车牌'}
    return {'hphm': hphm, 'hpzl': '00', 'cpzl': u'其他'}

def get_url_img(url, path):
    """根据URL地址抓图到本地文件"""
    r = requests.get(url, stream=True)

    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    # 非200响应,抛出异常
    r.raise_for_status()
    
def get_img(url, f):
    """根据URL地址抓图到本地文件"""
    r = requests.get(url, stream=True)
    #buf = StringIO.StringIO()
    if r.status_code == 200:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
    # 非200响应,抛出异常
    r.raise_for_status()

def random_str(randomlength=8):
    """生成随机字符串"""
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

def get_sign():
    """生成防伪码"""
    return Signer('hzhbc').sign(random_str(6))

def makedirs(path):
    """创建文件夹"""
    try:
        if os.path.isdir(path):
            pass
        else:
            os.makedirs(path)
    except IOError,e:
        raise

def hbc_img():
    img_dict = {
        (u'441302017', u'OT'): u'\u6885\u6e56\u8def\u6885\u6e56\u5361\u53e3_\u5f80\u6885\u6e56.jpg',
        (u'441302018', u'OT'): u'\u91d1\u9f99\u5927\u9053\u56db\u89d2\u697c\u5361\u53e3_\u5f80\u6cf0\u7f8e.jpg',
        (u'441302103', u'IN'): u'441302103_IN.jpg',
        (u'441302017', u'IN'): u'\u6885\u6e56\u8def\u6885\u6e56\u5361\u53e3_\u5f80\u4e0b\u89d2.jpg',
        (u'441302102', u'OT'): u'\u60e0\u57ce\u533a\u91d1\u949f\u8def\u7ba1\u59d4\u4f1a\u8def\u53e3_\u5f80\u6cf0\u8c6a\u8def.jpg',
        (u'441302006', u'IN'): u'\u4ef2\u607a\u533a\u56fd\u9053205\u7ebf\u9648\u6c5f\u4e0e\u9547\u9686\u4ea4\u754c\u5904\u5361\u53e3_\u5f80\u5e02\u533a.jpg',
        (u'441302026', u'IN'): u'\u60e0\u57ce\u533a\u53bf\u9053X205\u7ebf\u9a6c\u5b89\u67cf\u7530\u6865\u5361\u53e3_\u5f80\u67cf\u7530\u6865.jpg',
        (u'441302004', u'OT'): u'\u60e0\u535a\u8def\u4e0e\u4e09\u73af\u8def\u653e\u53e3\u5904\u5361\u53e3_\u5f80\u91d1\u5c71\u6c7d\u8f66\u57ce.jpg',
        (u'441302021', u'IN'): u'\u60e0\u57ce\u533aYG90\u7ebf\u5362\u6d32\u82a6\u6751\u5361\u53e3_\u5f80\u82a6\u5c9a.jpg',
        (u'441302022', u'IN'): u'\u60e0\u57ce\u533aX199\u5e7f\u4ecd\u516c\u8def\u4ecd\u56fe\u5361\u53e3_\u5f80\u60e0\u5dde.jpg',
        (u'441302025', u'IN'): u'\u60e0\u57ce\u533a\u53bf\u9053X205\u7ebf\u9a6c\u5b89\u9f99\u5858\u6865\u5361\u53e3_\u5f80\u9a6c\u5b89.jpg',
        (u'441302004', u'IN'): u'\u60e0\u535a\u8def\u4e0e\u4e09\u73af\u8def\u653e\u53e3\u5904\u5361\u53e3_\u535a\u7f57\u5f80\u4e09\u73af.jpg',
        (u'441302102', u'IN'): u'\u60e0\u57ce\u533a\u91d1\u949f\u8def\u7ba1\u59d4\u4f1a\u8def\u53e3_\u5f80\u4e09\u680b.jpg',
        (u'441302020', u'OT'): u'\u60e0\u57ce\u533a\u89c2\u5c9a\u5927\u6865\u82a6\u5c9a\u5361\u53e3_\u5f80\u89c2\u97f3\u9601.jpg',
        (u'441302006', u'OT'): u'\u4ef2\u607a\u533a\u56fd\u9053205\u7ebf\u9648\u6c5f\u4e0e\u9547\u9686\u4ea4\u754c\u5904\u5361\u53e3_\u5f80\u4ef2\u607a.jpg',
        (u'441302027', u'IN'): u'\u4e09\u73af\u897f\u8def\u4e30\u5c71\u5361\u53e3_\u5f80\u4e0b\u89d2.jpg',
        (u'441302106', u'IN'): u'\u60e0\u57ce\u533a\u60e0\u6cfd\u5927\u9053\u534e\u9633\u5de5\u4e1a\u533a\u5361\u53e3_\u5f80\u4e09\u73af.jpg',
        (u'441302019', u'IN'): u'\u6c38\u8054\u8def\u706b\u8f66\u897f\u7ad9\u5361\u53e3_\u897f\u7ad9.jpg',
        (u'441302027', u'OT'): u'\u4e09\u73af\u897f\u8def\u4e30\u5c71\u5361\u53e3_\u5f80\u897f\u7ad9.jpg',
        (u'441302024', u'OT'): u'\u60e0\u57ce\u533a\u53bf\u9053208\u7ebf\u6a2a\u6ca5\u5361\u53e3_\u5f80\u6881\u5316.jpg',
        (u'441302021', u'OT'): u'\u60e0\u57ce\u533aYG90\u7ebf\u5362\u6d32\u82a6\u6751\u5361\u53e3_\u5f80\u82a6\u6751.jpg',
        (u'441302015', u'OT'): u'\u60e0\u6c11\u5927\u9053\u5174\u6e56\u4e00\u8def\u5361\u53e3_\u5f80\u6c5d\u6e56.jpg',
        (u'441302105', u'IN'): u'\u60e0\u57ce\u533a\u53bf\u9053205\u7ebf\u4e1c\u6c5f\u9ad8\u65b0\u533a\u5317\u5357\u53e3_\u5f80\u6c34\u53e3.jpg',
        (u'441302007', u'OT'): u'\u5c0f\u91d1\u53e3\u5361\u53e3_\u5f80\u6c64\u6cc9.jpg',
        (u'441302104', u'OT'): u'\u60e0\u57ce\u533a\u53bf\u9053205\u7ebf\u4e1c\u6c5f\u9ad8\u65b0\u533a\u5317\u5361\u53e3_\u5f80\u9a6c\u5b89.jpg',
        (u'441302105', u'OT'): u'\u60e0\u57ce\u533a\u53bf\u9053205\u7ebf\u4e1c\u6c5f\u9ad8\u65b0\u533a\u5317\u5357\u53e3_\u5f80\u9a6c\u5b89.jpg',
        (u'441302010', u'OT'): u'\u60e0\u57ce\u533a\u9a6c\u5b89\u6cf0\u5b89\u8def\u9a6c\u5b89\u5361\u53e3_\u5f80\u60e0\u4e1c.jpg',
        (u'441302018', u'IN'): u'\u91d1\u9f99\u5927\u9053\u56db\u89d2\u697c\u5361\u53e3_\u5f80\u60e0\u5dde.jpg',
        (u'441302008', u'IN'): u'\u4ef2\u607a\u533a\u4ef2\u607a\u5927\u9053\u5bcc\u5ddd\u745e\u56ed\u5361\u53e3_\u5f80\u5e02\u533a.jpg',
        (u'441302023', u'IN'): u'\u60e0\u57ce\u533a\u7701\u9053120\u7ebf\u5927\u5c9a\u8001\u6536\u8d39\u7ad9\u524d\u5361\u53e3_\u5f80\u6a2a\u6ca5.jpg',
        (u'441302011', u'OT'): u'\u4ef2\u607a\u533a\u7701\u9053357\u7ebf\u9648\u6c5f\u68a7\u6751\u5361\u53e3_\u5f80\u4ef2\u607a.jpg',
        (u'441302015', u'IN'): u'\u60e0\u6c11\u5927\u9053\u5174\u6e56\u4e00\u8def\u5361\u53e3_\u5f80\u60e0\u5dde.jpg',
        (u'441302014', u'OT'): u'\u4ef2\u607a\u533a\u7701\u9053120\u7ebf\u672a\u6f7c\u6865\u5361\u53e3_\u5f80\u4ef2\u607a.jpg',
        (u'441302008', u'OT'): u'\u4ef2\u607a\u533a\u4ef2\u607a\u5927\u9053\u5bcc\u5ddd\u745e\u56ed\u5361\u53e3_\u5f80\u4ef2\u607a.jpg',
        (u'441302009', u'IN'): u'441302009_IN.jpg',
        (u'441302011', u'IN'): u'\u4ef2\u607a\u533a\u7701\u9053357\u7ebf\u9648\u6c5f\u68a7\u6751\u5361\u53e3_\u5f80\u5e02\u533a.jpg',
        (u'441302025', u'OT'): u'\u60e0\u57ce\u533a\u53bf\u9053X205\u7ebf\u9a6c\u5b89\u9f99\u5858\u6865\u5361\u53e3_\u5f80\u826f\u4e95.jpg',
        (u'441302020', u'IN'): u'\u60e0\u57ce\u533a\u89c2\u5c9a\u5927\u6865\u82a6\u5c9a\u5361\u53e3_\u5f80\u82a6\u5c9a.jpg',
        (u'441302014', u'IN'): u'\u4ef2\u607a\u533a\u7701\u9053120\u7ebf\u672a\u6f7c\u6865\u5361\u53e3_\u5f80\u5e02\u533a.JPG',
        (u'441302009', u'OT'): u'\u60e0\u57ce\u533a\u7701\u9053120\u7ebf\u6c34\u53e3\u5361\u53e3_\u5f80\u5357\u65cb.jpg',
        (u'441302010', u'IN'): u'\u60e0\u57ce\u533a\u9a6c\u5b89\u6cf0\u5b89\u8def\u9a6c\u5b89\u5361\u53e3_\u5f80\u9a6c\u5b89.jpg',
        (u'441302019', u'OT'): u'\u6c38\u8054\u8def\u706b\u8f66\u897f\u7ad9\u5361\u53e3_\u5f80\u9ad8\u901f\u516c\u8def.jpg',
        (u'441302023', u'OT'): u'\u60e0\u57ce\u533a\u7701\u9053120\u7ebf\u5927\u5c9a\u8001\u6536\u8d39\u7ad9\u524d\u5361\u53e3_\u5f80\u7d2b\u91d1.jpg',
        (u'441302022', u'OT'): u'\u60e0\u57ce\u533aX199\u5e7f\u4ecd\u516c\u8def\u4ecd\u56fe\u5361\u53e3_\u5f80\u4ecd\u56fe.jpg',
        (u'441302007', u'IN'): u'\u5c0f\u91d1\u53e3\u5361\u53e3_\u5f80\u60e0\u5dde.jpg',
        (u'441302103', u'OT'): u'\u60e0\u57ce\u533a\u60e0\u6cfd\u5927\u9053\u5357\u65cb\u5de5\u4e1a\u533a\u5361\u53e3_\u5f80\u5357\u65cb.jpg',
        (u'441302013', u'IN'): u'\u60e0\u57ce\u533a\u60e0\u5357\u5927\u9053\u60e0\u6de1\u8def\u5361\u53e3_\u5f80\u5e02\u533a.jpg',
        (u'441302024', u'IN'): u'\u60e0\u57ce\u533a\u53bf\u9053208\u7ebf\u6a2a\u6ca5\u5361\u53e3_\u5f80\u6a2a\u6ca5.jpg',
        (u'441302013', u'OT'): u'\u60e0\u57ce\u533a\u60e0\u5357\u5927\u9053\u60e0\u6de1\u8def\u5361\u53e3_\u5f80\u6de1\u6c34.jpg',
        (u'441302104', u'IN'): u'\u60e0\u57ce\u533a\u53bf\u9053205\u7ebf\u4e1c\u6c5f\u9ad8\u65b0\u533a\u5317\u5361\u53e3_\u5f80\u6c34\u53e3.jpg',
        (u'441302026', u'OT'): u'\u60e0\u57ce\u533a\u53bf\u9053X205\u7ebf\u9a6c\u5b89\u67cf\u7530\u6865\u5361\u53e3_\u5f80\u60e0\u5dde\u5927\u9053.jpg',
        (u'441302106', u'OT'): u'\u60e0\u57ce\u533a\u60e0\u6cfd\u5927\u9053\u534e\u9633\u5de5\u4e1a\u533a\u5361\u53e3_\u5f80\u5357\u65cb.jpg',
        (u'441302001', u'OT'): u'\u4e1c\u6e56\u897f\u8def_\u5f80\u65b0\u5f00\u6cb3\u6865.jpg',
        (u'441302001', u'IN'): u'\u4e1c\u6e56\u897f\u8def_\u5f80\u897f\u679d\u6c5f.jpg',
        (u'441302002', u'IN'): u'441302002_IN.jpg',
        (u'441302002', u'OT'): u'\u60e0\u57ce\u533a\u60e0\u5dde\u5927\u9053\u957f\u6e56\u5317\u8def\u8def\u6bb5_\u5f80\u9a6c\u5b89.jpg',
        (u'441302003', u'IN'): u'\u60e0\u57ce\u533a\u60e0\u5dde\u5927\u9053\u4e1c\u6c5f\u5927\u6865\u5361\u53e3_\u5f80\u4e1c\u5e73.jpg',
        (u'441302003', u'OT'): u'\u60e0\u57ce\u533a\u60e0\u5dde\u5927\u9053\u4e1c\u6c5f\u5927\u6865\u5361\u53e3_\u5f80\u6c5f\u5317.jpg',
        (u'441302005', u'IN'): u'\u60e0\u57ce\u533a\u60e0\u6c99\u5824\u4e8c\u8def\u4e09\u73af\u8def\u5361\u53e3_\u5f80\u6cb3\u5357\u5cb8.jpg',
        (u'441302005', u'OT'): u'\u60e0\u57ce\u533a\u60e0\u6c99\u5824\u4e8c\u8def\u4e09\u73af\u8def\u5361\u53e3_\u5f80\u4e09\u73af.jpg',
        (u'441302016', u'OT'): u'\u60e0\u57ce\u533a\u9cc4\u6e56\u8def\u5361\u53e3_\u5f80\u7ea2\u82b1\u6e56.jpg',
        (u'441302016', u'IN'): u'\u60e0\u57ce\u533a\u9cc4\u6e56\u8def\u5361\u53e3_\u5f80\u6c5f\u5317.jpg',
        
        (u'441303002', u'IN'): u'\u6c38\u6e56\u9ebb\u6eaa\u6751\u91d1\u679c\u6e7e\u5ea6\u5047\u533a\u8def\u53e3.jpg',
        (u'441303014', u'IN'): u'\u6c99\u7530\u82b1\u5858\u6751\u4e07\u5229\u5851\u80f6\u5382\u95e8\u53e3 .jpg',
        (u'441303034', u'IN'): u'\u5e73\u6f6d\u4e4c\u5858\u6865\u8ddd\u5e7f\u60e0\u9ad8\u901f600\u7c73\u5904.jpg',
        (u'441303005', u'IN'): u'\u6c38\u6e56\u56ed\u5cad\u6751\u53e3_\u5f80\u60e0\u9633\u60e0\u5357\u5927\u9053.jpg',
        (u'441303008', u'IN'): u'\u65b0\u5729\u5357\u5751\u6751\u4e0e\u576a\u5730\u4ea4\u754c\u5904.jpg',
        (u'441303033', u'IN'): u'\u79cb\u957f\u5927\u77f3\u9f13\u91d1\u6e56\u8def\u6df1\u6c55\u9ad8\u901f\u6db5\u6d1e\u65c1.jpg',
        (u'441303035', u'IN'): u'\u6de1\u6c34\u7231\u6c11\u8def\u53a6\u6df1\u94c1\u8def\u60e0\u5dde\u5357\u7ad9\u5165\u53e3\u5904_\u7231\u6c11\u6865\u5934\u5f80\u60e0\u5dde\u5357\u7ad9.jpg',
        (u'441303028', u'IN'): u'\u767d\u4e91\u516d\u8def\u9a6c\u6e9c\u5cad\u6bb5_\u6c99\u7530\u9547\u5f80\u6de1\u6c34.jpg',
        (u'441303004', u'IN'): u'\u826f\u767d\u516c\u8def\u65f6\u5316\u6751\u8def\u6bb5.jpg',
        (u'441303019', u'OT'): u'S358\u6de1\u6c34\u4eba\u6c11\u6865\u4e0e\u6df1\u6c55\u9ad8\u901f\u6865\u6d1e\u4ea4\u6c47\u5904.jpg',
        (u'441303015', u'IN'): u'\u79cb\u957f\u767d\u77f3\u6d1e\u6751\u4f9b\u6c34\u69fd\u4e0b.jpg',
        (u'441303012', u'IN'): u'\u9547\u9686\u8054\u6eaa\u6751\u91d1\u65f6\u53d1\u8def\u53e3_\u5f80\u5e73\u5357\u8f66\u7ba1\u6240\u65b9\u5411.jpg',
        (u'441303010', u'IN'): u'\u65b0\u5729\u7ea2\u7530\u6751\u51a0\u8363\u5382\u95e8\u53e3\u6e05\u6eaa\u4ea4\u754c\u5904.jpg',
        (u'441303017', u'IN'): u'\u79cb\u5b9d\u8def\u767d\u77f3\u533b\u9662\u95e8\u53e3.jpg',
        (u'441303001', u'IN'): u'\u6f6e\u839e\u9ad8\u901f\u826f\u4e95\u51fa\u5165\u53e3\u5904.jpg',
        (u'441303003', u'IN'): u'\u6c38\u6e56\u7a3b\u56ed\u6751\u53e3.jpg',
        (u'441303016', u'IN'): u'\u79cb\u957f\u897f\u6e56\u6751\u897f\u6e56\u6865\u65c1\u73af\u57ce\u897f\u8def.jpg',
        (u'441303025', u'IN'): u'\u65b0\u5729\u957f\u5e03\u6751\u963f\u9e4a\u6c34\u6865300\u7c73\u5904.jpg',
        (u'441303023', u'IN'): u'\u6de1\u6c34\u6d77\u5173\u767d\u4e91\u4e8c\u8def\u534e\u4e3d\u978b\u4e1a\u8def\u53e3\u5904_\u6df1\u5733\u5f80\u6de1\u6c34.jpg',

        (u'441305018', u'OT'): u'\u6cbf\u6d77\u5c0f\u5f84\u6e7e\u9ad8\u901f\u51fa\u53e3\u5361\u53e3_\u51fa.jpg',
        (u'441305032', u'OT'): u'\u6cbf\u6cb3\u8def\u897f\u4e00\u53f7\u8def\u5361\u53e3_\u51fa.jpg',
        (u'441305003', u'OT'): u'\u4eba\u6c11\u516d\u8def_\u897f\u533a\u6bb5\u5361\u53e3_\u51fa.jpg',
        (u'441305010', u'IN'): u'\u6cbf\u6d77\u9ad8\u901f\u6fb3\u5934\u6536\u8d39\u7ad9_\u5165.jpg',
        (u'441305017', u'OT'): u'\u6cbf\u6d77\u971e\u6d8c\u9ad8\u901f\u51fa\u53e3\u5361\u53e3_\u51fa.jpg',
        (u'441305026', u'OT'): u'\u77f3\u5316\u5927\u9053\u6a1f\u6811\u57d4\u6865\u5361\u53e3_\u51fa.jpg',
        (u'441305019', u'OT'): u'\u6cbf\u6d77\u9ad8\u901f\u77f3\u5316\u533a\u51fa\u53e3\u5361\u53e3_\u51fa.jpg',
        (u'441305026', u'IN'): u'\u77f3\u5316\u5927\u9053\u6a1f\u6811\u57d4\u6865\u5361\u53e3_\u516502.jpg',
        (u'441305012', u'OT'): u'\u9f99\u6d77\u4e8c\u8def_\u51fa.jpg',
        (u'441305002', u'OT'): u'\u5858\u6a2a\u4e0e\u6df1\u5733\u4ea4\u754c\u5904\u5361\u53e3_\u51fa.jpg',
        (u'441305017', u'IN'): u'\u6cbf\u6d77\u971e\u6d8c\u9ad8\u901f\u51fa\u53e3\u5361\u53e3_\u5165.jpg',
        (u'441305023', u'OT'): u'\u4e2d\u5174\u4e2d\u8def\u6865\u5361\u53e3_\u51fa.jpg',
        (u'441305011', u'IN'): u'\u5f00\u57ce\u5927\u9053_\u897f\u533a\u6bb5\u5361\u53e3_\u5165.jpg',
        (u'441305021', u'IN'): u'\u9f99\u6d77\u4e00\u8def\u5361\u53e3_\u5165.jpg',
        (u'441305023', u'IN'): u'\u4e2d\u5174\u4e2d\u8def\u6865\u5361\u53e3_\u516502.jpg',
        (u'441305012', u'IN'): u'\u9f99\u6d77\u4e8c\u8def_\u5165.jpg',
        (u'441305014', u'IN'): u'\u5317\u73af\u8def_\u516502.jpg',
        (u'441305020', u'IN'): u'\u9f99\u6d77\u4e00\u8def\u5361\u53e3_\u539f\u60e0\u6fb3\u5927\u9053\u4e30\u7530\u6c34\u5e93_\u5165.jpg',
        (u'441305014', u'OT'): u'\u5317\u73af\u8def_\u51fa.jpg',
        (u'441305013', u'IN'): u'\u77f3\u5316\u5927\u9053\u897f\u5361\u53e3_\u516502.jpg',
        (u'441305010', u'OT'): u'\u6cbf\u6d77\u9ad8\u901f\u6fb3\u5934\u6536\u8d39\u7ad9_\u51fa.jpg',
        (u'441305013', u'OT'): u'\u77f3\u5316\u5927\u9053\u897f\u5361\u53e3_\u51fa.jpg',
        (u'441305003', u'IN'): u'\u4eba\u6c11\u516d\u8def_\u897f\u533a\u6bb5\u5361\u53e3_\u5165.jpg',
        (u'441305015', u'IN'): u'\u897f\u5357\u5927\u9053\u5361\u53e3_\u516502.jpg',
        (u'441305021', u'OT'): u'\u9f99\u6d77\u4e00\u8def\u5361\u53e3_\u51fa.jpg',
        (u'441305015', u'OT'): u'\u897f\u5357\u5927\u9053\u5361\u53e3_\u51fa.jpg',
        (u'441305018', u'IN'): u'\u6cbf\u6d77\u5c0f\u5f84\u6e7e\u9ad8\u901f\u51fa\u53e3\u5361\u53e3_\u5165.jpg',
        (u'441305031', u'OT'): u'\u6cbf\u6cb3\u8def\u6d77\u60e0\u5361\u53e3_\u51fa.jpg',
        (u'441305031', u'IN'): u'\u6cbf\u6cb3\u8def\u6d77\u60e0\u5361\u53e3_\u5165.jpg',
        (u'441305011', u'OT'): u'\u5f00\u57ce\u5927\u9053_\u897f\u533a\u6bb5\u5361\u53e3_\u51fa.jpg',
        (u'441305002', u'IN'): u'\u5858\u6a2a\u4e0e\u6df1\u5733\u4ea4\u754c\u5904\u5361\u53e3_\u5165.jpg',
        (u'441305020', u'OT'): u'\u9f99\u6d77\u4e00\u8def\u5361\u53e3_\u539f\u60e0\u6fb3\u5927\u9053\u4e30\u7530\u6c34\u5e93_\u51fa.jpg',
        (u'441305019', u'IN'): u'\u6cbf\u6d77\u9ad8\u901f\u77f3\u5316\u533a\u51fa\u53e3\u5361\u53e3_\u5165.jpg',
        (u'441305032', u'IN'): u'\u6cbf\u6cb3\u8def\u897f\u4e00\u53f7\u5361\u8def\u53e3_\u5165.jpg',

        (u'441323001', u'IN'): u'\u7a14\u5c71\u5927\u57d4\u5c6f\u8def\u6bb52_\u8fdb.jpg',
        (u'441323009', u'OT'): u'\u9ec4\u57e0\u5c0f\u6f20_\u51fa.jpg',
        (u'441323006', u'OT'): u'\u5e73\u6d77\u5be8\u5934\u57732_\u51fa.jpg',
        (u'441323010', u'IN'): u'\u9ad8\u8c2d\u4f9b\u5e73\u8def\u53e32_\u8fdb.jpg',
        (u'441323009', u'IN'): u'\u9ec4\u57e0\u5c0f\u6f202_\u8fdb.jpg',
        (u'441323007', u'IN'): u'\u5409\u9ec4\u5927\u90532_\u8fdb.jpg',
        (u'441323012', u'OT'): u'\u767d\u82b1\u524d\u8fdb\u4e2d\u5b661_\u51fa.jpg',
        (u'441323005', u'IN'): u'\u5409\u9686\u767d\u4e91\u4ed42_\u8fdb.jpg',
        (u'441323010', u'OT'): u'\u9ad8\u8c2d\u5f80\u6c55\u5c3e_\u51fa.jpg',
        (u'441323005', u'OT'): u'\u5409\u9686\u5f80\u6c55\u5c3e_\u51fa.jpg',
        (u'441323008', u'OT'): u'\u767d\u82b1\u6f20\u5cad_\u51fa.jpg',
        (u'441323001', u'OT'): u'\u7a14\u5c71\u5927\u57d4\u5c6f\u8def\u6bb52_\u51fa.jpg',
        (u'441323007', u'OT'): u'\u5409\u9ec4\u5927\u90532_\u51fa.jpg',
        (u'441323003', u'OT'): u'\u5927\u5cad\u5341\u4e8c\u62582_\u51fa.jpg',
        (u'441323003', u'IN'): u'S356\u7ebf\u4e0e\u60e0\u9633\u4ea4\u754c_\u8fdb.jpg',
        (u'441323008', u'IN'): u'\u767d\u82b1\u6f20\u5cad2_\u8fdb.jpg',
        (u'441323012', u'IN'): u'\u767d\u82b1\u524d\u8fdb\u4e2d\u5b661_\u8fdb.jpg',
        (u'441323006', u'IN'): u'\u5e73\u6d77\u5be8\u5934\u57732_\u8fdb.jpg',

        (u'441324005', u'IN'): u'\u7701\u9053S244\u7ebf\u9f99\u95e8\u53bf\u84dd\u7530\u4e61\u5bc6\u6eaa\u6797\u573a\u8def\u53e3_\u65b0\u4e30\u5f80\u9f99\u95e8.jpg',
        (u'441324003', u'IN'): u'\u9f99\u95e8\u53bfX218\u7ebf\u8def\u6eaa\u9547\u5f80\u516c\u5e84_\u516c\u5e84\u5f80\u8def\u6eaa.jpg',
        (u'441324001', u'IN'): u'\u9f99\u95e8\u53bf\u5e73\u9675\u9547\u91d1\u9f99\u5927\u9053_\u60e0\u5dde\u5f80\u9f99\u95e8.jpg',
        (u'441324010', u'IN'): u'\u7701\u9053S244\u7ebf\u9f99\u95e8\u53bf\u9f99\u7530\u9547\u897f\u57d4\u6751\u8def\u6bb5_\u84dd\u7530\u5f80\u9f99\u95e8.jpg',
        (u'441324002', u'IN'): u'\u7701\u9053S353\u7ebf\u9f99\u95e8\u53bf\u5730\u6d3e\u9547_\u4ece\u5316\u5f80\u9f99\u95e8.jpg',
        (u'441324009', u'IN'): u'\u7701\u9053S353\u7ebf\u60e0\u5dde\u5e02\u9f99\u95e8\u53bf\u9f99\u57ce\u8857\u9053\u9e2c\u9e5a\u8def\u6bb5_\u9f99\u6f6d\u5f80\u9f99\u95e8.jpg',
        (u'441324007', u'IN'): u'\u9f99\u95e8\u53bf\u57ce\u91d1\u9f99\u5927\u9053\u91d1\u6cb3\u6e7e\u5c0f\u533a\u95e8\u524d\u8def\u6bb5_\u5f80\u535a\u7f57.jpg',
        (u'441324008', u'IN'): u'\u7701\u9053S119\u7ebf\u9f99\u95e8\u53bf\u6c38\u6c49\u9547\u7ea2\u661f\u6751\u8def\u6bb5_\u5e7f\u5dde\u5f80\u9f99\u95e8.jpg',
        (u'441324004', u'IN'): u'\u5357\u6606\u5c71\u5361\u53e3355\u7701\u905323\u516c\u91cc100\u7c73.jpg'
    }
    return img_dict

