# -*- coding: utf-8 -*-
import datetime
import json
import re
import time

import requests
import scrapy
from scrapy import Request
from logger_util import LoggerUtil
from myscrapy.items import FHJSXWPL


class fhjwSpider(scrapy.Spider):
    logger_util = LoggerUtil()
    logger = logger_util.getSelfLogger("fhjwSpider")

    name = 'fhjwpl2'
    allowed_domains = ['shankapi.ifeng.com',"comment.ifeng.com","mil.ifeng.com"]
    start_urls = ['https://mil.ifeng.com/']

    def parse(self, response):
        aitems = set(response.xpath("//div[@class='news-34dpVmYc']//a"))
        for aitem in aitems:
            item = {}
            url = "https:" + aitem.xpath("@href").extract()[0]
            title = aitem.xpath("@title").extract()[0]
            print(url, title)
            id = url.split("/")[-1]
            commentUrl = "ucms_" + id
            item["id"] = id
            item["title"] = title
            item["commentUrl"] = commentUrl
            item["url"] = url
            item["p"] = 1
            comment_url = "https://comment.ifeng.com/get.php?orderby=create_time&" \
                          "docUrl={0}&format=js&job=1&p=1&pageSize=20".format(commentUrl)
            yield response.follow(comment_url, meta=item, callback=self.parse_comment)

    def parse_comment(self,response):
        id = response.meta["id"]
        url = response.meta["url"]
        commentUrl = response.meta["commentUrl"]
        title = response.meta["title"]
        p = response.meta["p"]
        data = re.findall("{(.*)}", response.text.encode('utf-8').decode('unicode_escape'))
        if len(data) >0:
            jsondata_result = "{"+re.findall("{(.*)}",response.text)[0]+"}"
            jsondata = json.loads(jsondata_result)
            # print(jsondata)
            count = jsondata["count"]
            join_count = jsondata["join_count"]
            comments = jsondata["comments"]
            if len(comments) >0:
                for comment in comments:
                    comment_id = comment["comment_id"]
                    uname = comment["uname"]
                    user_id = comment["user_id"]
                    comment_contents = comment["comment_contents"]
                    comment_date = comment["comment_date"]
                    uptimes = comment["uptimes"]
                    parents = comment["parent"]
                    reply_comment_ids = []
                    if len(parents) >0 :
                        for parent in parents:
                            reply_comment_id = parent["comment_id"]
                            reply_comment_ids.append(reply_comment_id)
                    print("comment===",id, title, comment_id, uname, user_id, comment_contents, comment_date, uptimes,reply_comment_ids)

                    fhjsxwpl = FHJSXWPL()
                    fhjsxwpl["id"] = id
                    fhjsxwpl["title"] = title
                    fhjsxwpl["comment_id"] = comment_id
                    fhjsxwpl["comment_contents"] = comment_contents
                    fhjsxwpl["comment_date"] = comment_date
                    fhjsxwpl["user_name"] = uname
                    fhjsxwpl["user_id"] = user_id
                    fhjsxwpl["uptimes"] = uptimes
                    fhjsxwpl["reply_comment_ids"] = ",".join(reply_comment_ids)
                    pdate = datetime.datetime.now().strftime('%Y-%m-%d')
                    fhjsxwpl["pdate"] = pdate
                    fhjsxwpl["data_source"] = "凤凰网"
                    fhjsxwpl["data_module"] = "军事首页"
                    yield fhjsxwpl

                p = p+1
                comment_url = "https://comment.ifeng.com/get.php?orderby=create_time&" \
                              "docUrl={0}&format=js&job=1&p={1}&pageSize=20".format(commentUrl,p)
                yield scrapy.Request(comment_url, meta=response.meta, callback=self.parse_comment)
            else:
                print("结束")