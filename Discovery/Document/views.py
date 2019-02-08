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
COL_ID = 'ef4a0178-7f65-4fa6-b889-6f31a7c04cc2'
# CFG_ID = 'e6c8aaa5-00d2-491e-b959-4463aa126bec'
ENV_ID = 'cc5ffbfc-b67e-4b5b-b98e-2c626a018060'

def home(request):

    resColList = discovery.list_collections(ENV_ID).get_result()
    # print(resColList)

    colIdSet = []
    colNameSet = []
    configIdSet = []
    langSet = []
    statSet = []
    descSet = []
    createdSet = []
    updatedSet = []

    for collection in resColList['collections']:
        colIdSet.append(collection['collection_id'])
        colNameSet.append(collection['name'])
        configIdSet.append(collection['configuration_id'])
        langSet.append(collection['language'])
        statSet.append(collection['status'])
        descSet.append(collection['description'])
        createdSet.append(collection['created'])
        updatedSet.append(collection['updated'])

    print('colNameSet:' + str(colNameSet))
    print('colDetails:' + str(list(zip(colIdSet, colNameSet, configIdSet, langSet, statSet, descSet, createdSet, updatedSet))))

    return render(
        request, 
        'Document/home.html', 
        {
            'colDetails' : zip(colIdSet, colNameSet, configIdSet, langSet, statSet, descSet, createdSet, updatedSet)
        }
    )
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
            
            resGetCol = discovery.get_collection(ENV_ID, COL_ID).get_result()
            CFG_ID = resGetCol['configuration_id']

            resGetCfg = discovery.get_configuration(ENV_ID, CFG_ID).get_result()
            print('1.) resGetCfg')
            print(json.dumps(resGetCfg, indent=2))
            print('------------------------------------------------------------')

            # update SRC

            # "source": {
            #     "options": {},
            #     "schedule": {
            #     "enabled": true,
            #     "frequency": "weekly",
            #     "time_zone": "America/New_York"
            #     },
            #     "type": "web_crawl"
            # }

            urlKeyVal = {'url': urlSrc, 'crawl_speed': 'aggressive', 'maximum_hops': 20}
            missingUrl = {"urls": []}

            if "urls" not in resGetCfg['source']['options']:
                resGetCfg['source']['options'].update(missingUrl)
            
            if urlSrc not in resGetCfg['source']['options']['urls']:
                resGetCfg['source']['options']['urls'].append(urlKeyVal)
            
            print('2.) resGetCfg[''source'']')
            print(json.dumps(resGetCfg['source'], indent=2))
            print('------------------------------------------------------------')

            discovery.delete_configuration(ENV_ID, resGetCfg['configuration_id'])

            print('2.5) resGetCfg[''source''] After deleting previous configuration')
            rest = resGetCfg['source']
            print(str(rest))
            print('------------------------------------------------------------')

            resNewCfg = discovery.create_configuration(
                ENV_ID, 
                name='WebCrawlerConfig000', 
                description='Web Crawler Configuration', 
                conversions=None, 
                enrichments=resGetCfg['enrichments'],
                normalizations=None, 
                source=resGetCfg['source'],
            ).get_result()

            CFG_ID = resNewCfg['configuration_id']

            print('2.5.5) resNewCfg[''source'']')
            print(json.dumps(resNewCfg['source'], indent=2))
            print('------------------------------------------------------------')

            # resUpdateCfg = discovery.update_configuration(environment_id=ENV_ID, configuration_id=CFG_ID, name=resGetCfg['name'], description=resGetCfg['description'], enrichments=resGetCfg['enrichments'], source=newSrc).get_result()

            print('3.)resNewCfg')
            print(json.dumps(resNewCfg, indent=2))
            print('------------------------------------------------------------')

            resGetCfg = discovery.get_configuration(ENV_ID, CFG_ID).get_result()
            print('4.) resGetCfg (again)')
            print(json.dumps(resGetCfg, indent=2))
            # print(str(resGetCfg))

            print('------------------------------------------------------------')


            resGetCol = discovery.get_collection(ENV_ID, COL_ID).get_result()
            resUpdateCol = discovery.update_collection(ENV_ID, COL_ID, name=resGetCol['name'], description=resGetCol['description'], configuration_id=resNewCfg['configuration_id']).get_result()

            print('5.) resUpdateCol')
            print(json.dumps(resUpdateCol, indent=2))
            print('------------------------------------------------------------')


    else:
        form = ConfigForm()
    return render(
        request, 
        'Document/successUpdate.html', 
        {
            'form': form, 
            'cfgName': resGetCfg['name'],
            'colName': resGetCol['name'],
            'urlSrc': urlSrc,
        }
    )