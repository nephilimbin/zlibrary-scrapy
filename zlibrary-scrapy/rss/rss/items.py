# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZlibCateURLItem(scrapy.Item):
    '''建立目录URL的item'''
    cate_list = scrapy.Field()
    crawl_date = scrapy.Field()

class ZlibCateTermURLItem(scrapy.Item):
    '''建立目录URL的item'''
    term_list = scrapy.Field()
    crawl_date = scrapy.Field()

class ZlibBookURLItem(scrapy.Item):
    '''建立书URL的Item'''''
    # category_url = scrapy.Field()
    # category_term_name = scrapy.Field()
    # category_term_url = scrapy.Field()
    # book_url = scrapy.Field()
    # book_name = scrapy.Field()
    # book_file = scrapy.Field()
    book_list = scrapy.Field()
    crawl_date = scrapy.Field()


class ZlibBookItem(scrapy.Item):
    '''建立书详情页的Item'''
    book_url = scrapy.Field()
    book_name = scrapy.Field()
    book_author = scrapy.Field()
    book_category = scrapy.Field()
    book_publisher = scrapy.Field()
    book_language = scrapy.Field()
    book_pages = scrapy.Field()
    book_file = scrapy.Field()
    book_download = scrapy.Field()
    crawl_date = scrapy.Field()


