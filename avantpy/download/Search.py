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
        self.apiCustom = kwargs.get('apiCustom', '/avantapi/avantData/search/customSearch')
        self.apiScroll = kwargs.get('apiScroll', '/avantapi/avantData/search/scrollSearch')
        self.cluster = kwargs.get('cluster', 'AvantData')
        self.verifySSL = kwargs.get('veryfiSSL', False)
        self.size = kwargs.get('size', 5000)
        self.seedTime = kwargs.get('seedTime', '8m')
        self.query = self.makeQuery(**kwargs)
        self.data = []
        requests.packages.urllib3.disable_warnings(
            category=InsecureRequestWarning)
        self.search()

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
        try:
            self.log.info('Searching {} in {}'.format(self.index, self.url))
            self.response = requests.post(self.url+self.apiCustom, headers={'cluster': self.cluster},data=json.dumps(self.query), verify=self.verifySSL)
            if self.response.status_code < 400:
                self.data.append(self.response.json().keys())
                print(self.response.json()['took'])
        except Exception as e:
            self.log.info('Failed to search {} in {}'.format(self.index, self.url))
            self.log.debug(e)