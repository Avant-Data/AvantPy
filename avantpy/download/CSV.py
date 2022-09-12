# -*- coding: utf-8 -*-
import urllib.request
import logging
import csv


class CSV():

    def __init__(self, url, **kwargs):
        self.log = logging.getLogger(__name__)
        self.url = url
        self.decode = kwargs.get('decode', 'utf-8')
        self.start = kwargs.get('start')
        self.end = kwargs.get('end')
        self.response = kwargs.get('response')
        self.data = []
        self.readCSV()

    def readCSV(self):
        try:
            self.log.info('Reading '+self.url)
            self.response = urllib.request.urlopen(self.url)
            self.data = [i for i in csv.DictReader(
                [line.decode(self.decode, errors='ignore') for line in self.response][self.start:self.end])]
        except Exception as e:
            self.log.info('Failed to read '+self.url)
            self.log.debug(e)