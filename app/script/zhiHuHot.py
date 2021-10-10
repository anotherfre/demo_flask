# -*- coding:utf-8 -*-
import requests
from lxml import etree


class ZhihuHot:
    def __init__(self):
        self.url = 'https://www.zhihu.com/hot'
        self.url = 'https://www.zhihu.com/question/318185970/answer/742914625'
        self.header_data = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'Accept-Encoding': 'gzip, deflate, sdch, br',
                            'Accept-Language': 'zh-CN,zh;q=0.8',
                            'Connection': 'keep-alive',
                            'Cache-Control': 'max-age=0', 'Host': 'www.zhihu.com', 'Upgrade-Insecure-Requests': '1',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
                            }

    def download_item(self):
        resp = requests.get(self.url, headers=self.header_data)
        if resp.status_code == 200:
            return resp.content

    def clear_item(self, html):
        html = etree.parse(html, etree.HTMLParser())
        result = html.xpath('//section[@class="HotItem"]//text()')
        pass

    def save_item(self):
        pass


if __name__ == '__main__':
    zhihu = ZhihuHot()
    html = zhihu.download_item()
    items = zhihu.clear_item(html)
