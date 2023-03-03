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
        custom (dict, optional): Attributes to not be considered as text
        aliases (str, optional): Aliases attribute of the template
        mappingName (str, optional): Mappings attribute of the template
        templateName (str, optional): Template attribute of the template body
        regenerate (bool, optional): Always create template if True
        append (bool, optional): Append missing keys in the template if True


    Attributes:
        name (str): Name of the template
        template (list(dict) or dict): Dictionary or dictionaries with keys to generate a template
        baseurl (str): Baseurl to execute the upsert bulk 
        api (str): Endpoint where the connection with database is set
        cluster (str): Header parameter for communication with the api
        verifySSL (bool): Bool to verify SSL of requests
        order (int): Order attribute of the template
        shards (int): Shards attribute of the template
        custom (dict): Attributes to not be considered as text
        aliases (str): Aliases attribute of the template
        mappingName (str): Mappings attribute of the template
        templateName (str): Template attribute of the template body
        regenerate (bool): Always create template if True
        append (bool): Append missing keys in the template if True
        data(dict): The generated template

    Example:
        >>> import logging
        >>> logging.basicConfig(level=logging.INFO)
        >>> import avantpy
        >>> dataList = []
        >>> dataList.append({'testing1':'test', 'testing2':'test', 'testing3':'test'})
        >>> dataList.append({'testing4':'test', 'testing5':'test', 'testing6':'test'})
        >>> template = avantpy.upload.Template(template=dataList, name='testing_template', aliases='TestingTemplate', baseurl='https://192.168.102.133/')
        >>> template.upload()
        INFO:avantpy.upload.Template:Uploading template testing_template
        INFO:avantpy.upload.Template:{"acknowledged":true}
        >>> template.data.get('body').keys()
        dict_keys(['template', 'settings', 'mappings', 'aliases'])
        >>> template.data.get('body').get('mappings').get('testing_template').get('properties').keys()
        dict_keys(['testing1', 'testing3', 'testing6', 'testing2', 'testing4', 'testing5', 'GenerateTime'])
        >>> dataList.append({'testing7':'test', 'testing8':'test', 'testing9':'test'})
        >>> template.upload()
        INFO:avantpy.upload.Template:Template testing_template already exists
        >>> template.upload(append=True)
        INFO:avantpy.upload.Template:Appending keys ['testing7', 'testing8', 'testing9']
        INFO:avantpy.upload.Template:{"acknowledged":true}
        >>> template.data.get('body').get('mappings').get('testing_template').get('properties').keys()
        dict_keys(['testing7', 'testing1', 'testing9', 'testing8', 'testing3', 'testing6', 'testing2', 'testing4', 'testing5', 'GenerateTime']) 
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
                 custom: Optional[dict] = {},
                 regenerate: Optional[bool] = False,
                 append: Optional[bool] = False,
                 **kwargs: Any):
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
            r'[^a-zA-Z0-9_]*', '', self.name.title()))
        self.order = order
        self.shards = shards
        self.custom = custom
        self.regenerate = regenerate
        self.append = append
        requests.packages.urllib3.disable_warnings(
            category=InsecureRequestWarning)
        self.data = self.formatTemplate()

    def __repr__(self):
        return 'Generated template:\n{}'.format(json.dumps(self.data, indent=4))

    def propertiesMap(self, value: Union[dict, str]) -> dict:
        """Maps the provided value to a dictionary representing its properties.

        Args:
            value (Union[dict, str]): The value to map. Can be either a dictionary or a string.

        Returns:
            dict: A dictionary representing the properties of the provided value.

        Example:
            >>> propertiesMap('int')
            {'type': 'integer'}
        """
        if isinstance(value, dict):
            return value
        valuesMap = {
            "date": {
                "type": "date",
                "format": "yyyy/MM/dd HH:mm:ss||epoch_millis"
            },
            "int": {
                "type": "integer"
            },
        }
        if valuesMap.get(value):
            return valuesMap[value]
        return {"type": value}

    def getTemplateDict(self, template: Union[List[dict], Tuple[dict], Set[dict], dict]) -> dict:
        """Returns a dictionary containing all keys and values present in the input template.

        Args:
            template: A template dictionary or a list, tuple or set of dictionaries.
        
        Returns:
            A dictionary containing all keys and values present in the input template.
        """
        if isinstance(template, (list, tuple, set)):
            allKeys = {k for d in template for k in d.keys()}
            templateDict = dict()
            for key in allKeys:
                for di in template:
                    if di.get(key):
                        if isinstance(di.get(key), dict):
                            if not templateDict.get(key):
                                templateDict[key] = dict()
                            templateDict[key].update(di.get(key))
                        else:
                            templateDict[key] = di.get(key)
                            break
        elif isinstance(template, dict):
            templateDict = template
        return templateDict

    def generateProperties(self, template, gtime=True):
        """Returns a dictionary containing the properties of the input template.

        Args:
            template: A template dictionary or a list, tuple or set of dictionaries.
            gtime: A boolean flag that indicates whether or not to generate the "GenerateTime" property.
                Default is True.
        
        Returns:
            A dictionary containing the properties of the input template.
        """
        newDict = dict()
        textType = {
            "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    },
            "analyzer": "WS"
        }
        templateDict = self.getTemplateDict(template)
        for k, v in templateDict.items():
            if k in self.custom.keys():
                newDict[k] = self.propertiesMap(self.custom[k])
            elif isinstance(v, dict):
                newDict[k] = {
                    "properties": self.generateProperties(v, gtime=False)}
            elif isinstance(v, (list, tuple, set)):
                if all([isinstance(d, dict) for d in v]):
                    newDict[k] = {"type": "object"}
                else:
                    newDict[k] = textType
            else:
                newDict[k] = textType
        if not newDict.get('GenerateTime') and gtime:
            newDict["GenerateTime"] = {
                "type": "date",
                "format": "yyyy/MM/dd HH:mm:ss||epoch_millis"
            }
        return newDict

    def formatTemplate(self):
        """Generate the complete template"""
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

    def upload(self, **kwargs):
        """Upload the template to AvantData

        Args:
            regenerate (bool): always create a template if True
            append (bool): append missing keys to the current template if True
        """
        regenerate = kwargs.get('regenerate', self.regenerate)
        append = kwargs.get('append', self.append)
        if self.data:
            headers = {
                'cluster': self.cluster
            }
            response = requests.get(url=self.baseurl+self.api+'/'+self.name,
                                    headers=headers,
                                    verify=self.verifySSL
                                    )
            if response.status_code == 404 or regenerate:
                self.log.info('Uploading template {}'.format(self.name))
                responseCreate = requests.post(url=self.baseurl+self.apiCreate,
                                               headers=headers,
                                               data=json.dumps(self.data),
                                               verify=self.verifySSL)
                self.log.info(responseCreate.text)
            elif append:
                rJson = response.json()
                tmps = rJson.get(next(iter(rJson)))
                changed = False
                appendedKeys = []
                for k, v in tmps.get('mappings').items():
                    properties = v.get('properties')
                    newTemplate = self.getTemplateDict(self.template)
                    appendKeys = set(newTemplate.keys())-set(properties.keys())
                    appendedKeys.extend(list(appendKeys))
                    if appendKeys:
                        changed = True
                        appendTemplate = {newK: newTemplate.get(
                            newK) for newK in appendKeys}
                        appendProperties = self.generateProperties(
                            appendTemplate, gtime=False)
                        properties.update(appendProperties)
                        rJson[next(iter(rJson))
                              ]['mappings'][k]['properties'] = properties
                self.data = {
                    "name": self.name,
                    "order": tmps.pop('order'),
                    "body": rJson.get(next(iter(rJson)))
                }
                if changed:
                    self.log.info('Appending keys {}'.format(appendedKeys))
                    responseCreate = requests.post(url=self.baseurl+self.apiCreate,
                                                   headers=headers,
                                                   data=json.dumps(self.data),
                                                   verify=self.verifySSL)
                    self.log.info(responseCreate.text)
                else:
                    self.log.info(
                        'Nothing to append in template {}'.format(self.name))
            else:
                self.log.info('Template {} already exists'.format(self.name))
