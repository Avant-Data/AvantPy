import requests
import logging
import json
import re
from urllib3.exceptions import InsecureRequestWarning


class Template():

    def __init__(self, **kwargs):
        self.log = logging.getLogger(__name__)
        self.name = kwargs.get('name')
        assert self.name
        self.template = kwargs.get('template')
        assert self.template
        self.baseurl = kwargs.get('baseurl', 'https://127.0.0.1')
        self.api = kwargs.get('api', '/avantapi/avantData/template')
        self.apiCreate = kwargs.get('apiCreate', '/create')
        self.cluster = kwargs.get('cluster', 'AvantData')
        self.verifySSL = kwargs.get('verifySSL', False)
        self.url = kwargs.get('url', self.baseurl+self.api)
        self.templateName = kwargs.get('templateName', self.name+'*')
        self.mappingName = kwargs.get('mappingName', self.name)
        self.aliases = kwargs.get('aliases', re.sub(
            r'[^a-zA-Z0-9].*', '', self.name))
        self.order = kwargs.get('order', 1)
        self.typeMap = kwargs.get('typeMap', {})
        requests.packages.urllib3.disable_warnings(
            category=InsecureRequestWarning)
        self.formattedTemplate = dict()
        self.formatTemplate()
        self.uploadTemplate(self.name, self.formattedTemplate)

    def getMaxKeys(self, lst):
        lengths = [len(obj) for obj in lst]
        return lengths.index(max(lengths))

    def propertiesMap(self, key):
        valuesMap = {
            "date": {
                "type": "date",
                "format": "yyyy/MM/dd HH:mm:ss||epoch_millis"
            },
            "long": {
                "type": "long"
            },
            "int": {
                "type": "integer"
            },
            "integer": {
                "type": "integer"
            },
            "ip": {
                "type": "ip"
            },
            "object": {
                "type": "object"
            },
             "float": {
                "type": "float"
            },
        }
        return valuesMap[key]

    def generatedProperties(self, template):
        newDict = dict()
        for k in template[self.getMaxKeys(template)].keys():
            if k in self.typeMap.keys():
                newDict[k] = self.propertiesMap(self.typeMap[k])
            else:
                newDict[k] = {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    },
                    "analyzer": "WS"
                }
        if not newDict.get('GenerateTime'):
            newDict["GenerateTime"] = {
                "type": "date",
                "format": "yyyy/MM/dd HH:mm:ss||epoch_millis"
            }
        return json.loads(json.dumps(newDict))

    def formatTemplate(self):
        if isinstance(self.template, (list, tuple, set)):
            self.log.info('Generating template automatically')
            self.formattedTemplate = {
                "name": self.name,
                "order": self.order,
                "body": {
                    "template": self.templateName,
                    "settings": {
                        "index": {
                            "refresh_interval": "5s",
                            "analysis": {
                                "analyzer": {
                                    "WS": {
                                        "filter": [
                                            "lowercase"
                                        ],
                                        "type": "custom",
                                        "tokenizer": "whitespace"
                                    }
                                }
                            },
                            "number_of_shards": "2",
                            "number_of_replicas": "0"
                        }
                    },
                    "mappings": {
                        self.mappingName: {
                            "_all": {
                                "norms": False,
                                "enabled": True
                            },
                            "_size": {
                                "enabled": True
                            },
                            "properties": self.generatedProperties(self.template)
                        }
                    },
                    "aliases": {
                        self.aliases: {}
                    }
                }
            }

    def uploadTemplate(self, name, template):
        if template:
            headers = {
                'cluster': self.cluster
            }
            response = requests.get(url=self.url+'/'+name,
                                    headers=headers,
                                    verify=self.verifySSL
                                    )
            if response.status_code == 404:
                self.log.info(
                    'Template not found. Installing template '+name)
                responseCreate = requests.post(url=self.url+self.apiCreate,
                                               headers=headers,
                                               data=json.dumps(template),
                                               verify=self.verifySSL)
                self.log.info(responseCreate.text)
            else:
                self.log.info('Template '+name+' already exists')
