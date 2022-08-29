<p align="center">
  <a href="" rel="noopener">
 <img width=250px height=82px src="https://i.imgur.com/zHVh1RJ.png" alt="Project logo"></a>
</p>

<h3 align="center">AvantPy</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()

</div>

---

<p align="center"> AvantData Python Library
    <br> 
</p>

## Summary

- [Sobre](#about)
- [Instalação](#installing)
- [Utilização](#usage)
- [Testando](#testing)

## Example Usage:
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