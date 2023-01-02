<p align="center">
  <a href="" rel="noopener">
 <img width=250px height=82px src="https://i.imgur.com/zHVh1RJ.png" alt="AvantData"></a>
</p>

<h3 align="center">AvantPy</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()

</div>

---

<p align="center"> AvantData Python Library
    <br> 
</p>

## Table of Contents

- [About](#about)
- [Installing](#installing)
- [Usage](#usage)
- [Examples](#examples)
- [Built Using](#builtUsing)
- [TODO](#TODO)

## About <a name = "about"></a>

This library contains a set of tools capable of prepare data to be in a list of dictionaries format and, after that, manipulate this data and index it in AvantData with AvantApi

## Installing<a name = "installing"></a>

The installation can be done by exporting the [avantpy](./avantpy) folder to the local working repository or by installing it as a library. The installation as library can be done by making the wheel with [setup.py](./setup.py) file and installing it with pip

```shell
python setup.py bdist_wheel && pip install dist/avantpy*.whl
```

## Usage <a name="usage"></a>

The structure of avantpy consists of classes capable to [download](./avantpy/download/) data from different formats and leaving them in dictionary list format, ready to be [upload](./avantpy/upload/) in AvantData. The whole process can also be shortened with a [transfer](./avantpy/Transfer.py) if there is no need to edit the data.
```shell
avantpy
├── download
│   ├── CSV.py
│   ├── JSON.py
│   └── Search.py
├── Transfer.py
├── upload
│   ├── Template.py
│   └── UpsertBulk.py
└── utils.py
```

## Examples <a name = "examples"></a>

The first step to work with AvantPy is to make a list of dictionaries `[{...},{...},{...},...]` containing the data to be indexed.
To do so, it is possible to it with [download](./avantpy/download/) built-in classes, where the class will be choosed according to the data format.

A example using [Search](./avantpy/download/Search.py) to download documents from avantdata

```python
>>> import logging
>>> logging.basicConfig(level=logging.INFO)
>>> from avantpy.download import Search
>>> s = Search('https://192.168.102.10/', index='avantscan_results')
INFO:avantpy.download.Search:Searching avantscan_results in https://192.168.102.10
INFO:avantpy.download.Search:Total of 44639 documents found
INFO:avantpy.download.Search:Over 5000 found. Starting scroll search
INFO:avantpy.download.Search:5000/44639 downloaded documents
INFO:avantpy.download.Search:10000/44639 downloaded documents
INFO:avantpy.download.Search:15000/44639 downloaded documents
INFO:avantpy.download.Search:20000/44639 downloaded documents
INFO:avantpy.download.Search:25000/44639 downloaded documents
INFO:avantpy.download.Search:30000/44639 downloaded documents
INFO:avantpy.download.Search:35000/44639 downloaded documents
INFO:avantpy.download.Search:40000/44639 downloaded documents
INFO:avantpy.download.Search:44639 downloaded documents
>>> len(s.data)
44639
>>> [type(d) for d in s.data[:5]]
[<class 'dict'>, <class 'dict'>, <class 'dict'>, <class 'dict'>, <class 'dict'>]
>>> s.data[0].keys()
dict_keys(['id', 'type', 'index', 'reportID', 'taskID', 'taskName', 'taskComment', 'targetID', 'targetName', 'targetComment', 'resultID', 'description', 'assetIP', 'assetID', 'resultName', 'nvt', 'originalSeverity', 'originalThreat', 'owner', 'qodValue', 'overridedSeverity', 'overridedThreat', 'executionTime', 'executionTimeZone', 'modificationTime', 'modificationTimeZone', 'scanNVTVersion', 'scanNVTVersionZone', 'portNumber', 'portProtocol', 'portIANA', 'GenerateTime'])
```
A example downloading a [JSON](./avantpy/download/JSON.py) from CISA

```python
>>> import logging
>>> logging.basicConfig(level=logging.INFO)
>>> from avantpy.download import JSON
>>> kev = JSON('https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json', select='vulnerabilities')
INFO:avantpy.download.JSON:Reading https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
INFO:avantpy.download.JSON:<Response [200]> with 740KB. 868 dictionaries added to data attribute
>>> len(kev.data)
868
```
After having the data, it is time to prepare it to be uploaded to AvantData. A [template](./avantpy/upload/Template.py) must be made with the data structure. This is an example of how to make a template with data downloaded from CISA
```python
>>> from avantpy.upload import Template
>>> template = Template(name='kev', template=kev.data, baseurl='https://192.168.102.10', append=True)
>>> template.upload()
INFO:avantpy.upload.Template:Uploading template kev
INFO:avantpy.upload.Template:{"acknowledged":true}
```
And finally, data can now be uploaded to AvantData using this UpsertBulk example after appending a type, index and id key for each dictionary of the data.
```python
>>> from avantpy import utils
>>> from avantpy.upload import UpsertBulk
>>> kev.data = utils.add(kevfrom.data, id=utils.generateID, type='kev', index='kev')
>>> UpsertBulk(kev.data, baseurl='https://192.168.102.10').upload()
INFO:avantpy.upload.UpsertBulk:Total: 868
INFO:avantpy.upload.UpsertBulk:Updated: 0, Created 868. 
INFO:avantpy.upload.UpsertBulk:868 successfully executed with 0 failures
INFO:avantpy.upload.UpsertBulk:Created: 868 / Updated: 0 / Failed: 0
```

## Built Using <a name = "builtUsing"></a>
- [AvantData](https://www.avantdata.com.br/) - Platform for analysis, correlation and data management in corporate networks
- [AvantApi](https://avantapi.avantsec.com.br/) - Family of RESTFUL API endpoints for customizing actions in AvantData

## TODO <a name = "TODO"></a>
- Add zip/tar decompressors in download
- Add a txt regex downloader
- Add a class to upload to Redis