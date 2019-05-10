# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from os.path import join, basename, dirname
from urllib.parse import urlparse
from scrapy.pipelines.files import FilesPipeline


class MatplotlibExamplesPipeline(object):
    def process_item(self, item, spider):
        return item


# https://matplotlib.org/examples/axes_grid/demo_floating_axes.py
# url的shal散列值226vdh182k6l3x2s8y52d3d
# 则存储路径为 examples_src/full/226vdh182k6l3x2s8y52d3d.py
# 实现FilesPipeline的子类，重写file_path方法，更改文件命名
# 最终路径为 examples_src/full/axes_grid/demo_floating_axes.py
class MyFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        path = urlparse(request.url).path
        return join(basename(dirname(path)), basename(path))