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

AvantPy was created with the intention of making it easier to index data in AvantData. This library contains a set of tools capable of preparing data to be in dictionary list format and, after that, manipulating this data in order to prepare it to be indexed in AvantData with AvantApi

## Installing<a name = "installing"></a>

The installation can be done by exporting the [avantpy](./avantpy) folder to the local working repository or by installing it as a library. The installation as library can be done by making the wheel with [setup.py](./setup.py) file and installing it with pip

```shell
python setup.py bdist_wheel && pip install dist/avantpy-0.1.0-py3-none-any.whl
```

## Usage <a name = "usage"></a>
It is possible to download, prepare and index data with [Transfer](./avantpy/Transfer.py). 

| type | index | id |  cveID |  vendorProject | product | vulnerabilityName | dateAdded | shortDescription | requiredAction | dueDate | notes |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| | 0 | tcp | Reserved | Jon Postel | | iana | iana | 6fee099da7dfbb67599d7fa7389de898 | 1661543905000 |
| | 0 | udp | Reserved | Jon Postel | | iana | iana | 58f77dcc14a41b2984e298e86db85c73 | 1661543905000 |
| tcpmux | 1 | tcp | TCP Port Service Multiplexer | Mark Lottor | Mark Lottor | iana | iana | 1a29a08c6b2252fba8461330dba79027 | 1661543905000 |
| tcpmux | 1 | udp | TCP Port Service Multiplexer | Mark Lottor | Mark Lottor | iana | iana | ed23fa12819a63198b5c0b171ebbbf2d | 1661543905000 |
| compressnet | 2 | tcp | Management Utility | | | iana | iana | 15e0d1cd9db50a856604e28614429b5c | 1661543905000 |



{'type': 'cisakevs_teste', 'index': 'cisakevs_teste', 'id': '04019464675c64463e6e7d453309c919', 'cveID': 'CVE-2021-27104', 'vendorProject': 'Accellion', 'product': 'FTA', 'vulnerabilityName': 'Accellion FTA OS Command Injection Vulnerability', 'dateAdded': '2021-11-03', 'shortDescription': 'Accellion FTA 9_12_370 and earlier is affected by OS command execution via a crafted POST request to various admin endpoints.', 'requiredAction': 'Apply updates per vendor instructions.', 'dueDate': '2021-11-17', 'notes': ''}
{'type': 'cisakevs_teste', 'index': 'cisakevs_teste', 'id': '0c2df08bca3ab75505d5fc606eec97bb', 'cveID': 'CVE-2021-27102', 'vendorProject': 'Accellion', 'product': 'FTA', 'vulnerabilityName': 'Accellion FTA OS Command Injection Vulnerability', 'dateAdded': '2021-11-03', 'shortDescription': 'Accellion FTA 9_12_411 and earlier is affected by OS command execution via a local web service call.', 'requiredAction': 'Apply updates per vendor instructions.', 'dueDate': '2021-11-17', 'notes': ''}
{'type': 'cisakevs_teste', 'index': 'cisakevs_teste', 'id': 'ac4b3c13380a12f457760d82913f0926', 'cveID': 'CVE-2021-27101', 'vendorProject': 'Accellion', 'product': 'FTA', 'vulnerabilityName': 'Accellion FTA SQL Injection Vulnerability', 'dateAdded': '2021-11-03', 'shortDescription': 'Accellion FTA 9_12_370 and earlier is affected by SQL injection via a crafted Host header in a request to document_root.html.', 'requiredAction': 'Apply updates per vendor instructions.', 'dueDate': '2021-11-17', 'notes': ''}
{'type': 'cisakevs_teste', 'index': 'cisakevs_teste', 'id': '535855aaa714b2b26b73e2047ecdf531', 'cveID': 'CVE-2021-27103', 'vendorProject': 'Accellion', 'product': 'FTA', 'vulnerabilityName': 'Accellion FTA SSRF Vulnerability', 'dateAdded': '2021-11-03', 'shortDescription': 'Accellion FTA 9_12_411 and earlier is affected by SSRF via a crafted POST request to wmProgressstat.html.', 'requiredAction': 'Apply updates per vendor instructions.', 'dueDate': '2021-11-17', 'notes': ''}
{'type': 'cisakevs_teste', 'index': 'cisakevs_teste', 'id': '5500d99c5d2b14be3be7fd287bc773d3', 'cveID': 'CVE-2021-21017', 'vendorProject': 'Adobe', 'product': 'Acrobat and Reader', 'vulnerabilityName': 'Adobe Acrobat and Reader Heap-based Buffer Overflow Vulnerability', 'dateAdded': '2021-11-03', 'shortDescription': 'Acrobat Reader DC versions versions 2020.013.20074 (and earlier), 2020.001.30018 (and earlier) and 2017.011.30188 (and earlier) are affected by a heap-based buffer overflow vulnerability. An unauthenticated attacker could leverage this vulnerability to achieve arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.', 'requiredAction': 'Apply updates per vendor instructions.', 'dueDate': '2021-11-17', 'notes': ''}


```python
import avantpy

url = 'https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv'
ianaList = avantpy.download.CSV(url).list
ianaList = avantpy.utils.edit(ianaList,
                                keysMap=avantpy.utils.camelCase,
                                valuesMap=avantpy.utils.removeEmpty,
                                valuesRegex={
                                    '[\[\]]': '',
                                    '_': ' '
                                }
                             )
avantpy.upload.Template(name='iana',
                        template=ianaList,
                        baseurl='https://avantnightly.avantsec.com.br/'
                       )
ianaList = avantpy.utils.add(ianaList,
                             type='iana',
                             index='iana',
                             id=avantpy.utils.generateID,
                            )
avantpy.upload.UpsertBulk(ianaList,
                          baseurl='https://avantnightly.avantsec.com.br/'
                         )
```
### Downloaded CSV (lines 1 to 5)
| Service Name | Port Number | Transport Protocol |  Description |  Assignee |  Contact | Registration Date | Modification Date | Reference | Service Code | Unauthorized Use Reported | Assignment Notes |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| '' | 0 | tcp | Reserved | [Jon_Postel] | '' | '' | '' | '' | '' | '' | '' |
| '' | 0 | udp | Reserved | [Jon_Postel] | '' | '' | '' | '' | '' | '' | '' |
| tcpmux | 1 | tcp | TCP Port Service Multiplexer | [Mark_Lottor] | [Mark_Lottor] | '' | '' | '' | '' | '' | '' |
| tcpmux | 1 | udp | TCP Port Service Multiplexer | [Mark_Lottor] | [Mark_Lottor] | '' | '' | '' | '' | '' | '' |
| compressnet | 2 | tcp | Management Utility | '' | '' | '' | '' | '' | '' | '' | '' |

### Uploaded Documents (1 to 5)

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