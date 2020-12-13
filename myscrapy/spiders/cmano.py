# -*- coding: utf-8 -*-
import scrapy
import urllib
from myscrapy.items import CmanoItem, AttrItem, RelaItem, GJItem
from logger_util import LoggerUtil

class CmanoSpider(scrapy.Spider):
    logger_util = LoggerUtil()
    logger = logger_util.getSelfLogger("CmanoSpider")

    name = 'cmano'
    allowed_domains = ['www.cmano-db.com']
    start_urls = ['http://www.cmano-db.com/']

    def __init__(self, url):
        print("启动url===", url)

    def parse(self, response):
        # 爬取页面内的item
        items = set(response.xpath(
            '//ul[contains(@class, "nav navbar-nav")]/li/ul/li/a/@href'))
        self.logger.warning("测试", items)
        listCountrys = ['Ship', 'Submarine', 'Facility', 'Aircraft']
        noListCountrys = ["Weapon", "Sensor"]
        for item in items:
            tempItem = item.extract()
            new_url = 'http://www.cmano-db.com/'+urllib.parse.unquote(tempItem)
            self.logger.warning(tempItem)
            if tempItem[0:-1].lower() in [listCountry.lower() for listCountry in listCountrys]:
                self.logger.warning("测试", tempItem)
                yield response.follow(new_url, callback=self.parse_country)
            elif tempItem[0:-1].lower() in [noListCountry.lower() for noListCountry in noListCountrys]:
                self.logger.warning("测试", tempItem)
                yield response.follow(new_url, callback=self.parse_no_country_list)

    def parse_country(self,response):
        # self.logger.warning("country测试", response.url)
        items = set(response.xpath(
            '//div[contains(@class, "country")]/h4/a/@href'))
        self.logger.warning("测试", items)
        for index,item in enumerate(items):
            new_url = 'http://www.cmano-db.com/' + urllib.parse.unquote(item.extract())
            self.logger.warning("country测试", new_url)
            yield response.follow(new_url, callback=self.parse_country_list)

    def parse_country_list(self, response):
        self.logger.warning("country-list测试", response.url)
        items = set(response.xpath(
            '//table[contains(@class, "table table-striped table-hover")]//@href'))
        gjitem = GJItem()
        gjitem["name"] = response.url.split("/")[-2]
        print("-----------response.url", response.url)
        print("-----------gjname",gjitem)
        self.logger.warning("测试", items)
        for index,item in enumerate(items):
            new_url = 'http://www.cmano-db.com/' + urllib.parse.unquote(item.extract())
            self.logger.warning("测试", new_url)
            yield response.follow(new_url,meta={'item':gjitem}, callback=self.parse_country_detail)

    def parse_no_country_list(self, response):
        self.logger.warning("country-list测试", response.url)
        items = set(response.xpath(
            '//div[contains(@class, "country")]//@href'))
        self.logger.warning("测试", items)
        for index,item in enumerate(items):
            new_url = 'http://www.cmano-db.com/' + urllib.parse.unquote(item.extract())
            self.logger.warning("测试", new_url)
            yield response.follow(new_url,meta={'item': None}, callback=self.parse_country_detail)

    def parse_country_detail(self, response):

        label = response.url.split("/")[-3].strip()
        print("--------------label", label)
        name = response.xpath("//h3[@id='typography']/text()").extract()[0].strip()
        print("--------------name", name)

        img = CmanoItem()
        self.logger.warning("country-detial测试", response.url)
        imageitems = response.xpath("//div[contains(@class,'col-lg-7')]/a/img/@src")
        image_urls = []
        for index,item in enumerate(imageitems):
            new_url = 'http://www.cmano-db.com/' + urllib.parse.unquote(item.extract())
            image_urls.append(new_url)
        img["image_urls"] = image_urls
        yield img

        img1 = AttrItem()
        img1["name"] = name
        img1["attr"] = "label"
        img1["value"] = label
        print("--------------label", img1)
        yield img1

        item = response.meta['item']
        print("--------------item", item)
        if item is not None:
            imggj = RelaItem()
            imggj["name_partA"] = name
            imggj["name_partB"] = item["name"]
            imggj["rela"] = "服役国家"
            print("--------------服役国家", imggj)
            yield imggj

        if len(image_urls)>0:
            img0 = AttrItem()
            imagesname = image_urls[0].split("/")[-1].strip()
            filepath = "images/"+imagesname.split("_")[0]+"/"+imagesname
            print("--------------filepath", filepath)
            img0["name"] = name
            img0["attr"] = "image_path"
            img0["value"] = filepath
            yield img0

        items = response.xpath("//div[contains(@class,'col-lg-7')]/table[1]//td/text()")
        for index,item in enumerate(items):
            tempdata = item.extract().split(":")
            print("--------------tempdata", tempdata)
            if len(tempdata[0].strip())>0 and len(tempdata) == 2:
                img2 = AttrItem()
                img2["name"] = name
                img2["attr"] = tempdata[0].strip()
                img2["value"] = tempdata[1].strip()
                print("--------------attr",img2)
                yield img2

        weaponsList = ["Weapons:","Weapons / Loadouts:"]
        sensorsList = ["Sensors / EW:","Sensors:"]

        itemsrela1 = response.xpath("//div[contains(@class,'col-lg-7')]/table[2]//a/text()")
        print("------------itemsrela1",itemsrela1)
        relatype = response.xpath("//div[contains(@class,'col-lg-7')]/table[2]//u/text()").extract()
        print("------------relatype", relatype)
        for index, item in enumerate(itemsrela1):
            tempdata = item.extract()
            print("--------------tempdata", tempdata)
            if len(tempdata.strip()) > 0 :
                img3 = RelaItem()
                img3["name_partA"] = name
                img3["name_partB"] = tempdata.strip()
                if relatype[0] in sensorsList:
                    img3["rela"] = "传感器配置"
                elif relatype[0] in weaponsList:
                    img3["rela"] = "武器负载"
                print("--------------rela", img3)
                yield img3

        itemsrela12 = response.xpath("//div[contains(@class,'col-lg-7')]/table[3]//a/text()")
        print("------------itemsrela1", itemsrela12)
        relatype2 = response.xpath("//div[contains(@class,'col-lg-7')]/table[3]//u/text()").extract()
        print("------------relatype", relatype2)
        for index, item in enumerate(itemsrela12):
            tempdata = item.extract()
            print("--------------tempdata", tempdata)
            if len(tempdata.strip()) > 0:
                img4 = RelaItem()
                img4["name_partA"] = name
                img4["name_partB"] = tempdata.strip()
                if relatype2[0] in sensorsList:
                    img4["rela"] = "传感器配置"
                elif relatype2[0] in weaponsList:
                    img4["rela"] = "武器负载"
                print("--------------rela", img4)
                yield img4