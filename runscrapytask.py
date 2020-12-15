# -*- coding: utf-8 -*-
# @Time    : 2020/12/15 9:58
# @Author  : ztwu4
# @Email   : ztwu4@iflytek.com
# @File    : runscrapytask.py
# @Software: PyCharm
import os
import sched
import time

schedule = sched.scheduler(time.time, time.sleep)
# 被周期性调度触发的函数
def func():
    os.system("scrapy crawl tq")
    os.system("scrapy crawl xljspl4")
    os.system("scrapy crawl xljspl2")

def perform1(inc):
    schedule.enter(inc, 0, perform1, (inc,))
    func()

def mymain():
    schedule.enter(0, 0, perform1, (180,))

if __name__ == "__main__":
    mymain()
    schedule.run()