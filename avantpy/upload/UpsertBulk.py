# -*- coding: utf-8 -*-
from urllib3.exceptions import InsecureRequestWarning
from collections import Counter
import concurrent.futures
import logging
import requests
import json
from typing import Optional, Union, List, Tuple, Set, Any


class UpsertBulk:
    """Bulk Uploader

    A class to manage bulk uploads of data

    Args:
        data (list(dict)): List of dictionaries to be indexed [{"id":..., "index":..., "type":..., ...},...]
        baseurl (str, optional): baseurl to execute the upsert bulk 
        api (str, optional): endpoint where the connection with database is set
        cluster (str, optional): header parameter for communication with the api
        verifySSL (bool, optional): bool to verify SSL of requests
        chunkSize (int, optional): Number of documents to send in each bulk requests
        threads (int, optional): Number of threads to send each chunk of documents
        url (str, optional): Default to join the url path with api path
    Returns:
        The generated md5 hash
    Attributes:
        updated (int): Number of documents successfully updated
        created (int): Number of documents successfully created
        failed (int): Number of documents that failed indexing
        errors (dict): Dict subclass for counting hashable objects from collections (Counter)
        log (logger): Logger with __name__ of module 'logging'
        data (list(dict)): List of dictionaries to be indexed [{"id":..., "index":..., "type":..., ...},...]
        baseurl (str): baseurl to execute the upsert bulk 
        api (str): endpoint where the connection with database is set
        cluster (str): header parameter for communication with the api
        verifySSL (bool): bool to verify SSL of requests
        chunkSize (int): Number of documents to send in each bulk requests
        threads (int): Number of threads to send each chunk of documents
        url (str): Default to join the url path with api path
    """

    def __init__(self, data: Union[List[dict], Tuple[dict], Set[dict]],
                 baseurl: Optional[str] = 'https://127.0.0.1',
                 api: Optional[str] = '/avantapi/avantData/index/bulk/general/upsert',
                 cluster: Optional[str] = 'AvantData',
                 verifySSL: Optional[bool] = False,
                 chunkSize: Optional[int] = 1000,
                 threads: Optional[int] = 1,
                 **kwargs: Any):
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
        self.sendToIndex(data)

    def uploadToIndex(self, chunk: Union[list, tuple, set]):
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

    def sendToIndex(self, listToIndex: Union[list, tuple, set]):
        if listToIndex:
            self.log.info('Total: {}'.format(len(listToIndex)))
            chunks = [listToIndex]
            if len(listToIndex) > self.chunkSize:
                chunks = [listToIndex[x:x+self.chunkSize]
                            for x in range(0, len(listToIndex), self.chunkSize)]
            if self.threads > 1:
                with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
                    executor.map(self.uploadToIndex, chunks)
            else:
                for chunk in chunks:
                    self.uploadToIndex(chunk)
            if self.errors:
                self.failed += sum(self.errors.values())
                for k, v in self.errors.items():
                    self.log.warning('{} failed. Reason: {}'.format(v, k))
            self.log.info('{} successfully executed with {} failures'.format(
                self.updated+self.created, self.failed))
        else:
            self.log.info('Empty list')
