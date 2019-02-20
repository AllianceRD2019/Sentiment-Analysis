from django.shortcuts import render
from django.http import HttpResponse
from Document.forms import ConfigForm, CsvUploadForm
from Document.models import Article
from django.conf import settings

# scrapy dependencies
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from webcrawler.webcrawler import settings
# from crawler.crawler.spiders.site_crawler import SiteCrawler
from webcrawler.webcrawler.spiders.article_spider import ArticleSpider

import csv
import os


def home(request):
    csvUploadForm = CsvUploadForm()
    configForm = ConfigForm()

    return render(
        request, 
        'Document/home.html', 
        {
            'csvUploadForm':csvUploadForm,
            'configForm': configForm,
        }
    )

def schema(request):
    return render(request, 'Document/schema.html')

def queries(request):
    return render(request, 'Document/queries.html')

def metrics(request):
    return render(request, 'Document/metrics.html')

def update(request):
    return render( request, 'Document/success.html')

def upload(request):
    if request.method == 'POST':
        csvUploadForm = CsvUploadForm(request.POST, request.FILES)
        if csvUploadForm.is_valid():
            # if os.path.exists(filePath):
            #     # overwrite if exists
            #     os.remove(os.path.join(settings.MEDIA_ROOT, articleName))
            #     csvUploadForm.save()

            # with open(articleName, encoding="utf8") as csv_file:
            #     csv_reader = csv.reader(csv_file, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
            #     # skip header
            #     next(csv_reader, None)
            #     for row in csv_reader:
            #         date, headline, url, opening_text, source, country, subregion, language = row[0:]
            #         article = Article()
            #         article.date = date
            #         article.headline = headline
            #         article.url = url
            #         article.opening_text = opening_text
            #         article.source = source
            #         article.country = country
            #         article.subregion = subregion
            #         article.language = language
            #         article.save()

            article = request.FILES['csvFile']
            articleName = article.name
            
            # Get field value 'url' for all Article objects
            crawlUrls = list(Article.objects.all().values_list('url', flat=True))
            print('curr path: ' + os.path.dirname(os.path.realpath(__file__)))
            print('list size: ' + str(len(crawlUrls)))
            
            # execute scraper passing list of urls as argument
            # os.system("scrapy runspider site_crawler.py -a urls=" + crawlUrls)
            
            print('BOT_NAME: ' + settings.BOT_NAME)
            print('ITEM_PIPELINES: ' + str(settings.ITEM_PIPELINES))
            runner = CrawlerRunner(get_project_settings())
            
            d = runner.crawl(crawler_or_spidercls=ArticleSpider(), urlList=crawlUrls)
            d.addBoth(lambda _: reactor.stop())
            reactor.run(installSignalHandlers=0) # the script will block here until the crawling is finished
            # reactor.run(0)
            
            # os.system("cd ../webcrawler && scrapy crawl articles -a urlList=" + str(crawlUrls))


            # spider = SiteCrawler(urlList=crawlUrls)
            # process = CrawlerProcess({
            #     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
            # })
            # process.crawl(spider)
            # print('begin crawl')
            # print('spider.urls: ' + str(spider.urls))
            # process.start()
            # print('end crawl')

            return render(request, 'Document/success.html', {
                'csvUploadForm': csvUploadForm,
                'type': 'uploadCsv',
                'articleName': articleName,
                'successMessage': 'Successfully uploaded ' + articleName + ' to DB.'
            })
    else:
        csvUploadForm = CsvUploadForm()
    return render(request, 'Document/error.html', {
            'csvUploadForm': csvUploadForm,
            'type': 'uploadCsv',
            'errorMessage': 'No File Uploaded.',
        })
