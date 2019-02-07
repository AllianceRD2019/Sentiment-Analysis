from django.shortcuts import render
from django.http import HttpResponse
import os
import json
from watson_developer_cloud import DiscoveryV1
from Document.forms import ConfigForm

discovery = DiscoveryV1(
    version='2018-12-03',
    iam_apikey='PRU8Cm3QHZQRkbPaBBPHwpaipMh7iuE1Lh8JkW75eT0m',
    url='https://gateway-tok.watsonplatform.net/discovery/api')

# Collections API Credentials
START_URL = 'https://news.google.com/?hl=en-PH&gl=PH&ceid=PH:en'
COL_ID = 'df969925-6bf8-4178-a13a-347eb3a6f734'
CFG_ID = 'bd6910d0-adec-4864-9f1e-fe46a4780f0c'
ENV_ID = 'cc5ffbfc-b67e-4b5b-b98e-2c626a018060'

def home(request):
    # # Create credentials for the source that you are connecting to 
    # # using the Source Credentials API External link icon. 
    # # Record the returned credential_id of the newly created credentials.
    # # create_credentials(self, environment_id, source_type=None, credential_details=None, **kwargs)
    # resCred = discovery.create_credentials(environment_id=ENV_ID, source_type='web_crawl', credential_details={'credential_type': 'noauth', 'url': START_URL})
    # resCredJson = resCred.get_result()
    # print(resCredJson)

    # # Create a new configuration using the Configuration API External link icon. 
    # # This configuration must contain a source object which defines what should be crawled. 
    # # The source object must contain the credential_id that you recorded earlier.
    # # create_configuration(self, environment_id, name, description=None, 
    # # conversions=None, enrichments=None, normalizations=None, source=None, **kwargs)

    # resCfg = discovery.create_configuration(
    #     environment_id=ENV_ID, 
    #     name='WebCrawlerCfg', 
    #     description='Web Crawler Config', 
    #     conversions=None, 
    #     enrichments=[{
    #         'destination_field': 'enriched_text',
    #         'source_field': 'text',
    #         'enrichment_name': 'natural_language_understanding', 
    #         'options':{
    #             'features':{
    #                 'keywords':{
    #                     "sentiment": True,
    #                     "emotion": True,
    #                     "limit": 50
    #                 }, 
    #                 'entities':{
    #                     'sentiment': True,
    #                     'emotion': True,
    #                     'limit': 50,
    #                     'mentions': True,
    #                     'mention_types': True,
    #                     'sentence_locations': True,
    #                     'model': 'alchemy'
    #                 }, 
    #                 'sentiment':{
    #                     'document': True,
    #                     "targets": [
    #                         "MHI",
    #                         "Mitsubishi",
    #                         "Mitsubishi Heavy Industries"
    #                     ]
    #                 }, 
    #                 'emotion': {
    #                     'document': True,
    #                     "targets": [
    #                         "MHI",
    #                         "Mitsubishi",
    #                         "Mitsubishi Heavy Industries"
    #                     ]
    #                 }, 
    #                 'categories':{}, 
    #                 'semantic_roles': {
    #                     'entities': True,
    #                     'keywords': True,
    #                     'limit': 50
    #                 },
    #                 'relations': {
    #                     'model': 'en-news'
    #                 }, 
    #                 'concepts': {
    #                     'limit': 50,
    #                 }
    #             }, 
    #             'language': 'en', 
    #             'model': 'contract'
    #         }
    #     }],
    #     normalizations=None, 
    #     source={
    #         'type': 'web_crawl', 
    #         'credential_id': resCredJson['credential_id'], 
    #         'schedule':{
    #             'enabled': 'true', 
    #             'time_zone': 'Asia/Taipei', 
    #             'frequency': 'daily'
    #         }, 
    #         'options':{
    #             'urls':{
    #                 'url': START_URL, 
    #                 'crawl_speed': 'aggressive', 
    #                 'maximum_hops': 20
    #             }
    #         }
    #     }
    # )
    # resCfgJson = resCfg.get_result()
    # print(resCfgJson)

    # # Create a new collection using the Collections API External link icon. 
    # # The object defining the collection must contain the configuration_id that you recorded earlier.
    # new_collection = discovery.create_collection(environment_id=ENV_ID, name='WebCrawlerAPI', description='Web Crawler API', configuration_id=resCfgJson['configuration_id'], language='en').get_result()
    # print(json.dumps(new_collection, indent=2))

    # # The source crawl begins as soon as the collection is created, 
    # # and then again on the frequency that you specified. 
    # # Note: If you modify anything in the source object of the configuration 
    # # a new crawl will be started (or restarted if one is already running) at that time.

    return render(request, 'Document/home.html')

def schema(request):

    return render(request, 'Document/schema.html')

def queries(request):

    return render(request, 'Document/queries.html')

def metrics(request):

    return render(request, 'Document/metrics.html')

def update(request):
    if request.method == 'POST':
        form = ConfigForm(request.POST)
        if form.is_valid():
            urlSrc = request.POST.get('url', '')
            # create credentials, config, and collections once in WDS Tooling
            # update config source field (URLS) first
            # then, update collections to reflect 
            # config updates based on new input URLS from user

            resGetCfg = discovery.get_configuration(ENV_ID, CFG_ID).get_result()
            print(json.dumps(resGetCfg, indent=2))

            # update SRC
            urlKeyVal = {'url': urlSrc, 'crawl_speed': 'aggressive', 'maximum_hops': 20}
            if urlSrc not in resGetCfg['source']['options']['urls']:
                resGetCfg['source']['options']['urls'].append(urlKeyVal)
            
            resUpdateCfg = discovery.update_configuration(environment_id=ENV_ID, configuration_id=CFG_ID, name=resGetCfg['name'], description=resGetCfg['description'], enrichments=['enrichments'], source=resGetCfg['source'])

            print(json.dumps(resUpdateCfg, indent=2))

            resGetCol = discovery.get_collection(ENV_ID, COL_ID)
            resUpdateCol = discovery.update_collection(ENV_ID, COL_ID, name=resGetCol['name'], description=resGetCol['description'], configuration_id=resGetCol['configuration_id'])

            print(json.dumps(resUpdateCol, indent=2))

    else:
        form = ConfigForm()
    return render(request, 'Document/sucessUpdate.html', {
                                                    'form': form, 
                                                    'cfgName': resGetCfg['name'],
                                                    'colName': resGetCol['name'],
                                                    'urlSrc': urlSrc,
                                                }
                )



                	
{
    'credential_id': 'a4b69966-7765-49c6-bcf5-cbd6c7c5d136',
    'options': {
        'urls': [
                {
                    'url': 'https://mhi.com/news/'
                },
                    'https://news.google.com/?hl=en-PH&gl=PH&ceid=PH:en'
            ]
            },
 'schedule': {
     'enabled': 'true',
    'frequency': 'daily',
    'time_zone': 'Asia/Taipei'
    },
 'type': 'web_crawl',
 'url_batches': [{'urls': ['https://mhi.com/news/']}]}