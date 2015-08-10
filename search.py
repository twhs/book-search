#!/usr/bin/env python
# -*- coding:utf-8 -*-

from requests import Request, Session
from lxml import html

base_url = 'http://www.library.pref.okinawa.jp/'
search_path = 'wo/opc/srh/'
search_do_path = 'wo/opc/srh_do/'
search_detail_path = 'wo/opc/srh_detail'

search_req_params = {
    "auth": "",
    "pub" : "",
    "sort_item": "title",
    "sort_seq": "asc",
    "lines": 20,
    "req_max": "1000",
    "stype": "smp",
    "otype": "local",
    "dlang": "jpn",
    "tkbn": 1
}

def search(keyword):
    ss = Session()
    # 検索フォームのあるページヘアクセス 
    r = ss.get(base_url + search_path)

    # 検索フォームから検索
    req_params = search_req_params
    req_params['title'] = keyword
    req_params['_opcsid'] = r.cookies['_opcsid']
    r = ss.post(base_url + search_do_path, params=req_params)

    # レスポンスから検索結果一覧を抽出
    tree = html.fromstring(r.text)
    entries = tree.xpath('//table[@id="srh_kwd_hl"]/tr')[1:]
    for entry in entries:
        tds = entry.xpath('.//td')
        title = tds[1].xpath('.//text()')[0]
        author = tds[2].xpath('.//text()')[0]
        publisher = tds[3].xpath('.//text()')[0]
        print "%s/%s/%s" % (title, author, publisher)



if __name__ == '__main__':
    import sys
    search(sys.argv[1])
