# -*- coding: utf-8 -*-
# https://dzone.com/articles/23-useful-elasticsearch-example-queries

from urllib3.exceptions import InsecureRequestWarning
import requests
import logging
import json
from ..utils import *


class Search():

    def __init__(self, url, **kwargs):
        self.log = logging.getLogger(__name__)
        self.url = url
        self.index = kwargs.get('index', '*')
        self.apiCustom = kwargs.get(
            'apiCustom', '/avantapi/avantData/search/customSearch')
        self.apiScroll = kwargs.get(
            'apiScroll', '/avantapi/avantData/search/scrollSearch')
        self.cluster = kwargs.get('cluster', 'AvantData')
        self.verifySSL = kwargs.get('veryfiSSL', False)
        self.size = kwargs.get('size', 5000)
        self.maxSize = kwargs.get('maxSize', 5000)
        self.seedTime = kwargs.get('seedTime', '8m')
        self.format = kwargs.get('format', False)
        self.query = self.makeQuery(**kwargs)
        self.data = []
        self.took = 0
        requests.packages.urllib3.disable_warnings(
            category=InsecureRequestWarning)
        self.search()
        self.log.info('{} downloaded documents'.format(len(self.data)))
        if self.format:
            self.data = self.formatData()

    def makeQuery(self, **kwargs):
        searchQuery = {
            'index': self.index,
            'scroll': self.seedTime,
            'body': {
                'size': self.size,
                'query': {
                    'bool': {
                        'must': [
                            {
                                'query_string': {
                                    'query': kwargs.get('must', 'GenerateTime:*')
                                }
                            }
                        ],
                        'must_not': [
                            {
                                'query_string': {
                                    'query': kwargs.get('mustNot', 'GenerateTime:0')
                                }
                            }
                        ],
                        'filter': {
                            'range': kwargs.get('filter', {'GenerateTime': {'lte': 'now'}})
                        }
                    }
                },
                'sort': [
                    {
                        kwargs.get('sort', 'GenerateTime'): {
                            'order': 'desc'
                        }
                    }
                ]
            }
        }
        return searchQuery

    def search(self):
        self.log.info('Searching {} in {}'.format(self.index, self.url))
        try:
            self.response = requests.post(self.url+self.apiCustom,
                                          headers={'cluster': self.cluster},
                                          data=json.dumps(self.query),
                                          verify=self.verifySSL)
            if self.response.status_code < 400:
                self.scrollID = self.response.json().get('_scroll_id')
                self.total = self.response.json().get('hits').get('total')
                self.log.info('Total of {} documents found'.format(self.total))
                if type(self.response.json().get('took')) is int:
                    self.took += self.response.json().get('took')
                self.data.extend(self.response.json().get('hits').get('hits'))
                if self.total > self.maxSize and self.size >= self.maxSize:
                    self.scrollQuery = {
                        'scroll': self.seedTime,
                        'scroll_id': self.scrollID
                    }
                    self.log.info(
                        'Over {} found. Starting scroll search'.format(self.maxSize))
                    self.scrollSearch()
        except Exception as e:
            self.log.info('Failed to search {} in {}'.format(
                self.index, self.url))
            self.log.debug(e)

    def scrollSearch(self):
        self.log.info(
            '{}/{} downloaded documents'.format(len(self.data), self.total))
        try:
            self.response = requests.post(self.url+self.apiScroll,
                                        headers={'cluster': self.cluster},
                                        data=json.dumps(self.scrollQuery),
                                        verify=self.verifySSL)
            if self.response.status_code < 400:
                if type(self.response.json().get('took')) is int:
                    self.took += self.response.json().get('took')
                self.data.extend(self.response.json().get('hits').get('hits'))
                if len(self.response.json().get('hits').get('hits')) >= self.maxSize:
                    self.scrollSearch()
            elif self.response.status_code == 504:
                self.log.debug(self.response)
                self.scrollSearch()
        except Exception as e:
            self.log.info('Failed to scroll search {} in {}'.format(
                self.index, self.url))
            self.log.debug(e)
    
    def formatData(self):
        newData = []
        for d in self.data:
            newDict = dict()
            newDict['id'] = d['_id']
            newDict['type'] = d['_type']
            newDict['index'] = d['_index']
            newDict.update({k:v for k,v in d['_source'].items()})
            newData.append(newDict)
        return newData