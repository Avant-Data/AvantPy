import avantpy
import logging
logging.basicConfig(level=logging.INFO)

NAME = 'testingtemplate'
ALIASES = 'testingTemplate'
URL = 'https://prod.avantdata.com.br'

""" dataList = [
    {
        'teste': 'valor',
        'nightly': 'valor',
        'objeto': {'kkkk': 'll', 'lll': 'oo'},
        'liksta': [{'aaaaa':2, 'bbbbb':3},{'ccccc':2, 'ddddd':3}]
    }
] """
dataList = [
    {
        'liksta': [{'aaaaa':2, 'bbbbb':3},{'ccccc':2, 'ddddd':3}],
        #'hybrid': ['ok', {'someObj': 'ipipip'}],
        'qqqqqq': [1,2,4,3,4,9, 'teste'],
        'kkkkkkkk': [1,2,4,3,4,9, 'teste'],
        'maoi': 'teste',
        'maisUma': 'ooooo',
        'IOIOIO': [{'xd':1}]
    }
]
dataList = []
dataList.append({'testing1':'test', 'testing2':'test', 'testing3':'test'})
dataList.append({'testing4':'test', 'testing5':'test', 'testing6':'test'})
dataList.append({'testing7':'test', 'testing8':'test', 'testing9':'test'})

#print(dataList)
template = avantpy.upload.Template(name=NAME,
                                   template=dataList,
                                   baseurl=URL)
dataList.append({'testing10':'test', 'testing11':'test', 'testing13':'test'})
template.upload(append=True)
""" dataList = avantpy.utils.add(dataList,
id=avantpy.utils.generateID,
index=NAME,
type=NAME)
avantpy.upload.UpsertBulk(dataList, baseurl=URL) """
