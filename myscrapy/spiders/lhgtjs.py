# -*- coding: utf-8 -*-
# @Time    : 2020/3/18 14:25
# @Author  : ztwu4
# @Email   : ztwu4@iflytek.com
# @File    : lhgtjs.py
# @Software: PyCharm
import os
import re
import urllib
import scrapy
from logger_util import LoggerUtil

class LhgtjsSpider(scrapy.Spider):
    logger_util = LoggerUtil()
    logger = logger_util.getSelfLogger("LhgtjsSpider")

    name = 'lhgtjs'
    filepath = "jszlwz/data/lhgtjsdatas2.csv"
    allowed_domains = ['data.un.org']
    # start_urls = ['http://data.un.org/Handlers/ExplorerHandler.ashx?m=EDATA',
    #               'http://data.un.org/Handlers/ExplorerHandler.ashx?m=FAO',
    #               'http://data.un.org/Handlers/ExplorerHandler.ashx?m=ICS']
    start_urls = ['http://data.un.org/Handlers/ExplorerHandler.ashx?m=ICS']

    def __init__(self, url):
        if os.path.exists(self.filepath):
            os.remove(self.filepath)
        print("启动url===", url)

    def parse(self, response):
        # 爬取页面内的item
        items = set(response.xpath('//@href'))
        self.logger.warning("测试", items)
        for item in items:
            tempItem = item.extract()
            if re.findall("Data.aspx?.*[\d]",tempItem):
                dataurl = urllib.parse.unquote(str(tempItem).replace("\\\"",""))
                new_url = 'http://data.un.org/'+dataurl
                print(new_url)
                # self.logger.warning(new_url)
                yield response.follow(new_url, callback=self.parse_datadetail)

    def get_nextpage_url(self,page,url):
        print("url===",url)
        datatemp = url.split("?")[1].split("&")
        dataMartId = datatemp[0].split("=")[1]
        dataFilter = datatemp[1].split("=")[1]
        if dataMartId == "ICS":
            new_url = 'http://data.un.org/Handlers/DataHandler.ashx?Service=page' \
                      '&Page={0}' \
                      '&DataFilter={1}' \
                      '&DataMartId={2}' \
                      '&UserQuery=&c=2,5,6,7,8' \
                      '&s=_crEngNameOrderBy:asc,,yr:desc,_utEngNameOrderBy:asc' \
                .format(page, dataFilter, dataMartId)
        else:
            new_url = 'http://data.un.org/Handlers/DataHandler.ashx?Service=page' \
                  '&Page={0}' \
                  '&DataFilter={1}' \
                  '&DataMartId={2}' \
                  '&UserQuery=&c=2,5,6,7,8' \
                  '&s=_crEngNameOrderBy:asc,_enID:asc,yr:desc'\
                .format(page,dataFilter,dataMartId)
        print(new_url,dataMartId)
        return new_url,dataMartId

    def parse_data(self,response):
        name = response.meta['name']
        type = response.meta['type']
        items = response.xpath('//div[@class="DataContainer"]//tr')
        for item in items:
            tds = item.xpath("./td//text()").extract()
            print("原始数据===",type+"|"+name+"|"+"|".join(tds))
            with open(self.filepath,mode="a",encoding="utf-8") as f:
                f.write(type+"|"+name+"|"+"|".join(tds)+"\n")
            # lhgItem = LhgItem()
            # lhgItem.name = name
            # lhgItem.value = tds
            # yield lhgItem

    def parse_datadetail(self, response):
        print("test===============================")
        name = response.xpath('//div[@class="SeriesMeta"]//h2/text()').extract_first()
        # page = response.xpath('//span[contains(@id, "spanPageIndexB")]/text()').extract_first()
        total = response.xpath('//span[contains(@id, "spanPageCountB")]/text()').extract_first()
        for i in range(int(total)):
            page = i+1
            new_url,dataMartId = self.get_nextpage_url(page,response.url)
            print("test===",new_url,dataMartId)
            self.logger.warning(new_url)
            yield response.follow(new_url,meta={'name': name, 'type': dataMartId}, callback=self.parse_data)

