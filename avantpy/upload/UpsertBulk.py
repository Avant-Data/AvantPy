# -*- coding: utf-8 -*-
from urllib3.exceptions import InsecureRequestWarning
import concurrent.futures
import logging
import requests
import json


class UpsertBulk():

    def __init__(self, lst, **kwargs):
        self.log = logging.getLogger(__name__)
        self.baseurl = kwargs.get('baseurl', 'https://127.0.0.1')
        self.api = kwargs.get(
            'api', '/avantapi/avantData/index/bulk/general/upsert')
        self.url = kwargs.get('url', self.baseurl+self.api)
        self.cluster = kwargs.get('cluster', 'AvantData')
        self.verifySSL = kwargs.get('verifySSL', False)
        self.chunkSize = kwargs.get('chunkSize', 1000)
        self.threads = kwargs.get('threads', 10)
        self.indexed = 0
        requests.packages.urllib3.disable_warnings(
            category=InsecureRequestWarning)
        self.sendToIndex(lst)

    def uploadToIndex(self, chunk):
        jsonToSend = {'body': json.loads(json.dumps(chunk))}
        headers = {'cluster': self.cluster}
        responseBulk = requests.put(url=self.url,
                                    headers=headers,
                                    data=json.dumps(jsonToSend),
                                    verify=self.verifySSL)
        try:
            responseJson = json.loads(responseBulk.text)
            if responseJson.get('items'):
                successful, failed = (0, 0)
                for item in responseJson.get('items'):
                    try:
                        successful += item.get('update').get(
                            '_shards').get('successful')
                        failed += item.get('update').get('_shards').get('failed')
                    except:
                        failed += 1
                        self.log.warning(item.get('update').get('error'))
                if successful + failed > 0:
                    self.log.info('Successful: {}, Failed: {}'.format(successful, failed))
                    self.indexed += successful
        except Exception as e:
            self.log.warning(responseBulk.text+'\n'+e)

    def sendToIndex(self, listToIndex):
        if listToIndex:
            self.log.info('Total: {}'.format(len(listToIndex)))
            chunks = [listToIndex]
            if len(listToIndex) > self.chunkSize:
                chunks = [listToIndex[x:x+self.chunkSize]
                          for x in range(0, len(listToIndex), self.chunkSize)]
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
                executor.map(self.uploadToIndex, chunks)
            self.log.info('{} successfully indexed'.format(self.indexed))
            self.indexed = 0
        else:
            self.log.info('Empty list')
