import urllib.request
import logging
import csv


class CSV():

    def __init__(self, request, **kwargs):
        self.log = logging.getLogger(__name__)
        self.request = request
        self.decode = kwargs.get('decode', 'utf-8')
        self.start = kwargs.get('start')
        self.end = kwargs.get('end')
        self.response = kwargs.get('response')
        self.data = []
        self.readCSV()

    def __repr__(self):
        return '<{} dictionaries downloaded in data attribute>'.format(len(self.data))

    def readCSV(self):
        try:
            self.log.info('Reading '+self.request)
            self.response = urllib.request.urlopen(self.request)
            self.data = [i for i in csv.DictReader(
                [line.decode(self.decode, errors='ignore') for line in self.response][self.start:self.end])]
        except Exception as e:
            self.log.warning('Failed to read '+self.request)
            self.log.error(e)