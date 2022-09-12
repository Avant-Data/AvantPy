import requests
import logging
from ..utils import *

class JSON():

    def __init__(self, url, **kwargs):
        self.log = logging.getLogger(__name__)
        self.url = url
        self.destObj = kwargs.get('obj') if isinstance(kwargs.get('obj'), (list, tuple, set)) else [kwargs.get('obj')]
        self.headers = kwargs.get('headers', {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "deflate, gzip, br",
                "Accept-Language": "en-US",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
                "X-Requested-With": "XMLHttpRequest",
            })
        self.response = kwargs.get('reponse')
        self.data = []
        self.readJSON()

    def readJSON(self):
        try:
            self.log.info('Reading {}'.format(self.url))
            if not self.response:
                self.response = requests.get(self.url, headers=self.headers)
            self.data = getObj(self.response.json(), *self.destObj)
        except Exception as e:
            self.log.info('Failed to read {}'.format(self.url))
            self.log.debug(e)