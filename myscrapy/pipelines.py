from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request

from myscrapy.items import AttrItem, CmanoItem, RelaItem, LhgItem, FHJSXW, FHJSXWPL
from logger_util import LoggerUtil

class SaveToCsvPipeline(object):

    def __init__(self, filepath):
        self.filepath = filepath

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            filepath=crawler.settings.get('FILE_PATH'),
        )

    def open_spider(self, spider):
        self.f = open(self.filepath,encoding="utf-8",mode="w")

    def process_item(self, item, spider):
        print("SaveToCsvPipeline start...")
        if isinstance(item, LhgItem):
            self.logger.warning("保存数据到csv本地文件 -----------------------", item)
            self.f.write("|".join(item.name,item.value)+"\n")

    def close_spider(self, spider):
        self.f.close()

class MyscrapyPipeline(object):
    def process_item(self, item, spider):
        return item

class MyImagePipeline(ImagesPipeline):

    # 下载图片时加入referer请求头
    def get_media_requests(self, item, info):
        if isinstance(item, CmanoItem):
            for image_url in item['image_urls']:
                # headers = {'referer':item['referer']}
                yield Request(image_url)

    # 获取图片的下载结果, 控制台查看
    def item_completed(self, results, item, info):
        if isinstance(item, CmanoItem):
            image_paths = [x['path'] for ok, x in results if ok]
            if not image_paths:
                raise DropItem("Item contains no images")
            return item

    # 修改文件的命名和路径
    def file_path(self, request, response=None, info=None):
        print("测试-----------------------",request.url)
        image_guid = request.url.split('/')[-1]
        dirname = image_guid.split("_")[0]
        filename = './{}/{}'.format(dirname, image_guid)
        print("文件名-----------------------", filename)
        return filename

import pymongo

# class MongoPipeline(object):
#     logger_util = LoggerUtil()
#     logger = logger_util.getSelfLogger("MongoPipelineLogger")
#
#     def __init__(self, mongo_uri, mongo_db):
#         self.logger.warning(mongo_uri,mongo_db)
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI'),
#             mongo_db=crawler.settings.get('MONGO_DB')
#         )
#
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#
#     def process_item(self, item, spider):
#         if isinstance(item, AttrItem):
#             self.logger.warning("mongodb数据 db_aircraft_attr -----------------------", item)
#             self.db["db_aircraft_attr"].insert(dict(item))
#         elif isinstance(item, RelaItem):
#             self.logger.warning("mongodb数据 db_aircraft_rela -----------------------", item)
#             self.db["db_aircraft_rela"].insert(dict(item))
#         return item
#
#     def close_spider(self, spider):
#         self.client.close()

import pymysql

class MysqlPipeline():
    logger_util = LoggerUtil()
    logger = logger_util.getSelfLogger("mysqlPipelineLogger")

    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        if isinstance(item,FHJSXW):
            table = "yq_data"
            data = dict(item)
            self.logger.info("插入数据： ", data)
            keys = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            sql = 'insert into %s (%s) values (%s)' % (table, keys, values)
            print("执行sql:", sql)
            print(tuple(data.values()))
            try:
                self.cursor.execute(sql, tuple(data.values()))
                self.db.commit()
            except Exception as e:
                print("错误：", e)
            return item
        elif isinstance(item,FHJSXWPL):
            table = "yq_pl_data"
            data = dict(item)
            self.logger.info("插入数据： ",data)
            keys = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            sql = 'insert into %s (%s) values (%s)' % (table, keys, values)
            print("执行sql:",sql)
            print(tuple(data.values()))
            try:
                self.cursor.execute(sql, tuple(data.values()))
                self.db.commit()
            except Exception as e:
                print("错误：",e)
            return item