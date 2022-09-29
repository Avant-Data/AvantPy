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
- [Built Using](#builtUsing)
- [TODO](#TODO)

## About <a name = "about"></a>

This library contains a set of tools capable of prepare data to be in a list of dictionaries format and, after that, manipulate this data and index it in AvantData with AvantApi

## Installing<a name = "installing"></a>

The installation can be done by exporting the [avantpy](./avantpy) folder to the local working repository or by installing it as a library. The installation as library can be done by making the wheel with [setup.py](./setup.py) file and installing it with pip

```shell
python setup.py bdist_wheel && pip install dist/avantpy*.whl
```

## Usage <a name = "usage"></a>

The first step to work with AvantPy is to make a list of dictionaries `[{...},{...},{...},...]` containing the data to be indexed.
To do so, it is possible to it with [download](./avantpy/download/) built-in classes, where the class will be choosed according to the data format.

A example using [Search](./avantpy/download/Search.py) to download documents from avantdata

```python
>>> import logging
>>> logging.basicConfig(level=logging.INFO)
>>> from avantpy.download import Search
>>> s = Search('https://prod.avantdata.com.br', index='avantscan_results', format=True)
INFO:avantpy.download.Search:Searching avantscan_results in https://prod.avantdata.com.br
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
A example downloading a JSON from CISA

```python
>>> import logging
>>> logging.basicConfig(level=logging.INFO)
>>> import avantpy
>>> j = avantpy.download.JSON('https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json', select='vulnerabilities')
INFO:avantpy.download.JSON:Reading https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
INFO:avantpy.download.JSON:<Response [200]> with 706KB. 832 dictionaries added to data attribute
>>> 
```

The second step is to prepare the data within list dictionaries to be suitable for indexing. [utils](./avantpy/utils.py) contains various functions to manipulate list of dictionaries, such as `add()` which will add keys and values to each dictionary or `edit()` which will use a function or a regex on a key or on a value.

The third step is to upload the list of dictionaries to AvantData with [upload](./avantpy/upload/) built-in classes

Also, simple way to prepare and index data is with [Transfer](./avantpy/Transfer.py), a class which will do all the steps if there is no need to edit the data before indexing.

### Transfer
In one example the user wants to import [CISA Catalog of Known Exploited Vulnerabilities](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json) json file into AvantData. It is possible to import it by specifying the json url with `json` parameter, the name of the index and template with `name`, the `aliases` that will be used to search for it and the `baseurl`where the document will be indexed. Note that you will need to have the AvantApi installed to make this work.

Also, as the json is made up of the following keys:
- title &#8594; *string*
- catalogVersion &#8594; *string*
- dateRelease &#8594; *string of date*
- count &#8594; *int*
- vulnerabilities &#8594; *list of dictionaries*

`vulnerabilities` is the list of dictionaries target to be indexed in AvantData, so it will be the value of the `obj` parameter.
```python
import avantpy

JSON_URL = 'https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json'
avantpy.Transfer(json=JSON_URL,
                 obj='vulnerabilities',
                 name='cisakevs',
                 aliases='KEV',
                 baseurl='https://192.168.102.133/'
                 )
```

####  Data that will be indexed in AvantData (first 5 documents)
| type | index | id |  cveID |  vendorProject | product | vulnerabilityName | dateAdded | shortDescription | requiredAction | dueDate | notes |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| cisakevs | cisakevs | 04019464675c64463e6e7d453309c919 | CVE-2021-27104 | Accellion | FTA | Accellion FTA OS Command Injection Vulnerability | 2021-11-03 | Accellion FTA 9_12_370 and earlier is affected by OS command execution via a crafted POST request to various admin endpoints. | Apply updates per vendor instructions. | 2021-11-17 | '' |
| cisakevs | cisakevs | 0c2df08bca3ab75505d5fc606eec97bb | CVE-2021-27102 | Accellion | FTA | Accellion FTA OS Command Injection Vulnerability | 2021-11-03 | Accellion FTA 9_12_411 and earlier is affected by OS command execution via a local web service call. | Apply updates per vendor instructions. | 2021-11-17 | '' |
| cisakevs | cisakevs | ac4b3c13380a12f457760d82913f0926 | CVE-2021-27101 | Accellion | FTA | Accellion FTA SQL Injection Vulnerability | 2021-11-03 | Accellion FTA 9_12_370 and earlier is affected by SQL injection via a crafted Host header in a request to document_root.html. | Apply updates per vendor instructions. | 2021-11-17 | '' |
| cisakevs | cisakevs | 535855aaa714b2b26b73e2047ecdf531 | CVE-2021-27103 | Accellion | FTA | Accellion FTA SSRF Vulnerability | 2021-11-03 | Accellion FTA 9_12_411 and earlier is affected by SSRF via a crafted POST request to wmProgressstat.html. | Apply updates per vendor instructions. | 2021-11-17 | '' |
| cisakevs | cisakevs | 5500d99c5d2b14be3be7fd287bc773d3 | CVE-2021-21017 | Adobe | Acrobat and Reader | Adobe Acrobat and Reader Heap-based Buffer Overflow Vulnerability | 2021-11-03 | Acrobat Reader DC versions versions 2020.013.20074 (and earlier), 2020.001.30018 (and earlier) and 2017.011.30188 (and earlier) are affected by a heap-based buffer overflow vulnerability. An unauthenticated attacker could leverage this vulnerability to achieve arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file | Apply updates per vendor instructions. | 2021-11-17 | '' |

### Download, Prepare and Upload

another way to use AvantPy in a situation where data manipulation is required is through all the steps mentioned above. As in this csv example where the [Service Name and Transport Protocol Port Number Registry](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml) is downloaded to be in a list of dictionaries. After the download, some data preparation is done to use the `Template()` class where a template will be created in AvantData if it doesn't exist. Thereafter, a `type`, `index` and `id` are added to be in the correct format for uploading to AvantData with `UpsertBulk()`.

```python
import avantpy

CSV_URL = 'https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv'
ianaList = avantpy.download.CSV(CSV_URL).list
ianaList = avantpy.utils.edit(ianaList,
                              keys=avantpy.utils.camelCase,
                              values=[avantpy.utils.removeEmpty,
                                {
                                  '[\[\]]': '',
                                  '_': ' '
                                }
                              ])
avantpy.upload.Template(name='iana',
                        template=ianaList,
                        aliases='IANA',
                        baseurl='https://192.168.102.133/'
                        )
ianaList = avantpy.utils.add(ianaList,
                             type='iana',
                             index='iana',
                             id=avantpy.utils.generateID
                             )
avantpy.upload.UpsertBulk(ianaList,
                          baseurl='https://192.168.102.133/'
                          )
```
#### Downloaded CSV (lines 1 to 5)
| Service Name | Port Number | Transport Protocol |  Description |  Assignee |  Contact | Registration Date | Modification Date | Reference | Service Code | Unauthorized Use Reported | Assignment Notes |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| '' | 0 | tcp | Reserved | [Jon_Postel] | '' | '' | '' | '' | '' | '' | '' |
| '' | 0 | udp | Reserved | [Jon_Postel] | '' | '' | '' | '' | '' | '' | '' |
| tcpmux | 1 | tcp | TCP Port Service Multiplexer | [Mark_Lottor] | [Mark_Lottor] | '' | '' | '' | '' | '' | '' |
| tcpmux | 1 | udp | TCP Port Service Multiplexer | [Mark_Lottor] | [Mark_Lottor] | '' | '' | '' | '' | '' | '' |
| compressnet | 2 | tcp | Management Utility | '' | '' | '' | '' | '' | '' | '' | '' |

#### Uploaded Documents (1 to 5)

| serviceName | portNumber | transportProtocol |  description |  assignee |  contact | type | index | id | GenerateTime |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| | 0 | tcp | Reserved | Jon Postel | | iana | iana | 6fee099da7dfbb67599d7fa7389de898 | 1661543905000 |
| | 0 | udp | Reserved | Jon Postel | | iana | iana | 58f77dcc14a41b2984e298e86db85c73 | 1661543905000 |
| tcpmux | 1 | tcp | TCP Port Service Multiplexer | Mark Lottor | Mark Lottor | iana | iana | 1a29a08c6b2252fba8461330dba79027 | 1661543905000 |
| tcpmux | 1 | udp | TCP Port Service Multiplexer | Mark Lottor | Mark Lottor | iana | iana | ed23fa12819a63198b5c0b171ebbbf2d | 1661543905000 |
| compressnet | 2 | tcp | Management Utility | | | iana | iana | 15e0d1cd9db50a856604e28614429b5c | 1661543905000 |

## Built Using <a name = "builtUsing"></a>
- [AvantData](https://www.avantdata.com.br/) - Platform for analysis, correlation and data management in corporate networks
- [AvantApi](https://avantapi.avantsec.com.br/) - Family of RESTFUL API endpoints for customizing actions in AvantData

## TODO <a name = "TODO"></a>
- Improve the auto generation of Templates
- remove() function in utils
- Improve the logs of UpsertBulk
- Date parser in utils
- extend() function in utils
- Add customSearch and scrollSearch to download classes
- Add zip/tar decompressors in download
- Enable the threads manipulation in upload and download
- 