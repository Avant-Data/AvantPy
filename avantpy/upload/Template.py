import requests
import logging
import socket
import json
import re
from typing import Optional, Union, List, Tuple, Set, Any
from urllib3.exceptions import InsecureRequestWarning


class Template:
    """Template

    A class to manage creation of templates

    Args:
        name (str): Name of the template
        template (list(dict) or dict): Dictionary or dictionaries with keys to generate a template
        baseurl (str, optional): Baseurl to execute the upsert bulk 
        api (str, optional): Endpoint where the connection with database is set
        cluster (str, optional): Header parameter for communication with the api
        verify_SSL (bool, optional): Bool to verify SSL of requests
        order (int, optional): Order attribute of the template
        shards (int, optional): Shards attribute of the template
        custom (dict, optional): Attributes to not be considered as text
        aliases (str, optional): Aliases attribute of the template
        mapping_name (str, optional): Mappings attribute of the template
        template_name (str, optional): Template attribute of the template body
        regenerate (bool, optional): Always create template if True
        append (bool, optional): Append missing keys in the template if True


    Attributes:
        name (str): Name of the template
        template (list(dict) or dict): Dictionary or dictionaries with keys to generate a template
        baseurl (str): Baseurl to execute the upsert bulk 
        api (str): Endpoint where the connection with database is set
        cluster (str): Header parameter for communication with the api
        verify_SSL (bool): Bool to verify SSL of requests
        order (int): Order attribute of the template
        shards (int): Shards attribute of the template
        custom (dict): Attributes to not be considered as text
        aliases (str): Aliases attribute of the template
        mapping_name (str): Mappings attribute of the template
        template_name (str): Template attribute of the template body
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
                 baseurl: Optional[str] = '',
                 api: Optional[str] = '/avantapi/avantData/template',
                 api_create: Optional[str] = '/avantapi/avantData/template/create',
                 cluster: Optional[str] = 'AvantData',
                 verify_SSL: Optional[str] = False,
                 order: Optional[int] = 1,
                 shards: Optional[int] = 2,
                 custom: Optional[dict] = {},
                 regenerate: Optional[bool] = False,
                 append: Optional[bool] = False,
                 **kwargs: Any):
        self.log = logging.getLogger(__name__)
        self.name = name
        self.template = template
        self.baseurl = self.getUrl(baseurl)
        self.api = api
        self.api_create = api_create
        self.cluster = cluster
        self.verify_SSL = verify_SSL
        self.template_name = kwargs.get('template_name', self.name+'*')
        self.mapping_name = kwargs.get('mapping_name', self.name)
        self.aliases = kwargs.get('aliases', re.sub(
            r'[^a-zA-Z0-9_]*', '', self.name.title()))
        self.order = order
        self.shards = shards
        self.custom = custom
        self.regenerate = regenerate
        self.append = append
        requests.packages.urllib3.disable_warnings(
            category=InsecureRequestWarning)
        self.data = self.format_template()

    def __repr__(self):
        return 'Generated template:\n{}'.format(json.dumps(self.data, indent=4))

    def properties_map(self, value: Union[dict, str]) -> dict:
        """Maps the provided value to a dictionary representing its properties.

        Args:
            value (Union[dict, str]): The value to map. Can be either a dictionary or a string.

        Returns:
            dict: A dictionary representing the properties of the provided value.

        Example:
            >>> properties_map('int')
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

    def get_template_dict(self, template: Union[List[dict], Tuple[dict], Set[dict], dict]) -> dict:
        """Returns a dictionary containing all keys and values present in the input template.

        Args:
            template: A template dictionary or a list, tuple or set of dictionaries.
        
        Returns:
            A dictionary containing all keys and values present in the input template.
        """
        if isinstance(template, (list, tuple, set)):
            allKeys = {k for d in template for k in d.keys()}
            template_dict = dict()
            for key in allKeys:
                for di in template:
                    if di.get(key):
                        if isinstance(di.get(key), dict):
                            if not template_dict.get(key):
                                template_dict[key] = dict()
                            template_dict[key].update(di.get(key))
                        else:
                            template_dict[key] = di.get(key)
                            break
        elif isinstance(template, dict):
            template_dict = template
        return template_dict

    def generate_properties(self, template, gtime=True):
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
        template_dict = self.get_template_dict(template)
        for k, v in template_dict.items():
            if k in self.custom.keys():
                newDict[k] = self.properties_map(self.custom[k])
            elif isinstance(v, dict):
                newDict[k] = {
                    "properties": self.generate_properties(v, gtime=False)}
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

    def format_template(self):
        """Generate the complete template"""
        if isinstance(self.template, (list, tuple, set, dict)):
            properties = self.generate_properties(self.template)
        else:
            raise ValueError('Template needs to be a dict, list, tuple or set')
        formattedTemplate = {
            "name": self.name,
            "order": self.order,
            "body": {
                "template": self.template_name,
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
                    self.mapping_name: {
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

    def flatten_dict(self, d):
        flattened = {}
        for k, v in d.items():
            if isinstance(v, dict):
                if 'type' in v:
                    flattened[k] = v['type']
                elif 'properties' in v:
                    flattened[k] = self.flatten_dict(v['properties'])
            else:
                flattened[k] = v
        return flattened

    
    def compare_dictionaries(self, dict1, dict2):
        diff = {}
        keys_added = set(dict2.keys()) - set(dict1.keys())
        for key in keys_added:
            diff[key] = dict2[key]
        common_keys = set(dict1.keys()) & set(dict2.keys())
        for key in common_keys:
            if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                nested_diff = self.compare_dictionaries(dict1[key], dict2[key])
                if nested_diff:
                    diff[key] = nested_diff
            elif dict1[key] != dict2[key]:
                diff[key] = dict2[key]
        return diff

    def pop_specific_values(self, dictionary, specific):
        keys_to_pop = []
        for key, value in dictionary.items():
            if value == specific:
                keys_to_pop.append(key)
        return keys_to_pop
    
    def remove_keys(self, dictionary, keys_to_pop):
        if not isinstance(dictionary, dict):
            return dictionary
        for key in keys_to_pop:
            if key in dictionary:
                dictionary.pop(key)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                dictionary[key] = self.remove_keys(value, keys_to_pop)
        return dictionary

    def upload(self, **kwargs):
        """Upload a new Elasticsearch template or append to an existing one.

        Args:
            regenerate (bool, optional): If True, the existing template will be deleted and a new one with the same name will be created. Defaults to self.regenerate.
            append (bool, optional): If True, new properties in the template will be added to the existing template. Defaults to self.append.

        Raises:
            Exception: If the upload fails.
        """
        regenerate = kwargs.get('regenerate', self.regenerate)
        append = kwargs.get('append', self.append)
        if self.data:
            headers = {
                'cluster': self.cluster
            }
            response = requests.get(url=self.baseurl+self.api+'/'+self.name,
                                    headers=headers,
                                    verify=self.verify_SSL
                                    )
            if response.status_code == 404 or regenerate:
                self.log.info('Uploading template {}'.format(self.name))
                responseCreate = requests.post(url=self.baseurl+self.api_create,
                                               headers=headers,
                                               data=json.dumps(self.data),
                                               verify=self.verify_SSL)
                self.log.info(responseCreate.text)
            elif append:
                rJson = response.json()
                tmps = rJson.get(next(iter(rJson)))
                changed = False
                appendedKeys = []
                for k, v in tmps.get('mappings').items():
                    properties = v.get('properties')
                    flattened_props = self.flatten_dict(properties)
                    keys_to_pop = self.pop_specific_values(flattened_props, 'object')
                    newTemplate = self.get_template_dict(self.template)
                    flattened_props = self.remove_keys(flattened_props, keys_to_pop)
                    newTemplate = self.remove_keys(newTemplate, keys_to_pop)
                    appendKeys = self.compare_dictionaries(flattened_props, newTemplate)
                    appendedKeys.extend(appendKeys)
                    if appendKeys:
                        changed = True
                        appendTemplate = {newK: newTemplate.get(
                            newK) for newK in appendKeys}
                        appendProperties = self.generate_properties(
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
                    responseCreate = requests.post(url=self.baseurl+self.api_create,
                                                   headers=headers,
                                                   data=json.dumps(self.data),
                                                   verify=self.verify_SSL)
                    self.log.info(responseCreate.text)
                else:
                    self.log.info(
                        'Nothing to append in template {}'.format(self.name))
            else:
                self.log.info('Template {} already exists'.format(self.name))

    def getUrl(self, url: str) -> str:
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
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            host_ip = s.getsockname()[0]
            s.close()
            return 'https://{}'.format(host_ip)
        return url