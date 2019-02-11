from django.shortcuts import render
from django.http import HttpResponse
import os
import json
from watson_developer_cloud import DiscoveryV1
from Document.forms import ConfigForm, CsvUploadForm
import csv

discovery = DiscoveryV1(
    version='2018-12-03',
    iam_apikey='PRU8Cm3QHZQRkbPaBBPHwpaipMh7iuE1Lh8JkW75eT0m',
    url='https://gateway-tok.watsonplatform.net/discovery/api')

# Collections API Credentials
START_URL = 'https://news.google.com/?hl=en-PH&gl=PH&ceid=PH:en'
COL_ID = 'd165e602-378e-4f91-aea5-42860f2880f6'
# CFG_ID = 'e6c8aaa5-00d2-491e-b959-4463aa126bec'
ENV_ID = 'cc5ffbfc-b67e-4b5b-b98e-2c626a018060'

def home(request):
    csvUploadForm = CsvUploadForm()
    configForm = ConfigForm()
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
            'csvUploadForm':csvUploadForm,
            'configForm': configForm, 
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
        configForm = ConfigForm(request.POST)
        if configForm.is_valid():
            urlSrc = request.POST.get('url', '')
            # create credentials, config, and collections once in WDS Tooling
            # update config source field (URLS) first
            # then, update collections to reflect 
            # config updates based on new input URLS from user
            
            resGetCol = discovery.get_collection(ENV_ID, COL_ID).get_result()
            CFG_ID = resGetCol['configuration_id']

            resGetCfg = discovery.get_configuration(ENV_ID, CFG_ID).get_result()
            print('1.) resGetCfg Before Update')
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

            urlKeyValEntry = {
                'url': urlSrc,
                # 'limit_to_starting_hosts': True,
                # 'crawl_speed': 'normal',
                # 'allow_untrusted_certificate': False,
                # 'maximum_hops': 20,
                # 'request_timeout': 3000,
                # 'override_robots_txt': False
            }

            # inside source[options]
            urlSubDict = {'urls': []}
            # inside source
            urlBatchesSubDict = {'url_batches': [{'urls': []}]} 

            # if urls not found in source[options], url_batches also does not exist
            if 'urls' not in resGetCfg['source']['options']:
                resGetCfg['source']['options'].update(urlSubDict)
            
            if 'url_batches' not in resGetCfg['source']:
                resGetCfg['source'].update(urlBatchesSubDict)
            
            if urlKeyValEntry['url'] not in resGetCfg['source']['options']['urls']:
                resGetCfg['source']['options']['urls'].append(urlKeyValEntry)
            
            if urlSrc not in resGetCfg['source']['url_batches'][0]['urls']:
                resGetCfg['source']['url_batches'][0]['urls'].append(urlSrc)
            
            # resGetCfg['source']['options']['urls'][-1]['url'] = urlSrc
            # resGetCfg['source']['options']['urls'][-1]['crawl_speed'] = 'normal'
            # resGetCfg['source']['options']['urls'][-1]['maximum_hops'] = 20

            resGetCfg['source']['schedule']['frequency'] = 'daily'
            
            print('2.) resGetCfg On Update')
            print(json.dumps(resGetCfg, indent=2))
            print('type: ' + str(type(resGetCfg['source'])))
            print('url keyval type: ' + str(type(urlKeyValEntry)))
            print('------------------------------------------------------------')

            # discovery.delete_configuration(ENV_ID, resGetCfg['configuration_id'])

            # print('2.5) resGetCfg[''source''] After deleting previous configuration')
            # print(json.dumps(resGetCfg['source'], indent=2))
            # print('------------------------------------------------------------')

            # resNewCfg = discovery.create_configuration(
            #     ENV_ID, 
            #     name=resGetCfg['name'], 
            #     description=resGetCfg['description'], 
            #     conversions=None, 
            #     enrichments=resGetCfg['enrichments'],
            #     normalizations=None, 
            #     source=resGetCfg['source'],
            # ).get_result()

            # CFG_ID = resNewCfg['configuration_id']

            # print('2.5.5) resNewCfg[''source'']')
            # print(json.dumps(resNewCfg['source'], indent=2))
            # print('------------------------------------------------------------')

            resUpdateCfg = discovery.update_configuration(environment_id=ENV_ID, configuration_id=resGetCfg['configuration_id'], name=resGetCfg['name'], description=resGetCfg['description'], enrichments=resGetCfg['enrichments'], source=resGetCfg['source']).get_result()

            print('3.)resUpdateCfg After Update')
            print('resGetCfg')
            print(json.dumps(resGetCfg, indent=2))
            print('resUpdateCfg')
            print(json.dumps(resUpdateCfg, indent=2))
            print('------------------------------------------------------------')

            resGetCol = discovery.get_collection(ENV_ID, COL_ID).get_result()
            resUpdateCol = discovery.update_collection(environment_id=ENV_ID, collection_id=COL_ID, name=resGetCol['name'], description=resGetCol['description'], configuration_id=resUpdateCfg['configuration_id']).get_result()

            print('5.) resUpdateCol After Config Update')
            print(json.dumps(resUpdateCol, indent=2))
            print('------------------------------------------------------------')


    else:
        configForm = ConfigForm()

    print(str(resUpdateCfg['source']['options']['urls']))
    
    if not any(subdDict.get('url', None) == urlSrc for subdDict in resUpdateCfg['source']['options']['urls']):
        errorMessage = 'Failed to add URL to web crawler.'
        return render(
            request, 
            'Document/error.html', 
            {
                'configForm': configForm, 
                'errorMessage': errorMessage
            }
        )
    else:
        return render(
            request, 
            'Document/success.html', 
            {
                'configForm': configForm, 
                'cfgName': resGetCfg['name'],
                'colName': resGetCol['name'],
                'urlSrc': urlSrc,
                'type': 'addUrl',
            }
        )

def upload(request):
    if request.method == 'POST':
        csvUploadForm = CsvUploadForm(request.POST, request.FILES)
        if csvUploadForm.is_valid():
            inputFile = request.FILES['csvFile']
            inputFileName = inputFile.name
            filePath = os.path.join('media/Document/csv/', inputFileName)
            # inputFileNameNoExt, fileExt = os.path.splitext('media/Document/csv/' + inputFileName)

            resGetCol = discovery.get_collection(ENV_ID, COL_ID).get_result()
            CFG_ID = resGetCol['configuration_id']
            resGetCfg = discovery.get_configuration(ENV_ID, CFG_ID).get_result()

            if not os.path.exists(filePath):
                csvUploadForm.save()    

            with open(inputFileName) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                resGetCol = discovery.get_collection(ENV_ID, COL_ID).get_result()
                CFG_ID = resGetCol['configuration_id']
                resGetCfg = discovery.get_configuration(ENV_ID, CFG_ID).get_result()

                # inside source[options]
                urlSubDict = {'urls': []}
                # inside source
                urlBatchesSubDict = {'url_batches': [{'urls': []}]} 

                # if urls not found in source[options], url_batches also does not exist
                if 'urls' not in resGetCfg['source']['options']:
                    resGetCfg['source']['options'].update(urlSubDict)
                
                if 'url_batches' not in resGetCfg['source']:
                    resGetCfg['source'].update(urlBatchesSubDict)
                
                for row in csv_reader:
                    urlSrc = row[0]
                    urlKeyValEntry = {
                        'url': urlSrc,
                        # 'limit_to_starting_hosts': True,
                        # 'crawl_speed': 'normal',
                        # 'allow_untrusted_certificate': False,
                        # 'maximum_hops': 20,
                        # 'request_timeout': 3000,
                        # 'override_robots_txt': False
                    }

                    if urlKeyValEntry['url'] not in resGetCfg['source']['options']['urls']:
                        resGetCfg['source']['options']['urls'].append(urlKeyValEntry)
                
                    if urlSrc not in resGetCfg['source']['url_batches'][0]['urls']:
                        resGetCfg['source']['url_batches'][0]['urls'].append(urlSrc)
                    
                    # resGetCfg['source']['options']['urls'][-1]['url'] = urlSrc
                    # resGetCfg['source']['options']['urls'][-1]['crawl_speed'] = 'normal'
                    # resGetCfg['source']['options']['urls'][-1]['maximum_hops'] = 20
                    # resGetCfg['source']['schedule']['frequency'] = 'daily'
                    
                resUpdateCfg = discovery.update_configuration(environment_id=ENV_ID, configuration_id=resGetCfg['configuration_id'], name=resGetCfg['name'], description=resGetCfg['description'], enrichments=resGetCfg['enrichments'], source=resGetCfg['source']).get_result()

                print('Source URLS after file upload')
                print(json.dumps(resUpdateCfg, indent=2))
                print('------------------------------------------------------------')

                resGetCol = discovery.get_collection(ENV_ID, COL_ID).get_result()
                resUpdateCol = discovery.update_collection(environment_id=ENV_ID, collection_id=COL_ID, name=resGetCol['name'], description=resGetCol['description'], configuration_id=resUpdateCfg['configuration_id']).get_result()

                print('Collection after file upload')
                print(json.dumps(resUpdateCol, indent=2))
                print('------------------------------------------------------------')

            return render(request, 'Document/success.html', {
                'csvUploadForm': csvUploadForm,
                'type': 'uploadCsv',
                'inputFileName': inputFileName,
                'cfgName': resGetCfg['name'],
                'colName': resGetCol['name'],
            })
    else:
        csvUploadForm = CsvUploadForm()
    return render(request, 'Document/error.html', {
            'csvUploadForm': csvUploadForm,
            'type': 'uploadCsv',
            'errorMessage': 'No File Uploaded.',
        })
        