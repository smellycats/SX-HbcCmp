# -*- coding: utf-8 -*-
import arrow

from hbc_store import HbcStore


def test_add_hbc():
    hs = HbcStore(**{'host': '127.0.0.1', 'port': 5000})
    data = {
        'jgsj': '2016-03-15 10:26:34',
        'hphm': u'粤L12345',
        'kkdd_id': '441302002',
        'hpys_code': 'BU',
        'fxbh_code': 'IN',
        'cdbh': 2,
        'imgurl': 'http://test/123.jpg',
        'imgpath': 'd://test/123.jpg'
    }
    hs.add_hbc(data)
    del hs

def test_check_hbc_img_exist():
    hs = HbcStore(**{'host': '127.0.0.1', 'port': 5000})
    date = '2016-03-15'
    hphm = u'粤L12345'
    kkdd = '441302'
    print hs.check_hbc_img_exist(date, hphm, kkdd)
    del hs

def test_get_hbc_img():
    hs = HbcStore(**{'host': '127.0.0.1', 'port': 5000})
    print hs.get_hbc_img('441303')
    del hs

def test_get_kkdd():
    hs = HbcStore(**{'host': '127.0.0.1', 'port': 5000})
    print hs.get_kkdd('441303')
    del hs

def test_get_white_list():
    hs = HbcStore(**{'host': '127.0.0.1', 'port': 5000})
    print hs.get_white_list()
    del hs

if __name__ == '__main__':
    #test_add_hbc()
    test_check_hbc_img_exist()
    test_get_hbc_img()
    test_get_kkdd()
    test_get_white_list()
