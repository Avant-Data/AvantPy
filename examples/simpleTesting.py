import avantpy
import logging
import json
logging.basicConfig(level=logging.INFO)

NAME = 'testingtemplate'
ALIASES = 'testingTemplate'
URL = 'https://avantnightly.avantsec.com.br'

dataList = [
    {
        'teste': 'valor',
        'nightly': 'valor',
        'objeto': {'kkkk': 'll', 'lll': 'oo'},
        'liksta': [{'aaaaa':2, 'bbbbb':3},{'ccccc':2, 'ddddd':3}]
    }
]

template = avantpy.upload.Template(name=NAME,
                                   template=dataList,
                                   baseurl=URL)

template.upload()
dataList = avantpy.utils.add(dataList,
id=avantpy.utils.generateID,
index=NAME,
type=NAME)
avantpy.upload.UpsertBulk(dataList, baseurl=URL)
