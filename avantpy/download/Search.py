from urllib3.exceptions import InsecureRequestWarning
import requests
import logging
import json
from typing import Optional, Any


class Search:
    """Search
    A class to manage downloads from avantdata
    Args:
        url (str): AvantData URL
        index (str, optional): Index where the documents are
        must (str, optional): Must query_string from elasticsearch
        mustNot (str, optional): = Must_not query_string from elasticsearch
        filter (str, optional): Filter range query from elasticsearch
        sort (str, optional): Attribute to sort the search
        apiCustom (str, optional): Endpoint where the connection with custom search is set
        apiScroll (str, optional): Endpoint where the connection with scroll search is set
        cluster (str, optional): Header parameter for communication with the api
        verifySSL (bool, optional): Bool to verify SSL of requests
        size (int, optional): Number of documents to be searched (max 5000)
        maxSize (int, optional): Number of documents to start scroll search
        seedTime (str, optional): Period to retain the search context for scrolling,
    Attributes:
        data (list(dict)): Downloaded documents as a list of dictionaries
        url (str): AvantData URL
        index (str): Index where the documents are
        must (str): Must query_string from elasticsearch
        mustNot (str): = Must_not query_string from elasticsearch
        filter (str): Filter range query from elasticsearch
        sort (str): Attribute to sort the search
        log (logger): Logger with __name__
        apiCustom (str): Endpoint where the connection with custom search is set
        apiScroll (str): Endpoint where the connection with scroll search is set
        cluster (str): Header parameter for communication with the api
        verifySSL (bool): Bool to verify SSL of requests
        size (int): Number of documents to be searched (max 5000)
        maxSize (int): Number of documents to start scroll search
        seedTime (str): Period to retain the search context for scrolling,
        took (int): Time elasticsearch took to process the query on its side
    Examples:
        >>> import logging
        >>> logging.basicConfig(level=logging.INFO)
        >>> import avantpy
        >>> s = avantpy.download.Search('https://prod.avantdata.com.br', index='avantscan_results')
        INFO:avantpy.download.Search:Searching avantscan_results in https://prod.avantdata.com.br
        INFO:avantpy.download.Search:Total of 44639 documents found
        INFO:avantpy.download.Search:Over 5000 found. Starting scroll search
        INFO:avantpy.download.Search:5000/44639 downloaded documents
        INFO:avantpy.download.Search:10000/44639 downloaded documents
        INFO:avantpy.download.Search:15000/44639 downloaded documents
        INFO:avantpy.download.Search:20000/44639 downloaded documents
        INFO:avantpy.download.Search:25000/44639 downloaded documents
        INFO:avantpy.download.Search:30000/44639 downloaded documents
        INFO:avantpy.download.Search:35000/44639 downloaded documents
        INFO:avantpy.download.Search:40000/44639 downloaded documents
        INFO:avantpy.download.Search:44639 downloaded documents
        >>> len(s.data)
        44639
        >>> [type(d) for d in s.data[:5]]
        [<class 'dict'>, <class 'dict'>, <class 'dict'>, <class 'dict'>, <class 'dict'>]
    """

    def __init__(self,
                 url: str,
                 index: Optional[str] = '*',
                 must: Optional[str] = 'GenerateTime:*',
                 mustNot: Optional[str] = 'GenerateTime:0',
                 filter: Optional[dict] = {'GenerateTime': {'lte': 'now'}},
                 sort: Optional[str] = 'GenerateTime',
                 apiCustom: Optional[str] = '/avantapi/avantData/search/customSearch',
                 apiScroll: Optional[str] = '/avantapi/avantData/search/scrollSearch',
                 cluster: Optional[str] = 'AvantData',
                 verifySSL: Optional[bool] = False,
                 size: Optional[int] = 5000,
                 maxSize: Optional[int] = 5000,
                 seedTime: Optional[str] = '8m',
                 aggs: Optional[dict] = {},
                  **kwargs: Any):
        self.log = logging.getLogger(__name__)
        self.url = url
        self.index = index
        self.must = must
        self.mustNot = mustNot
        self.filter = filter
        self.sort = sort
        self.apiCustom = apiCustom
        self.apiScroll = apiScroll
        self.cluster = cluster
        self.verifySSL = verifySSL
        self.size = size
        self.maxSize = maxSize
        self.seedTime = seedTime
        self.aggs = aggs
        self.query = kwargs.get('query', self.makeQuery())
        self.data = []
        self.took = 0
        requests.packages.urllib3.disable_warnings(
            category=InsecureRequestWarning)
        self.search()
        self.raw = self.data.copy()
        self.data = self.formatData()
        self.log.info('{} downloaded documents'.format(len(self.data)))

    def __repr__(self):
        return '<{} dictionaries downloaded in data attribute>'.format(len(self.data))

    def makeQuery(self):
        """Return the GET /_search object to search in elasticsearch"""
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
                                    'query': self.must
                                }
                            }
                        ],
                        'must_not': [
                            {
                                'query_string': {
                                    'query': self.mustNot
                                }
                            }
                        ],
                        'filter': {
                            'range': self.filter
                        }
                    }
                },
                'sort': [
                    {
                        self.sort: {
                            'order': 'desc'
                        }
                    }
                ]
            }
        }
        if self.aggs:
            searchQuery['body']['size'] = 0
            searchQuery['body']['aggs'] = self.aggs
        return searchQuery

    def search(self):
        """Performs the first search request and checks the need for scroll search"""
        self.log.info('Searching {} in {}'.format(self.index, self.url))
        try:
            self.response = requests.post(self.url+self.apiCustom,
                                          headers={'cluster': self.cluster},
                                          data=json.dumps(self.query),
                                          verify=self.verifySSL)
            if self.response.status_code < 400 and isinstance(self.response.json(), dict) and not self.aggs:
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
            elif self.aggs and isinstance(self.response.json(), dict):
                if type(self.response.json().get('took')) is int:
                    self.took += self.response.json().get('took')
                self.data.append(self.response.json().get('aggregations'))
        except Exception:
            self.log.error('Failed to search {} in {}'.format(
                self.index, self.url), exc_info=True)

    def scrollSearch(self):
        """Make the scroll search loop"""
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
            self.log.warning('Failed to scroll search {} in {}'.format(
                self.index, self.url))
            self.log.error(e)

    def formatData(self):
        """Transforms elasticsearch return data to a list of dictionaries"""
        newData = []
        if self.aggs:
            newData = self.data
        else:
            for d in self.data:
                newDict = dict()
                newDict['id'] = d['_id']
                newDict['type'] = d['_type']
                newDict['index'] = d['_index']
                newDict.update({k: v for k, v in d['_source'].items()})
                newData.append(newDict)
        return newData