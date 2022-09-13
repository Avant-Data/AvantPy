# -*- coding: utf-8 -*-
from urllib3.exceptions import InsecureRequestWarning
from collections import Counter
import concurrent.futures
import logging
import requests
import json
import typing


class UpsertBulk():

    def __init__(self, lst: typing.Union[list, tuple, set],
                 baseurl: typing.Optional[str] = 'https://127.0.0.1',
                 api: typing.Optional[str] = '/avantapi/avantData/index/bulk/general/upsert',
                 cluster: typing.Optional[str] = 'AvantData',
                 verifySSL: typing.Optional[bool] = False,
                 chunkSize: typing.Optional[int] = 1000,
                 threads: typing.Optional[int] = 1,
                 **kwargs):
        self.log = logging.getLogger(__name__)
        self.baseurl = baseurl
        self.api = api
        self.cluster = cluster
        self.verifySSL = verifySSL
        self.chunkSize = chunkSize
        self.threads = threads
        self.url = kwargs.get('url', self.baseurl+self.api)
        self.updated, self.created, self.failed = (0, 0, 0)
        self.errors = Counter()
        requests.packages.urllib3.disable_warnings(
            category=InsecureRequestWarning)
        self.sendToIndex(lst)

    def uploadToIndex(self, chunk: typing.Union[list, tuple, set]):
        jsonToSend = {'body': json.loads(json.dumps(chunk))}
        headers = {'cluster': self.cluster}
        responseBulk = requests.put(url=self.url,
                                    headers=headers,
                                    data=json.dumps(jsonToSend),
                                    verify=self.verifySSL)
        try:
            responseJson = json.loads(responseBulk.text)
            if responseJson.get('items'):
                results = Counter(item.get('update').get('result')
                                  for item in responseJson.get('items'))
                self.updated += results.get('updated', 0)
                self.created += results.get('created', 0)
                if responseJson.get('errors'):
                    self.errors.update(Counter(item.get('update').get('error').get(
                        'reason') for item in responseJson.get('items') if item.get('update').get('error')))
                self.log.info('Updated: {}, Created {}. '.format(
                    self.updated, self.created))
        except Exception as e:
            self.log.debug(responseBulk.text)
            self.log.warning(e)

    def sendToIndex(self, listToIndex: typing.Union[list, tuple, set]):
        if listToIndex:
            self.log.info('Total: {}'.format(len(listToIndex)))
            chunks = [listToIndex]
            if self.threads > 1:
                if len(listToIndex) > self.chunkSize:
                    chunks = [listToIndex[x:x+self.chunkSize]
                              for x in range(0, len(listToIndex), self.chunkSize)]
                with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
                    executor.map(self.uploadToIndex, chunks)
            else:
                self.uploadToIndex(listToIndex)
            if self.errors:
                self.failed += sum(self.errors.values())
                for k, v in self.errors.items():
                    self.log.warning('{} failed. Reason: {}'.format(v, k))
            self.log.info('{} successfully executed with {} failures'.format(
                self.updated+self.created, self.failed))
        else:
            self.log.info('Empty list')
