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
from myscrapy.items import FHJSXWPL


class xljs4Spider(scrapy.Spider):
    logger_util = LoggerUtil()
    logger = logger_util.getSelfLogger("xljs4Spider")

    name = 'xljspl4'
    allowed_domains = ['mil.news.sina.com.cn',"comment.sina.com.cn"]

    start_urls = ["http://mil.news.sina.com.cn/roll/index.d.html?cid=234400"]

    def parse(self, response):
        datas = set(response.xpath("//div[@class='fixList']//a"))
        for item in datas:
            new_url = item.xpath("@href").extract()[0]
            title = item.xpath("text()").extract()[0]
            print(new_url,title)
            metadata = {}
            metadata["title"] = title
            yield response.follow(url=new_url,meta=metadata,callback=self.parse_news)

        next_datas = response.xpath("//a[@title='下一页']/@href").extract()
        if len(next_datas) > 0:
            next_url = next_datas[0]
            print("页码====", next_url, "====")
            yield response.follow(url=next_url,callback=self.parse)

    def parse_news(self,response):
        url = response.url
        title = response.meta["title"]
        id = re.findall("-(.*)\.",url.split("/")[-1])[0]
        id = id[1:]

        print("id,title",id,title)
        # datas = set(response.xpath("//div[@class='fixList']//a"))

        comment_url = "http://comment.sina.com.cn/page/info?version=1&format=json&channel=jc&newsid=comos-{0}&group=0&compress=0&ie=utf-8&oe=utf-8" \
                      "&page={1}&page_size=10&t_size=3&h_size=3&thread=1&uid=unlogin_user&callback=jsonp_1602817818772&_=1602817818772"
        comment_url = comment_url.format(id,1)

        metadata = {}
        metadata["id"] = id
        metadata["title"] = title
        metadata["page"] = 1
        print(metadata)
        print("comment_url===",comment_url)
        yield response.follow(url=comment_url, meta=metadata, callback=self.parse_comment)

    def parse_comment(self, response):
        id = response.meta["id"]
        title = response.meta["title"]
        page = response.meta["page"]

        data = re.findall("{(.*)}", response.text)
        if len(data) > 0:
            jsondata_result = "{" + re.findall("{(.*)}", response.text)[0] + "}"
            jsondata = json.loads(jsondata_result)["result"]
            print(jsondata)
            count = jsondata["count"]
            join_count = count["total"]
            comment_count = count["show"]

            cmntlist = jsondata["cmntlist"]
            threaddict = jsondata["threaddict"]
            if len(cmntlist) >0:

                for cmn in cmntlist:
                    xljsxwpl = FHJSXWPL()
                    xljsxwpl["id"] = id
                    xljsxwpl["title"] = title
                    xljsxwpl["user_name"] = cmn["nick"]
                    xljsxwpl["user_id"] = cmn["uid"]
                    xljsxwpl["comment_id"] = cmn["mid"]
                    xljsxwpl["comment_contents"] = cmn["content"]
                    xljsxwpl["comment_date"] = cmn["time"]
                    xljsxwpl["uptimes"] = cmn["agree"]
                    xljsxwpl["reply_comment_ids"] = ""
                    pdate = datetime.datetime.now().strftime('%Y-%m-%d')
                    xljsxwpl["pdate"] = pdate
                    xljsxwpl["data_source"] = "新浪网"
                    xljsxwpl["data_module"] = "南海局势"
                    print(xljsxwpl)
                    yield xljsxwpl

                if len(threaddict.values()) >0:
                    threaddictlist = threaddict.values()
                    for threaddictitem in threaddictlist:
                        for thread in threaddictitem["list"]:
                            xljsxwpl = FHJSXWPL()
                            xljsxwpl["id"] = id
                            xljsxwpl["title"] = title
                            xljsxwpl["user_name"] = thread["nick"]
                            xljsxwpl["user_id"] = thread["uid"]
                            xljsxwpl["comment_id"] = thread["mid"]
                            xljsxwpl["comment_contents"] = thread["content"]
                            xljsxwpl["comment_date"] = thread["time"]
                            xljsxwpl["uptimes"] = thread["agree"]
                            xljsxwpl["reply_comment_ids"] = ""
                            pdate = datetime.datetime.now().strftime('%Y-%m-%d')
                            xljsxwpl["pdate"] = pdate
                            xljsxwpl["data_source"] = "新浪网"
                            xljsxwpl["data_module"] = "南海局势"
                            print(xljsxwpl)
                            yield xljsxwpl

                page = page+1
                comment_url = "http://comment.sina.com.cn/page/info?version=1&format=json&channel=jc&newsid=comos-{0}&group=0&compress=0&ie=utf-8&oe=utf-8" \
                              "&page={1}&page_size=10&t_size=3&h_size=3&thread=1&uid=unlogin_user&callback=jsonp_1602817818772&_=1602817818772"
                comment_url = comment_url.format(id, page)
                print("next_page==",comment_url)
                yield scrapy.Request(comment_url, meta=response.meta, callback=self.parse_comment)
            else:
                print("结束")
