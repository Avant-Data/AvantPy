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

ianaList = avantpy.download.CSV('https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv').list
ianaList = avantpy.utils.removeEmpty(ianaList)
ianaList = avantpy.utils.add(ianaList, type='iana', index='iana', id=avantpy.utils.generateID)

""" Output (ianaList)
[
{'type': 'iana', 'index': 'iana', 'id': '724fd6be68bc796a744af51f4bec273f', 'Port Number': '0', 'Transport Protocol': 'tcp', 'Description': 'Reserved', 'Assignee': '[Jon_Postel]', 'Contact': '[Jon_Postel]'}
{'type': 'iana', 'index': 'iana', 'id': '775a75c993149105c167d0d1ad0a8baa', 'Port Number': '0', 'Transport Protocol': 'udp', 'Description': 'Reserved', 'Assignee': '[Jon_Postel]', 'Contact': '[Jon_Postel]'}
{'type': 'iana', 'index': 'iana', 'id': 'f6d45c96471cd1dc60e8893bf113b631', 'Service Name': 'tcpmux', 'Port Number': '1', 'Transport Protocol': 'tcp', 'Description': 'TCP Port Service Multiplexer', 'Assignee': '[Mark_Lottor]', 'Contact': '[Mark_Lottor]'}
{'type': 'iana', 'index': 'iana', 'id': '1c3cb600d80df63da46971a64f003595', 'Service Name': 'tcpmux', 'Port Number': '1', 'Transport Protocol': 'udp', 'Description': 'TCP Port Service Multiplexer', 'Assignee': '[Mark_Lottor]', 'Contact': '[Mark_Lottor]'}
{'type': 'iana', 'index': 'iana', 'id': '8c248f5ed127b89a30238ea355d67dd4', 'Service Name': 'compressnet', 'Port Number': '2', 'Transport Protocol': 'tcp', 'Description': 'Management Utility'}
]
"""
```

