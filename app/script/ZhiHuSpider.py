# -*- coding=utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pymysql
import datetime


class ZhiHuSpider:
    def __init__(self, original_url):
        self.header_data = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'Accept-Encoding': 'gzip, deflate, sdch, br',
                            'Accept-Language': 'zh-CN,zh;q=0.8',
                            'Connection': 'keep-alive',
                            'Cache-Control': 'max-age=0', 'Host': 'www.zhihu.com', 'Upgrade-Insecure-Requests': '1',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'

                            }
        self.original_url = original_url
        self.conn = pymysql.connect(
            host='192.168.31.196',
            user='root',
            password='123456789cJ.',
            db='demo_database',
            port=3306,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )

    def db_operation(self, quotes):
        """
        插入数据库
        :return:
        """
        insert_data = []
        create_time = datetime.datetime.now()
        for quote in quotes:
            temp = [quote, 0, create_time, 0]
            insert_data.append(temp)
        if not self.conn:
            return 'conn failed'
        try:
            with self.conn.cursor() as cursor:
                sql = ''' insert into user_contents (content, del_flag, create_time, user_id) values(%s,%s,%s,%s)'''
                cursor.executemany(sql, insert_data)
                self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def clear_cont(self, items):
        """
        清洗数据
        :return:
        """
        pass

    def get_cont(self):
        """
        爬取内容
        :return:
        """

        resp = requests.get(self.original_url, headers=self.header_data)

        soup = BeautifulSoup(resp.text, features="html.parser")
        quotes = soup.select('blockquote')
        words = soup.select('div.RichContent-inner p')
        coll_list = []
        for quote in quotes:
            if len(quote.text) > 6:
                coll_list.append(quote.text)
        for word in words:
            if len(word.text) > 6:
                coll_list.append(word.text)

        return coll_list

    def __del__(self):
        self.conn.close()


if __name__ == '__main__':
    """
    img_url: 下载图片的问题链接
    path：下载保存的路径
    """

    url = "https://www.zhihu.com/question/318185970/answer/742914625"
    _spider = ZhiHuSpider(original_url=url)
    quotes = _spider.get_cont()
    _spider.db_operation(quotes)
