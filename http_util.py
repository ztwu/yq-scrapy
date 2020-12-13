# -*- coding: utf-8 -*-
# @Time    : 2020/4/14 14:46
# @Author  : ztwu4
# @Email   : ztwu4@iflytek.com
# @File    : http_util.py
# @Software: http请求操作
import json
import requests

def do_post(url, datas, headers):
    r = requests.post(url=url, data=json.dumps(datas),headers=headers)
    status_code = r.status_code
    if status_code == 200:
        print("返回数据=",r.text)
        return r.text
    else:
        print(r.raise_for_status())

def do_get(url, datas, headers):
    r = requests.get(url=url, params=datas,headers=headers)
    status_code = r.status_code
    if status_code == 200:
        print("返回数据=",r.text)
        return r.text
    else:
        print(r.raise_for_status())

if __name__ == '__main__':
    datas = {"entityParagraph":"F22部署在关岛","beginOffset":0,"endOffset":3,"entityName":"F22","entityType":"aircraft"}
    headers = {'Content-Type': 'application/json'}
    url = "http://172.31.202.29:45678/entitylinking/post"
    data = do_post(url, datas, headers)
    object = json.loads(data)
    entity_id = str(object['entities'][0]['id'])
    entity_name = str(object['entities'][0]['KBName'])
    if entity_id.__ne__("NIL"):
        print(entity_id,entity_name)

    # url = "http://tieba.baidu.com/f?"
    # datas = {
    #     'kw': '赵丽颖吧',
    #     'pn': '50'
    # }
    # headers = {
    #     'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'}
    # data = do_post(url, datas, headers)
    # print(data)