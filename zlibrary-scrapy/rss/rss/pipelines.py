# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from items import ZlibBookItem, ZlibBookURLItem, ZlibCateURLItem, ZlibCateTermURLItem
import pymysql


class ZlibCateURLPipeline:
    '''建立书籍目录的存储类'''
    def open_spider(self, spider):
        '''爬虫开始时建立mysql连接'''
        data_config = spider.settings['DATABASE_CONFIG']
        # 建立连接
        self.conn = pymysql.connect(**data_config)
        # 定义游标
        self.cur = self.conn.cursor()
    # 数据存储
    def process_item(self, item, spider):
        if isinstance(item, ZlibCateURLItem):
            sql = 'insert into zlib_cate_url(category_url, crawl_date) values(%s,%s)'
            data_list = []
            for category_url in item['cate_list']:
                category_url, category_term_url, category_term_name, category_term_booknum = category_url
                data_list.append((category_url, item['crawl_date']))
            self.cur.executemany(sql, data_list)
            self.conn.commit()
            return item
        else:
            return DropItem

    def close_spider(self, spider):
        '''爬虫结束时关闭数据库'''
        self.cur.close()
        self.conn.close()

class ZlibCateTermURLPipeline:
    '''建立书籍目录的存储类'''
    def open_spider(self, spider):
        '''爬虫开始时建立mysql连接'''
        data_config = spider.settings['DATABASE_CONFIG']
        # 建立连接
        self.conn = pymysql.connect(**data_config)
        # 定义游标
        self.cur = self.conn.cursor()
    # 数据存储
    def process_item(self, item, spider):
        if isinstance(item, ZlibCateTermURLItem):
            sql = 'insert into zlib_cate_term_url(category_url, category_term_url, category_term_name, category_term_booknum, crawl_date) \
                values(%s,%s,%s,%s,%s)'
            data_list = []
            for term in item['term_list']:
                category_url, category_term_url, category_term_name, category_term_booknum = term
                data_list.append((category_url, category_term_url, category_term_name, category_term_booknum, item['crawl_date']))
            self.cur.executemany(sql, data_list)
            self.conn.commit()
            return item
        else:
            return DropItem

    def close_spider(self, spider):
        '''爬虫结束时关闭数据库'''
        self.cur.close()
        self.conn.close()

class ZlibBookURLPipeline:
    '''建立书籍信息的存储类(通过链接爬取)'''
    def open_spider(self, spider):
        '''建立mysql连接'''
        data_config = spider.settings['DATABASE_CONFIG']
        # 建立连接
        self.conn = pymysql.connect(**data_config)
        # 定义游标
        self.cur = self.conn.cursor()

    # 数据存储
    def process_item(self, item, spider):
        if isinstance(item, ZlibBookURLItem):
            sql = "insert into zlib_book_url(category_term_url, book_url, book_name, book_file, crawl_date)  \
                    values(%s,%s,%s,%s,%s)"
            data_list = []
            for book in item['book_list']:
                category_term_url, book_url, book_name, book_file = book
                data_list.append((category_term_url, book_url, book_name, book_file, item['crawl_date']))
            self.cur.executemany(sql, data_list)
            self.conn.commit()
            return item
        else:
            return DropItem

    def close_spider(self, spider):
        '''关闭数据库'''
        self.cur.close()
        self.conn.close()

class ZlibBookPipeline:
    '''建立书籍信息的存储类'''
    def open_spider(self, spider):
        '''建立mysql连接'''
        data_config = spider.settings['DATABASE_CONFIG']
        # 建立连接
        self.conn = pymysql.connect(**data_config)
        # 定义游标
        self.cur = self.conn.cursor()

    # 数据存储
    def process_item(self, item, spider):
        if isinstance(item, ZlibBookItem):
            sql = "select book_name from zlib_book where book_name=%s and book_author=%s"
            self.cur.execute(sql, (item['book_name'], item['book_author']))
            if not self.cur.fetchone():
                sql = "insert into zlib_book(category_url,category_term_url,category_term_name,book_url,book_name, \
                book_author,book_category,book_publisher,book_language,book_pages,book_file,book_download,crawl_date) \
                      values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                self.cur.execute(sql, (
                    item['category_url'],
                    item['category_term_url'],
                    item['category_term_name'],
                    item['book_url'],
                    item['book_name'],
                    item['book_author'],
                    item['book_category'],
                    item['book_publisher'],
                    item['book_language'],
                    item['book_pages'],
                    item['book_file'],
                    item['book_download'],
                    item['crawl_date'],
                ))
                self.conn.commit()
            return item
        else:
            return DropItem

    def close_spider(self, spider):
        '''关闭数据库'''
        self.cur.close()
        self.conn.close()

