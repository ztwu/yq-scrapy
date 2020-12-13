# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class GJItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

class CmanoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    pass

class AttrItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    label = scrapy.Field()
    attr = scrapy.Field()
    value = scrapy.Field()
    pass

class RelaItem(scrapy.Item):
    # define the fields for your item here like:
    name_partA = scrapy.Field()
    name_partB = scrapy.Field()
    rela = scrapy.Field()
    pass

class LhgItem(scrapy.Item):
    name = scrapy.Field()
    value = scrapy.Field()
    pass

class FHJSXW(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    context = scrapy.Field()
    publish_time = scrapy.Field()
    comment_count = scrapy.Field()
    join_count = scrapy.Field()
    accumulator_count = scrapy.Field()
    pdate = scrapy.Field()
    data_source = scrapy.Field()
    data_module = scrapy.Field()
    pass

class FHJSXWPL(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    comment_id = scrapy.Field()
    comment_contents = scrapy.Field()
    comment_date = scrapy.Field()
    user_name = scrapy.Field()
    user_id = scrapy.Field()
    uptimes = scrapy.Field()
    reply_comment_ids = scrapy.Field()
    pdate = scrapy.Field()
    data_source = scrapy.Field()
    data_module = scrapy.Field()
    pass