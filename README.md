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

## Example Usage:
```python
import avantpy

url = 'https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv'
ianaList = avantpy.download.CSV(url).list
for i in range(5):
    print(ianaList[i])
ianaList = avantpy.utils.filter(ianaList,
                                keysMap=avantpy.utils.camelCase,
                                valuesMap=avantpy.utils.removeEmpty,
                                keysReplace={
                                    'contact': 'contato',
                                    'transportProtocol': 'protocolo'
                                },
                                valuesRegex={'[\[_\]]': ''}
                                )
ianaList = avantpy.utils.add(ianaList,
                             type='iana',
                             index='iana',
                             id=avantpy.utils.generateID
                             )
for i in range(5):
    print(ianaList[i])



"""
First output (ianaList)
{'Service Name': '', 'Port Number': '0', 'Transport Protocol': 'tcp', 'Description': 'Reserved', 'Assignee': '[Jon_Postel]', 'Contact': '[Jon_Postel]', 'Registration Date': '', 'Modification Date': '', 'Reference': '', 'Service Code': '', 'Unauthorized Use Reported': '', 'Assignment Notes': ''}
{'Service Name': '', 'Port Number': '0', 'Transport Protocol': 'udp', 'Description': 'Reserved', 'Assignee': '[Jon_Postel]', 'Contact': '[Jon_Postel]', 'Registration Date': '', 'Modification Date': '', 'Reference': '', 'Service Code': '', 'Unauthorized Use Reported': '', 'Assignment Notes': ''}
{'Service Name': 'tcpmux', 'Port Number': '1', 'Transport Protocol': 'tcp', 'Description': 'TCP Port Service Multiplexer', 'Assignee': '[Mark_Lottor]', 'Contact': '[Mark_Lottor]', 'Registration Date': '', 'Modification Date': '', 'Reference': '', 'Service Code': '', 'Unauthorized Use Reported': '', 'Assignment Notes': ''}
{'Service Name': 'tcpmux', 'Port Number': '1', 'Transport Protocol': 'udp', 'Description': 'TCP Port Service Multiplexer', 'Assignee': '[Mark_Lottor]', 'Contact': '[Mark_Lottor]', 'Registration Date': '', 'Modification Date': '', 'Reference': '', 'Service Code': '', 'Unauthorized Use Reported': '', 'Assignment Notes': ''}
{'Service Name': 'compressnet', 'Port Number': '2', 'Transport Protocol': 'tcp', 'Description': 'Management Utility', 'Assignee': '', 'Contact': '', 'Registration Date': '', 'Modification Date': '', 'Reference': '', 'Service Code': '', 'Unauthorized Use Reported': '', 'Assignment Notes': ''}

Second output (ianaList)
{'type': 'iana', 'index': 'iana', 'id': '3fc104569ecc8689a0409052d2e918e8', 'portNumber': '0', 'protocolo': 'tcp', 'description': 'Reserved', 'assignee': 'JonPostel', 'contato': 'JonPostel'}
{'type': 'iana', 'index': 'iana', 'id': 'bb834ea6d5f4d89fe2d0c84959dd1c9d', 'portNumber': '0', 'protocolo': 'udp', 'description': 'Reserved', 'assignee': 'JonPostel', 'contato': 'JonPostel'}
{'type': 'iana', 'index': 'iana', 'id': '75027ad8e61d72465149c2ece1b33fca', 'serviceName': 'tcpmux', 'portNumber': '1', 'protocolo': 'tcp', 'description': 'TCP Port Service Multiplexer', 'assignee': 'MarkLottor', 'contato': 'MarkLottor'}
{'type': 'iana', 'index': 'iana', 'id': 'faf1b67ec5e2f81872ec5af11a2670ce', 'serviceName': 'tcpmux', 'portNumber': '1', 'protocolo': 'udp', 'description': 'TCP Port Service Multiplexer', 'assignee': 'MarkLottor', 'contato': 'MarkLottor'}
{'type': 'iana', 'index': 'iana', 'id': 'c38069c65a04940defb44968051a5d38', 'serviceName': 'compressnet', 'portNumber': '2', 'protocolo': 'tcp', 'description': 'Management Utility'}
"""
```

