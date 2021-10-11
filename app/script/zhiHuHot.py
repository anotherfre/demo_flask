# -*- coding:utf-8 -*-
import requests
from lxml import etree


class ZhihuHot:
    def __init__(self):
        self.url = 'https://www.zhihu.com/hot'
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'}
        self.proxies = {
            'http': 'http://122.114.31.177:808'
        }

    def download_item(self):
        resp = requests.get(self.url, headers=self.headers, allow_redirects=False, proxies=self.proxies)
        if resp.status_code == 200:
            resp.encoding = 'utf-8'
            return resp.text

    def clear_item(self, html):
        html = etree.HTML(html)
        result = html.xpath("//div[@class='HotItem-content']")
        pass

    def save_item(self):
        pass


if __name__ == '__main__':
    zhihu = ZhihuHot()
    html = zhihu.download_item()
    items = zhihu.clear_item(html)
