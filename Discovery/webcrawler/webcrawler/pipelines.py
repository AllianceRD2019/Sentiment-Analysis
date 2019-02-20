# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from html.parser import HTMLParser
from Document.models import Article

class WebcrawlerPipeline(object):
    def __init__(self):
        print("Initializing Pipeline")

    def open_spider(self, spider):
        print("Open Spider")
        
    def close_spider(self, spider):
        print("Close Spider")

    def process_item(self, item, spider):
        print("***********************PIPELINE")
        print('Start Pipeline')
        # Get Article where url == response.url
        article = Article.objects.get(url=item["url"])
        print(str(article))
        item['content'] = '\n'.join(map(str, item['content']))

        # remove html
        HTMLCleaner = MLStripper()
        HTMLCleaner.feed(item['content'])

        item['content'] = HTMLCleaner.get_data()
        print("***********************CONTENT: " + str(item['content']))

        # save parsed item as article content
        article.article_content = item['content']
        article.save()
        print('successfully saved to db.')
        return item

# Class used to remove HTML tags from a string
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)
