import avantpy
import logging
import json
logging.basicConfig(level=logging.INFO)

# data to serve as a template. Note that someDate is in epoch millis. It can be transformed with utils.dateToEpochMillis
dataList = [
    {
        'someListOfDict': [{'aaaaa':2, 'bbbbb':3},{'ccccc':2, 'ddddd':3}],
        'someTuple': (1,2,4,3,4,9, 'teste'),
        'someList': [1,2,4,3,4,9, 'teste'],
        'someString': 'test',
        'someInt': 43,
        'someFloat': 6.7,
        'someDate': 1668616843000,
        'someListOfDictOneItem': [{'t':1}]
    }
]

# Initializing the Template class
template = avantpy.upload.Template(name='testing_template',
                                   template=dataList,
                                   custom={
                                    'someInt': 'integer',
                                    'someFloat': 'float',
                                    'someDate': 'date',
                                   },
                                   baseurl='https://192.168.102.133')

# Let's see what is the template generated in template.data
logging.info(json.dumps(template.data, indent=4))
"""
INFO:root:{
    "name": "testing_template",
    "order": 1,
    "body": {
        "template": "testing_template*",
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
                "number_of_shards": 2,
                "number_of_replicas": "0"
            }
        },
        "mappings": {
            "testing_template": {
                "_all": {
                    "norms": false,
                    "enabled": true
                },
                "_size": {
                    "enabled": true
                },
                "properties": {
                    "someInt": {
                        "type": "integer"
                    },
                    "someFloat": {
                        "type": "float"
                    },
                    "someListOfDict": {
                        "type": "object"
                    },
                    "someString": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        },
                        "analyzer": "WS"
                    },
                    "someDate": {
                        "type": "date",
                        "format": "yyyy/MM/dd HH:mm:ss||epoch_millis"
                    },
                    "someTuple": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        },
                        "analyzer": "WS"
                    },
                    "someList": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        },
                        "analyzer": "WS"
                    },
                    "someListOfDictOneItem": {
                        "type": "object"
                    },
                    "GenerateTime": {
                        "type": "date",
                        "format": "yyyy/MM/dd HH:mm:ss||epoch_millis"
                    }
                }
            }
        },
        "aliases": {
            "Testing_Template": {}
        }
    }
}
"""

# Now that the template seems ok, it's to upload
template.upload()
"""
INFO:avantpy.upload.Template:Uploading template testing_template
INFO:avantpy.upload.Template:{"acknowledged":true}
"""

# Now let's append some keys to dataList, append to the template and upload again
dataList.append({'testing10':'test', 'testing11':'test', 'testing13':'test'})
template.upload(append=True)
"""
INFO:avantpy.upload.Template:Appending keys ['testing10', 'testing13', 'testing11']
INFO:avantpy.upload.Template:{"acknowledged":true}
"""

# Checking the template.data again, we can see that the keys testing10, testing11 and testing13 were added to the template
logging.info(json.dumps(template.data, indent=4))
"""
INFO:root:{
    "name": "testing_template",
    "order": 1,
    "body": {
        "template": "testing_template*",
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
            "testing_template": {
                "_all": {
                    "norms": false,
                    "enabled": true
                },
                "_size": {
                    "enabled": true
                },
                "properties": {
                    "someInt": {
                        "type": "integer"
                    },
                    "someFloat": {
                        "type": "float"
                    },
                    "someListOfDict": {
                        "type": "object"
                    },
                    "someString": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        },
                        "analyzer": "WS"
                    },
                    "someDate": {
                        "type": "date",
                        "format": "yyyy/MM/dd HH:mm:ss||epoch_millis"
                    },
                    "someTuple": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        },
                        "analyzer": "WS"
                    },
                    "someList": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        },
                        "analyzer": "WS"
                    },
                    "someListOfDictOneItem": {
                        "type": "object"
                    },
                    "GenerateTime": {
                        "type": "date",
                        "format": "yyyy/MM/dd HH:mm:ss||epoch_millis"
                    },
                    "testing10": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        },
                        "analyzer": "WS"
                    },
                    "testing13": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        },
                        "analyzer": "WS"
                    },
                    "testing11": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        },
                        "analyzer": "WS"
                    }
                }
            }
        },
        "aliases": {
            "Testing_Template": []
        }
    }
}
"""