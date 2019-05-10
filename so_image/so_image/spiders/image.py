# -*- coding: utf-8 -*-
import scrapy
import json
from so_image.items import SoImageItem


class ImageSpider(scrapy.Spider):
    name = "image"
    allowed_domains = ["image.so.com"]
    BASE_URL = 'https://image.so.com/zj?ch=food&sn=%s&listtype=new&temp=1'
    start_urls = [BASE_URL % 0]
    start_index = 0
    # 限制最大下载数量，防止磁盘用量过大
    MAX_DOWNLOAD_NUM = 20

    def parse(self, response):
        # 使用json模块解析响应结果
        infos = json.loads(response.body.decode('utf8'))

        # 提取所有图片下载url到一个列表，赋给items的'image_urls'字段。若用一行代码表示则items不需要实现两个字段
        # yield {'image_urls': [info['qhimg_url'] for info in infos['list']]}

        image = SoImageItem()
        image['image_urls'] = [info['qhimg_url'] for info in infos['list']]
        yield image

        # 若count字段大于0，并且下载数量不足 MAX_DOWNLOAD_NUM，继续获取下一页图片信息
        self.start_index += infos['count']
        if infos['count'] > 0 and self.start_index < self.MAX_DOWNLOAD_NUM:
            yield scrapy.Request(self.BASE_URL % self.start_index)
