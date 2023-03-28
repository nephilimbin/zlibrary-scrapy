import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from items import ZlibCateURLItem, ZlibCateTermURLItem, ZlibBookURLItem, ZlibBookItem
import datetime
import pandas as pd

BASE_URL = r'' # Set you own base url
cookies = r'' # Set your cookies

class ZlibCateURLSpider(scrapy.Spider):
    '''Zlibrary的目录爬虫'''
    # 设置scrpit名称
    name = 'zlib_category_url'
    # 设置scrapy抓取的域名
    allowed_domains = ['carbon.pm']
    # 设置起始url
    start_urls = ['']
    # 设置Zlib分配私域地址
    

    def start_requests(self):
        '''设置cookied登录'''
        cookies = {i.split("=")[0]: i.split("=")[1]
                   for i in cookies.split("; ")}
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse_start_urls, 
            cookies=cookies
        )
    
    def parse_start_urls(self, response):
        '''解析目录页'''
        item = ZlibCateURLItem()
        # 结果集
        cate_list = []
        # 获得目录链接标签
        xpath_href = response.xpath('//li[@class="subcategory-name"]/a[1]/@href').extract() # /category/716/Others
        for index, category_href in enumerate(xpath_href):
            if index >= 0:
                category_url = self.BASE_URL + category_href
                cate_list.append(category_url)
        # 添加item值
        item['cate_list'] = cate_list
        item['crawl_date'] = datetime.datetime.utcnow()
        yield item

class ZlibCateTermURLSpider(scrapy.Spider):
    '''Zlibrary的爬虫'''
    # 设置scrpit名称
    name = 'zlib_cate_term_url'
    # 设置scrapy抓取的域名
    allowed_domains = ['carbon.pm']
    # 设置起始url
    start_urls = ['']

    def start_requests(self):
        '''设置cookied登录'''
        cookies = {i.split("=")[0]: i.split("=")[1]
                   for i in cookies.split("; ")}
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse_start_urls, # 如果不需要解析，直接yield请求即可
            cookies=cookies
        )
    
    def parse_start_urls(self, response):
        '''解析目录页'''
        # 获得目录链接标签
        xpath_href = response.xpath('//li[@class="subcategory-name"]/a[1]/@href').extract() # /category/716/Others
        for index, category_href in enumerate(xpath_href):
            if index >= 0:
                category_url = self.BASE_URL + category_href
                yield scrapy.Request(category_url, callback=self.parse_category)

    def parse_category(self, response):
        '''解析目录内分类,获得小组url'''
        # 创建Item实例
        item = ZlibCateTermURLItem()
        term_list = []
        category_term_names = response.xpath('//div[@class="termWrap "]/a/text()').extract()
        for index, term_name in enumerate(category_term_names):
            if index >= 0: # 控制分组数量，测试用
                # 获得目录分组的url
                category_url = response.url
                category_term_url = response.url + f'/s/?term={term_name}&page=1' # 无法直接获取url，需要通过拼接字符串url进行请求
                category_term_name = term_name
                category_term_booknum = response.xpath('//div[@class="termWrap "]/sup/text()').extract()[index]
                term_list.append((category_url, category_term_url, category_term_name, category_term_booknum))
                # yield scrapy.Request(category_term_url, callback=self.parse_category_term, meta={'item': item}) 
        item['term_list'] = term_list
        item['crawl_date'] = datetime.datetime.today()
        yield item



class ZlibBookURLSpider(scrapy.Spider):
    '''Zlibrary的爬虫(通过链接地址爬取)'''
    # 设置scrpit名称
    name = 'zlib_book_url'
    # 设置scrapy抓取的域名
    allowed_domains = ['carbon.pm']
    # 设置起始url
    start_urls = [''] # 目录页

    def start_requests(self):
        '''设置cookied登录'''
        cookies = {i.split("=")[0]: i.split("=")[1]
                   for i in cookies.split("; ")}
        # 读取ZlibCateTermURLSpider类爬取的地址
        df = pd.read_excel(r'./spiders/zlib_cate_term_url.xlsx')
        booknum = df.category_term_booknum.to_list()
        items_per_page = 50
        pages = []
        for num in booknum:
            if num > 1000:
                pages.append(20)
            else:
                pages.append((num + items_per_page - 1)//items_per_page)
        for index, url in enumerate(df.category_term_url.to_list()):
            yield scrapy.Request(
                url,
                callback=self.parse_category_term, # 如果不需要解析，直接yield请求即可
                cookies=cookies,
                meta={'page': pages[index]}
            )
    
    def parse_category_term(self, response):
        '''解析分类中的小组,获得书url'''
        # 获得分类中的小组的页数
        page = response.meta['page']
        # 获得书本信息列表
        book_list = []
        # 获得书url
        xpaths = response.xpath('//h3[@itemprop="name"]/a/@href').extract() # /book/2631061/558336
        for index, url_suffix in enumerate(xpaths): 
            if index >= 0: # 控制书本数，测试用
                # 获得书的部分信息
                category_term_url = response.url
                book_url = self.BASE_URL + url_suffix # 无法直接获取url，需要通过拼接字符串url进行请求
                book_name = response.xpath('//h3[@itemprop="name"]/a/text()').extract()[index]
                book_file = response.xpath('//div[@class="bookProperty property__file"]/child::*[last()]').extract()[index] # 在书简介中有下载地址,但不全,所以提取标签页后期处理
                book_list.append((category_term_url, book_url, book_name, book_file))
        # 创建Item对象
        item = ZlibBookURLItem()
        item['book_list'] = book_list
        item['crawl_date'] = datetime.datetime.today()
        yield item


        # 请求下一页 
        if int(response.url.split('=')[-1]) < page: # 网站每个term最大翻页为20
            print(response.url)
            curent_page = str(int(response.url.split('=')[-1]) + 1)
            url_parts = response.url.split('=')
            url_parts[-1] = curent_page
            next_page = '='.join(url_parts)
            
            yield scrapy.Request(next_page, callback=self.parse_category_term, meta={'page': page})




