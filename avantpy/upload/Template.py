import requests
import logging
import json
import re
from typing import Optional, Union, List, Tuple, Set, Any
from urllib3.exceptions import InsecureRequestWarning


class Template():
    """Template

    A class to manage creation of templates

    Args:
        name (str): Name of the template
        template (list(dict) or dict): Dictionary or dictionaries with keys to generate a template
        baseurl (str, optional): Baseurl to execute the upsert bulk 
        api (str, optional): Endpoint where the connection with database is set
        cluster (str, optional): Header parameter for communication with the api
        verifySSL (bool, optional): Bool to verify SSL of requests
        order (int, optional): Order attribute of the template
        shards (int, optional): Shards attribute of the template
        typeMap (dict, optional): Attributes to not be considered as text
        aliases (str, optional): Aliases attribute of the template
        mappingName (str, optional): Mappings attribute of the template
        templateName (str, optional): Template attribute of the template body
        regenerate (bool, optional): Always create template if True


    Attributes:
        name (str): Name of the template
        template (list(dict) or dict): Dictionary or dictionaries with keys to generate a template
        baseurl (str): Baseurl to execute the upsert bulk 
        api (str): Endpoint where the connection with database is set
        cluster (str): Header parameter for communication with the api
        verifySSL (bool): Bool to verify SSL of requests
        order (int): Order attribute of the template
        shards (int): Shards attribute of the template
        typeMap (dict): Attributes to not be considered as text
        aliases (str): Aliases attribute of the template
        mappingName (str): Mappings attribute of the template
        templateName (str): Template attribute of the template body
        regenerate (bool): Always create template if True
        data(dict): The generated template

    Examples:
        >>> import logging
        >>> logging.basicConfig(level=logging.INFO)
        >>> import avantpy
        >>> dataList = []
        >>> dataList.append({'id':'6fee099da7dfbb67599d7fa7389de898', 'type':'test', 'index':'test', 'testKey': 'firstValue'})
        >>> dataList.append({'id':'58f77dcc14a41b2984e298e86db85c73', 'type':'test', 'index':'test', 'testKey': 'secondValue'})
        >>> dataList.append({'id':'ed23fa12819a63198b5c0b171ebbbf2d', 'type':'test', 'index':'test', 'testKey': 'thirdValue'})
        >>> avantpy.upload.UpsertBulk(dataList, baseurl='https://192.168.102.133/')
        INFO:avantpy.upload.UpsertBulk:Total: 3
        INFO:avantpy.upload.UpsertBulk:Updated: 0, Created 3. 
        INFO:avantpy.upload.UpsertBulk:3 successfully executed with 0 failures
        <Created: 3 / Updated: 0 / Failed: 0>
    """

    def __init__(self,
                 name: str,
                 template: Union[List[dict], Tuple[dict], Set[dict], dict],
                 baseurl: Optional[str] = 'https://127.0.0.1',
                 api: Optional[str] = '/avantapi/avantData/template',
                 apiCreate: Optional[str] = '/avantapi/avantData/template/create',
                 cluster: Optional[str] = 'AvantData',
                 verifySSL: Optional[str] = False,
                 order: Optional[int] = 1,
                 shards: Optional[int] = 2,
                 typeMap: Optional[dict] = {},
                 regenerate: Optional[bool] = False,
                 **kwargs):
        self.log = logging.getLogger(__name__)
        self.name = name
        self.template = template
        self.baseurl = baseurl
        self.api = api
        self.apiCreate = apiCreate
        self.cluster = cluster
        self.verifySSL = verifySSL
        self.templateName = kwargs.get('templateName', self.name+'*')
        self.mappingName = kwargs.get('mappingName', self.name)
        self.aliases = kwargs.get('aliases', re.sub(
            r'[^a-zA-Z0-9].*', '', self.name.title()))
        self.order = order
        self.shards = shards
        self.typeMap = typeMap
        self.regenerate = regenerate
        requests.packages.urllib3.disable_warnings(
            category=InsecureRequestWarning)
        self.data = self.formatTemplate()

    def __repr__(self):
        return 'Generated template:\n{}'.format(json.dumps(self.data, indent=4))

    def propertiesMap(self, key):
        valuesMap = {
            "date": {
                "type": "date",
                "format": "yyyy/MM/dd HH:mm:ss||epoch_millis"
            },
            "int": {
                "type": "integer"
            },
        }
        if valuesMap.get(key):
            return valuesMap[key]
        return {"type": key}

    def generateProperties(self, template, gtime=True):
        newDict = dict()
        if isinstance(template, (list, tuple, set)):
            allKeys = {k for d in template for k in d.keys()}
            templateDict = dict()
            for key in allKeys:
                for di in template:
                    if di.get(key):
                        templateDict[key] = di.get(key)
                    break
        elif isinstance(template, dict):
            templateDict = template
        for k,v in templateDict.items():
            if k in self.typeMap.keys():
                newDict[k] = self.propertiesMap(self.typeMap[k])
            elif isinstance(v, dict):
                newDict[k] = {"properties": self.generateProperties(v, gtime=False)}
            elif isinstance(v, (list, tuple, set)):
                newDict[k] = {"type": "object"}
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
        if not newDict.get('GenerateTime') and gtime:
            newDict["GenerateTime"] = {
                "type": "date",
                "format": "yyyy/MM/dd HH:mm:ss||epoch_millis"
            }
        return newDict

    def formatTemplate(self):
        if isinstance(self.template, (list, tuple, set, dict)):
            properties = self.generateProperties(self.template)
        else:
            raise ValueError('Template needs to be a dict, list, tuple or set')
        formattedTemplate = {
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
                        "number_of_shards": self.shards,
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
                        "properties": properties
                    }
                },
                "aliases": {
                    self.aliases: {}
                }
            }
        }
        return formattedTemplate

    def upload(self):
        if self.data:
            headers = {
                'cluster': self.cluster
            }
            response = requests.get(url=self.baseurl+self.api+'/'+self.name,
                                    headers=headers,
                                    verify=self.verifySSL
                                    )
            print(self.regenerate)
            if response.status_code == 404 or self.regenerate:
                self.log.info(
                    'Template not found. Installing template {}'.format(self.name))
                responseCreate = requests.post(url=self.baseurl+self.apiCreate,
                                               headers=headers,
                                               data=json.dumps(self.data),
                                               verify=self.verifySSL)
                self.log.info(responseCreate.text)
            else:
                print(json.dumps(self.data))
                print(response.text)
                print('################')
                print(json.dumps(json.loads(response.text), indent=4))
                self.log.info('Template {} already exists'.format(self.name))
