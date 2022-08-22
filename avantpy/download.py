# -*- coding: utf-8 -*-


class CSV():

    def __init__(self, url, **kwargs):
        import urllib.request
        import logging
        import csv
        self.log = logging.getLogger(__name__)
        self.url = url
        self.decode = kwargs.get('decode', 'utf-8')
        self.start = kwargs.get('start')
        self.end = kwargs.get('end')
        try:
            self.log.info('Reading '+self.url)
            response = urllib.request.urlopen(self.url)
            self.list = [i for i in csv.DictReader(
                [line.decode(self.decode, errors='ignore') for line in response][self.start:self.end])]
        except Exception as e:
            self.log.info('Failed to read '+self.url)
            self.log.debug(e)