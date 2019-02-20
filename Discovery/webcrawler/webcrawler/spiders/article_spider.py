import scrapy
from .. import items
from scrapy import signals
from scrapy import Spider

# crawler main class
class ArticleSpider(scrapy.Spider):
    name = "articles"
    urlList = [
        # 'https://www.3wcoffee.com/qfnews/detail?id=1324',
        # 'http://bharatapress.com/2019/01/29/general-electric-nysege-upgraded-by-valuengine-to-sell/'
    ]
    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'crawler.pipelines.CrawlerPipeline': 300,
    #     }
    # }

    # def __init__(self, urlList='', *args, **kwargs):
    #     print('init start')
    #     super(SiteCrawler, self).__init__(*args, **kwargs)
    #     # accept url args
    #     self.urls = urlList
    #     # print(str(self.urls))
    #     print('init end')

    def __init__(self, *args, **kwargs):
        # print("Existing settings: %s" % self.settings.attributes.keys())
        print('init start')
        # print(str(kwargs))
        # self.urlList = kwargs.pop('urlList').s
        # self.start_urls = kwargs.pop('urlList').split(',')
        super(ArticleSpider, self).__init__(*args, **kwargs)
        # endpoints = kwargs.get('urlList').split(',')
        # self.start_urls = [x for x in endpoints]
        self.urlList = kwargs.get('urlList')
        # self.urlList = kwargs.get('urlList').split(',')
        # self.urlList = ['http://www.neraca.co.id/article/112294/industri-kereta-api-nasional-berpeluang-jadi-pemain-global', 'http://www.energyland.info/news-show-tek-neftegaz-181914']
        # self.urlList = ['https://www.gastopowerjournal.com/projectsafinance/item/9345-ge-delivers-first-aero-derivative-gas-turbine-to-tobago']
        print('type: ' + str(type(self.urlList)))
        # print(str(self.urlList))
        print('init end')

    def start_requests(self):
        print('crawl start')
        # print(str(self.urlList))
        for url in self.urlList:
            # yield scrapy.Request(url=url, callback=self.parse)
            if url is not '':
                yield scrapy.Request(url=url, callback=self.parse)
                # print('type: ' + str(type(scrapy.Request(url=url, callback=self.parse))))
            # print('will parse content in url: ' + url)
        print('crawl end')

    def parse(self, response):
        print('parse start')
        item = items.ArticleItem(url=response.url, content=response.css('p').getall())
        # item['url'] = response.url
        # item['content'] = response.css('p').getall()
        # print(str(item['content'])
        # print(str(item))
        print('parse end')
        return item
    
    @classmethod
    def item_scraped(item, response, spider):
        print('******************SCRAPED ITEM')
        spider.logger.info('Item %s scraped with spider %s', spider.name, str(item))