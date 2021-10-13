# -*- coding:utf-8 -*-
import requests
from lxml import etree
import pymysql
import datetime
from .spider_config import *

conn = pymysql.connect(host=HOST,
                       user=USER,
                       password=PASSWORD,
                       database=DATABASE,
                       charset='utf8',
                       port=PORT)


class ZhihuHot:
    def __init__(self):
        self.url = 'https://www.zhihu.com/hot'
        self.headers = {
            'user-agent': user_agent,
            'cookie': cookie
        }
        self.proxies = {
            'http': 'http://122.114.31.177:808'
        }

    def download_item(self):
        try:
            resp = requests.get(self.url, headers=self.headers, allow_redirects=False, proxies=self.proxies)
            if resp.status_code == 200:
                resp.encoding = 'utf-8'
                return resp.text
        except Exception as e:
            print(e)

    def clear_item(self, html):
        html = etree.HTML(html)
        query_list = html.xpath("//div[@class='HotItem-content']")
        hot_list = []

        for index, data in enumerate(query_list):
            item_title = data.xpath(".//h2[@class='HotItem-title']/text()")[0]
            item_url = data.xpath(".//a/@href")[0]
            item_title = str(index) + ':' + item_title
            hot_dict = {'title': item_title, 'url': item_url}
            hot_list.append(hot_dict)
        return hot_list

    def save_item(self, items):
        create_time = datetime.datetime.utcnow()
        try:
            for data in items:
                with conn.cursor() as cursor:
                    sql = '''insert into zhihu_hot(title, title_url, create_time, del_flag) values(%s,%s,%s,%s)'''
                    cursor.execute(sql, (data['title'], data['url'], create_time, 0))
                    conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()


if __name__ == '__main__':
    zhihu = ZhihuHot()
    html = zhihu.download_item()
    items = zhihu.clear_item(html)
    zhihu.save_item(items)
