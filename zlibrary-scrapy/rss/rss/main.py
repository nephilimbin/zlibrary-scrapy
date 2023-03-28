import time
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import cmdline
from spiders.zlib import ZlibBookURLSpider, ZlibCateURLSpider, ZlibCateTermURLSpider
import multiprocessing


if __name__ == '__main__':
    start_time = time.time()
    process = CrawlerProcess(settings = get_project_settings(),)

    # process.crawl(ZlibCateURLSpider)
    # process.crawl(ZlibCateTermURLSpider)
    process.crawl(ZlibBookURLSpider)
    process.start() # the script will block here until the crawling is finished
    # cmdline.execute("scrapy crawl zlib".split())

    # Record the end time
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    print(f"Elapsed time: {elapsed_time} seconds")