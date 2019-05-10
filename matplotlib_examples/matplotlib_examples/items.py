# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ExamplesItem(scrapy.Item):
    # file_url字段将要下载文件的url传给pipeline，pipeline会自动将文件下载到本地，并将下载结果信息存入files字段
    # 结果信息：[Path, Checksum, url] 即 [文件下载到本地的路径，文件的校验和，文件的url地址]
    file_urls = scrapy.Field()
    files = scrapy.Field()
