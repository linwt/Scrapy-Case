# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domain = ['example.webscraping.com']
    start_urls = ['http://example.webscraping.com/places/default/user/profile']

    # 解析登录后下载的页面，此例中为用户个人信息页面
    def parse(self, response):
        keys = response.css('table label::text').re('(.+):')
        values = response.css('table td.w2p_fw::text').extract()

        yield dict(zip(keys, values))

    # 登录页面的 url
    login_url = 'http://example.webscraping.com/places/default/user/login'

    # 重写start_requests方法，最先请求登录页面
    def start_requests(self):
        yield Request(self.login_url, callback=self.login)

    # 登录页面的解析函数，构造FormRequest对象提交表单
    def login(self, response):
        # 登录页面的解析函数，构造 FormRequest 对象提交表单
        fd = {'email': 'liushuo@webscraping.com', 'password': '12345678'}
        yield FormRequest.from_response(response, formdata=fd, callback=self.parse_login)

    # 登录成功后，继续爬取start_urls中的页面
    def parse_login(self, response):
        if 'Welcome Liu' in response.text:
            # yield scrapy.Request('http://example.webscraping.com/places/default/user/profile', callback=self.parse)
            yield from super().start_requests()  # Python 3 语法