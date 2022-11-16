from ..utils import *
import requests
import logging
from typing import Optional, Union, List, Tuple, Set, Type

class JSON:
    """JSON Downloader

    A class to download JSON as a list of dictionaries

    Args:
        request (str or list(str)): URLs containing JSON objects to be downloaded
        select (str or list(str), optional): Select only specified keys to download
        headers (dict, optional): Headers to be sent in the request

    Attributes:
        data (list(dict)): Downloaded JSONs as a list of dictionaries
        responseStatus (list(int)): List containing the response status of all requests
        request (str or list(str)): URLs containing JSON objects to be downloaded
        select (str or list(str)): Select only specified keys to download
        headers (dict): headers to be sent in the request
        log (logger): Logger with __name__

    Examples:
        >>> import avantpy
        >>> import logging
        >>> logging.basicConfig(level=logging.INFO)
        >>> avantpy.download.JSON('https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json', select='vulnerabilities')
        INFO:avantpy.download.JSON:Reading https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
        INFO:avantpy.download.JSON:<Response [200]> with 706KB. 832 dictionaries added to data attribute
        <832 dictionaries downloaded in data attribute>
    """

    def __init__(self,
                 request: Union[str, Type[requests.Request], List[Union[str, Type[requests.Request]]], Tuple[Union[str, Type[requests.Request]]], Set[Union[str, Type[requests.Request]]]],
                 select: Optional[Union[str, List[str],
                                        Tuple[str], Set[str]]] = None,
                 headers: dict = {
                     "Accept": "application/json, text/javascript, */*; q=0.01",
                     "Accept-Encoding": "deflate, gzip, br",
                     "Accept-Language": "en-US",
                     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
                     "X-Requested-With": "XMLHttpRequest",
                 },
                 **kwargs):
        self.log = logging.getLogger(__name__)
        self.request = request if isinstance(
            request, (list, tuple, set)) else [request]
        self.select = select if isinstance(
            select, (list, tuple, set)) else [select]
        self.headers = headers
        self.responseStatus = []
        self.data = []
        self.bulkRead()

    def __repr__(self):
        return '<{} dictionaries downloaded in data attribute>'.format(len(self.data))

    def readJSON(self, url: str = None, response: Type[requests.Request] = None):
        try:
            if url:
                self.log.info('Reading {}'.format(url))
                response = requests.get(url, headers=self.headers)
            self.responseStatus.append(response.status_code)
            responseJson = response.json()
            data = getData(responseJson, *self.select)
            if not isinstance(data, (list, tuple, set)):
                data = [data]
            self.data.extend(data)
            self.log.info('{} with {}. {} dictionaries added to data attribute'.format(response, humanSize(len(response.content)), len(data)))
        except Exception as e:
            self.log.warning('Failed to read {}'.format(url))
            self.log.error(e)

    def bulkRead(self):
        for request in self.request:
            if type(request) is str:
                self.readJSON(url = request)
            else:
                self.readJSON(response = request)