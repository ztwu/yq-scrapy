# -*- coding: utf-8 -*-
import datetime
import json
import re
import time

import requests
import scrapy
from scrapy import Request
from logger_util import LoggerUtil
from myscrapy.items import FHJSXW


class fhjwSpider(scrapy.Spider):
    logger_util = LoggerUtil()
    logger = logger_util.getSelfLogger("fhjwSpider")

    name = 'fhjw2'
    allowed_domains = ['shankapi.ifeng.com',"comment.ifeng.com","mil.ifeng.com",
                       "tech.ifeng.com","ishare.ifeng.com","news.ifeng.com","survey.news.ifeng.com"]
    start_urls = ['https://mil.ifeng.com/']

    def parse(self, response):
        aitems = set(response.xpath("//div[@class='news-34dpVmYc']//a"))
        for aitem in aitems:
            item = {}
            url = "https:"+aitem.xpath("@href").extract()[0]
            title = aitem.xpath("@title").extract()[0]
            print(url,title)
            id = url.split("/")[-1]
            commentUrl = "ucms_"+ id
            item["id"] = id
            item["title"] = title
            item["commentUrl"] = commentUrl
            item["url"] = url
            comment_url = "https://comment.ifeng.com/get.php?orderby=create_time&" \
                          "docUrl={0}&format=js&job=1&p=1&pageSize=1".format(commentUrl)
            yield response.follow(comment_url, meta=item, callback=self.parse_comment)

    def parse_comment(self,response):
        id = response.meta["id"]
        url = response.meta["url"]
        commentUrl = response.meta["commentUrl"]
        title = response.meta["title"]
        data = re.findall("{(.*)}", response.text.encode('utf-8').decode('unicode_escape'))
        if len(data) >0:
            jsondata_result = "{"+re.findall("{(.*)}",response.text)[0]+"}"
            jsondata = json.loads(jsondata_result)
            # print(jsondata)
            count = jsondata["count"]
            join_count = jsondata["join_count"]
            comments = jsondata["comments"]
            print("count===", id, title, count, join_count)
            metaitem= {}
            metaitem["id"] = id
            metaitem["title"] = title
            metaitem["count"] = count
            metaitem["join_count"] = join_count
            metaitem["commentUrl"] = commentUrl
            print("url====",url)
            yield response.follow(url, meta=metaitem, callback=self.parse_context)

    def parse_context(self, response):
        id = response.meta["id"]
        title = response.meta["title"]
        count = response.meta["count"]
        join_count = response.meta["join_count"]
        commentUrl = response.meta["commentUrl"]
        publish_time = response.xpath("//p[@class='time-1Mgp9W-1']/span[1]/text()").extract()[0].strip()
        context = response.xpath("////div[@class='text-3w2e3DBc']//p/text()").extract()
        # print("结果数据：",id,title,publish_time,context,count,join_count)
        accumulator_url = "https://survey.news.ifeng.com/api/getaccumulatorweight?format=js&" \
        "key={0}ding&serviceid=2&callback=getaccumulator"
        accumulator_url = accumulator_url.format(commentUrl)
        accumulator_meta = {}
        accumulator_meta["id"] = id
        accumulator_meta["title"] = title
        accumulator_meta["publish_time"] = publish_time
        accumulator_meta["context"] = context
        accumulator_meta["count"] = count
        accumulator_meta["join_count"] = join_count
        accumulator_meta["commentUrl"] = commentUrl
        print("获取推荐数：",accumulator_url)
        yield scrapy.Request(accumulator_url,meta=accumulator_meta, callback=self.parese_context2)

    def parese_context2(self,response):
        fhjsxw = FHJSXW()
        id = response.meta["id"]
        title = response.meta["title"]
        context = response.meta["context"]
        publish_time = response.meta["publish_time"]
        count = response.meta["count"]
        join_count = response.meta["join_count"]
        commentUrl = response.meta["commentUrl"]
        data = re.findall("\"browse\":{(.*)}}}", response.text)
        print(data)
        if len(data) > 0:
            jsondata_result = "{" + data[0] + "}"
            jsondata = json.loads(jsondata_result)
            print(jsondata)
            accumulator_count = jsondata[commentUrl+"ding"]
            print("结果数据：",id,title,context,publish_time,count,join_count,accumulator_count)
            fhjsxw["id"] = id
            fhjsxw["title"] = title
            fhjsxw["context"] = "|".join(context)
            fhjsxw["publish_time"] = publish_time
            fhjsxw["comment_count"] = count
            fhjsxw["join_count"] = join_count
            fhjsxw["accumulator_count"] = accumulator_count
            pdate = datetime.datetime.now().strftime('%Y-%m-%d')
            fhjsxw["pdate"] = pdate
            fhjsxw["data_source"] = "凤凰网"
            fhjsxw["data_module"] = "军事首页"
            yield fhjsxw
        else:
            fhjsxw["id"] = id
            fhjsxw["title"] = title
            fhjsxw["context"] = context
            fhjsxw["publish_time"] = publish_time
            fhjsxw["comment_count"] = count
            fhjsxw["join_count"] = join_count
            fhjsxw["accumulator_count"] = 0
            pdate = datetime.datetime.now().strftime('%Y-%m-%d')
            fhjsxw["pdate"] = pdate
            fhjsxw["data_source"] = "凤凰网"
            fhjsxw["data_module"] = "军事首页"
            yield fhjsxw