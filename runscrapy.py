import schedule
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def fhjs_job():
    process = CrawlerProcess(get_project_settings())
    process.crawl("fhjw")
    process.start()

def fhjspl_job():
    process = CrawlerProcess(get_project_settings())
    process.crawl("fhjwpl")
    process.start()

def fhjs2_job():
    process = CrawlerProcess(get_project_settings())
    process.crawl("fhjw2")
    process.start()

def fhjspl2_job():
    process = CrawlerProcess(get_project_settings())
    process.crawl("fhjwpl2")
    process.start()

def xljs_job():
    process = CrawlerProcess(get_project_settings())
    process.crawl("xljs")
    process.start()

def xljs2_job():
    process = CrawlerProcess(get_project_settings())
    process.crawl("xljs2")
    process.start()

def xljs3_job():
    process = CrawlerProcess(get_project_settings())
    process.crawl("xljs3")
    process.start()

def xljs4_job():
    process = CrawlerProcess(get_project_settings())
    process.crawl("xljs4")
    process.start()

def xljspl_job():
    process = CrawlerProcess(get_project_settings())
    process.crawl("xljspl")
    process.start()

def xljspl2_job():
    process = CrawlerProcess(get_project_settings())
    process.crawl("xljspl2")
    process.start()

def xljspl3_job():
    process = CrawlerProcess(get_project_settings())
    process.crawl("xljspl3")
    process.start()

def xljspl4_job():
    process = CrawlerProcess(get_project_settings())
    process.crawl("xljspl4")
    process.start()

def fhjstest_job():
    process = CrawlerProcess(get_project_settings())
    process.crawl("fhjwtest")
    process.start()

if __name__ == '__main__':

    # fhjstest_job()

    # xljs_job()
    # xljs2_job()
    # xljs3_job()
    # xljs4_job()

    # xljspl_job()
    xljspl2_job()
    # xljspl3_job()
    # xljspl4_job()

    # fhjs_job()
    # fhjspl_job()
    # fhjs2_job()
    # fhjspl2_job()
    # schedule.every().day.at('17:48').do(fhjs_job)
    # schedule.every().day.at('17:50').do(fhjspl_job)
    # schedule.every().day.at('17:52').do(fhjs2_job)
    # schedule.every().day.at('17:54').do(fhjspl2_job)
    # while True:
    #     schedule.run_pending()

