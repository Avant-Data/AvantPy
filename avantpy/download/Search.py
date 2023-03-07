from urllib3.exceptions import InsecureRequestWarning
import socket
import requests
import logging
import json
from typing import Optional, Any, List, Dict

class Search:
    """Search
    A class to manage downloads from avantdata
    Args:
        url (str, optional): AvantData URL
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
        max_size (int, optional): Number of documents to start scroll search
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
        max_size (int): Number of documents to start scroll search
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
                 url: Optional[str] = '',
                 index: Optional[str] = '*',
                 must: Optional[str] = 'GenerateTime:*',
                 mustNot: Optional[str] = 'GenerateTime:0',
                 filter: Optional[dict] = {'GenerateTime': {'lte': 'now'}},
                 sort: Optional[str] = 'GenerateTime',
                 apiCustom: Optional[str] = '/avantapi/avantData/search/customSearch',
                 apiScroll: Optional[str] = '/avantapi/avantData/search/scrollSearch',
                 api_memory: Optional[str] = '/avantapi/2.0/avantData/avantMem/search',
                 cluster: Optional[str] = 'AvantData',
                 verifySSL: Optional[bool] = False,
                 size: Optional[int] = 5000,
                 max_size: Optional[int] = 9999999999,
                 seedTime: Optional[str] = '8m',
                 memory: Optional[bool] = False,
                 aggs: Optional[dict] = {},
                 **kwargs: Any):
        self.log = logging.getLogger(__name__)
        self.url = self.get_url(url)
        self.index = index
        self.must = must
        self.mustNot = mustNot
        self.memory = memory
        self.filter = filter
        self.sort = sort
        self.apiCustom = apiCustom
        self.apiScroll = apiScroll
        self.api_memory = api_memory
        self.cluster = cluster
        self.verifySSL = verifySSL
        self.size = size
        self.max_size = max_size
        self.seedTime = seedTime
        self.aggs = aggs
        self.key = kwargs.get('key', self.index)
        self.query = kwargs.get('query', self.makeQuery())
        self.data = []
        self.took = 0
        requests.packages.urllib3.disable_warnings(
            category=InsecureRequestWarning)
        if self.memory:
            self.memory_search()
            self.raw = self.data
        else:
            self.search()
            self.raw = self.data.copy()
            self.data = self.formatData()
        self.log.info('{} downloaded documents'.format(len(self.data)))

    def __repr__(self):
        return '<{} dictionaries downloaded in data attribute>'.format(len(self.data))

    def makeQuery(self):
        """Returns the GET /_search object for searching in Elasticsearch."""
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
        """ Searches for documents in Elasticsearch using the given query."""
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
                if min(self.total, self.max_size) > self.size:
                    self.scrollQuery = {
                        'scroll': self.seedTime,
                        'scroll_id': self.scrollID
                    }
                    self.log.info(
                        'Over {} found. Starting scroll search'.format(self.size))
                    self.scrollSearch()
            elif self.aggs and isinstance(self.response.json(), dict):
                if type(self.response.json().get('took')) is int:
                    self.took += self.response.json().get('took')
                self.data.append(self.response.json().get('aggregations'))
        except Exception:
            self.log.error('Failed to search {} in {}'.format(
                self.index, self.url), exc_info=True)

    def scrollSearch(self):
        """Make the scroll search loop.

        Continuously retrieves the next batch of search results from Elasticsearch using the scroll API
        until all results have been retrieved.

        Raises:
            Warning: If the search fails.
        """
        self.log.info(
            '{}/{} downloaded documents'.format(len(self.data), min(self.total, self.max_size)))
        try:
            self.response = requests.post(self.url+self.apiScroll,
                                          headers={'cluster': self.cluster},
                                          data=json.dumps(self.scrollQuery),
                                          verify=self.verifySSL)
            if self.response.status_code < 400:
                if type(self.response.json().get('took')) is int:
                    self.took += self.response.json().get('took')
                self.data.extend(self.response.json().get('hits').get('hits'))
                if min(self.total, self.max_size) > len(self.data):
                    self.scrollSearch()
        except Exception as e:
            self.log.warning('Failed to scroll search {} in {}'.format(
                self.index, self.url))
            self.log.error(e)

    def formatData(self) -> List[Dict[str, Any]]:
        """Transforms elasticsearch return data to a list of dictionaries

        Returns:
            List of dictionaries containing fields 'id', 'type', 'index' and any fields present in the '_source' field of each hit.
        """
        newData = []
        if self.aggs:
            newData = self.data
        else:
            for d in self.data:
                newData.append({
                    'id': d['_id'],
                    'type': d['_type'],
                    'index': d['_index'],
                    **{k: v for k, v in d['_source'].items()}
                })
        return newData

    def memory_search(self) -> List[Any]:
        payload = {
            'key': self.key
        }
        try:
            response = requests.post(self.url+self.api_memory, data=json.dumps(payload), verify=self.verifySSL)
            self.log.debug(response.text)
            if response.ok:
                value = eval(response.json())
                if isinstance(value, list):
                    self.data.extend(value)
                elif isinstance(value, str):
                    self.data.append(value)
            else:
                self.log.warning('Response error. Status code: {}'.format(response.status_code))
        except Exception:
            self.log.error('Error searching in memory.')

    def get_url(self, url: str) -> str:
        """This function returns a URL string.
        
        If the `url` argument is not empty, the function simply returns it.
        
        If the `url` argument is empty, the function creates a UDP socket and connects to the IP address and port
        of Google's public DNS server (8.8.8.8 on port 80) to get the IP address of the host. It then formats the IP
        address as a string and returns it with the `https://` protocol prefix.
        
        Args:
            url: string representing the URL that the function will try to retrieve.
        
        Returns:
            str: The URL to use for API requests.
        """
        if not url:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            host_ip = s.getsockname()[0]
            s.close()
            return 'https://{}'.format(host_ip)
        return url
