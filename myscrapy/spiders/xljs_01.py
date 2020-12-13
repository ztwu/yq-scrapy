# -*- coding: utf-8 -*-
# @Time    : 2020/10/16 9:13
# @Author  : ztwu4
# @Email   : ztwu4@iflytek.com
# @File    : xljs.py
# @Software: PyCharm
import datetime
import json
import re
import time

import scrapy

from logger_util import LoggerUtil
from myscrapy.items import FHJSXWPL, FHJSXW


class xljsSpider(scrapy.Spider):
    logger_util = LoggerUtil()
    logger = logger_util.getSelfLogger("xljsSpider")

    name = 'xljs01'
    allowed_domains = ['mil.news.sina.com.cn', "comment.sina.com.cn"]
    start_urls = ["http://mil.news.sina.com.cn/roll/index.d.html?cid=57919"]

    def parse(self, response):
        datas = set(response.xpath("//div[@class='fixList']//a"))
        for item in datas:
            new_url = item.xpath("@href").extract()[0]
            title = item.xpath("text()").extract()[0]
            print(new_url, title)
            metadata = {}
            metadata["title"] = title
            yield response.follow(url=new_url, meta=metadata, callback=self.parse_news)

        next_datas = response.xpath("//a[@title='下一页']/@href").extract()
        if len(next_datas) > 0:
            next_url = next_datas[0]
            print("页码====", next_url, "====")
            yield response.follow(url=next_url, callback=self.parse)

    def parse_news(self,response):
        url = response.url
        title = response.meta["title"]
        id = re.findall("-(.*)\.",url.split("/")[-1])[0]
        id = id[1:]
        context = response.xpath("//div[@class='article']//p/text()").extract()
        publish_time = response.xpath("//div[@class='date-source']/span[1]/text()").extract()[0]
        print("id,title",id,title,publish_time,context)

        comment_url = "http://comment.sina.com.cn/page/info?version=1&format=json&channel=jc&newsid=comos-{0}&group=0&compress=0&ie=utf-8&oe=utf-8" \
                      "&page={1}&page_size=10&t_size=3&h_size=3&thread=1&uid=unlogin_user&callback=jsonp_1602817818772&_=1602817818772"
        comment_url = comment_url.format(id,1)

        metadata = {}
        metadata["id"] = id
        metadata["title"] = title
        metadata["context"] = context
        metadata["publish_time"] = publish_time
        print(metadata)
        print("comment_url===",comment_url)
        yield response.follow(url=comment_url, meta=metadata, callback=self.parse_comment)

    def parse_comment(self, response):
        id = response.meta["id"]
        title = response.meta["title"]
        context = response.meta["context"]
        publish_time = response.meta["publish_time"]
        data = re.findall("{(.*)}", response.text)
        if len(data) > 0:
            jsondata_result = "{" + re.findall("{(.*)}", response.text)[0] + "}"
            jsondata = json.loads(jsondata_result)["result"]
            count = jsondata["count"]
            join_count = count["total"]
            comment_count = count["show"]
            xljsxw = FHJSXW()
            pdate = datetime.datetime.now().strftime('%Y-%m-%d')
            xljsxw["id"] = id
            xljsxw["title"] = title
            xljsxw["context"] =  "|".join(context)
            xljsxw["publish_time"] = publish_time
            xljsxw["comment_count"] = comment_count
            xljsxw["join_count"] = join_count
            xljsxw["accumulator_count"] = 0
            xljsxw["pdate"] = pdate
            xljsxw["data_source"] = "新浪网"
            xljsxw["data_module"] = "国际军情"
            print(xljsxw)
            yield xljsxw
        else:
            xljsxw = FHJSXW()
            pdate = datetime.datetime.now().strftime('%Y-%m-%d')
            xljsxw["id"] = id
            xljsxw["title"] = title
            xljsxw["context"] = "|".join(context)
            xljsxw["publish_time"] = publish_time
            xljsxw["comment_count"] = 0
            xljsxw["join_count"] = 0
            xljsxw["accumulator_count"] = 0
            xljsxw["pdate"] = pdate
            xljsxw["data_source"] = "新浪网"
            xljsxw["data_module"] = "国际军情"
            print(xljsxw)
            yield xljsxw

