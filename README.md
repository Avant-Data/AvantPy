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
```javascript
import avantpy

ianaList = avantpy.download.CSV('https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv').list
ianaList = avantpy.utils.removeEmpty(ianaList)
ianaList = avantpy.utils.add(ianaList, type='iana', index='iana', id=avantpy.utils.generateID(ianaList))

""" Output (ianaList)
[
{'type': 'iana', 'index': 'iana', 'id': '212695eaca0ed17bfbd0676f7738d669', 'Port Number': '0', 'Transport Protocol': 'tcp', 'Description': 'Reserved', 'Assignee': '[Jon_Postel]', 'Contact': '[Jon_Postel]'},
{'type': 'iana', 'index': 'iana', 'id': '212695eaca0ed17bfbd0676f7738d669', 'Port Number': '0', 'Transport Protocol': 'udp', 'Description': 'Reserved', 'Assignee': '[Jon_Postel]', 'Contact': '[Jon_Postel]'},
{'type': 'iana', 'index': 'iana', 'id': '212695eaca0ed17bfbd0676f7738d669', 'Service Name': 'tcpmux', 'Port Number': '1', 'Transport Protocol': 'tcp', 'Description': 'TCP Port Service Multiplexer', 'Assignee': '[Mark_Lottor]', 'Contact': '[Mark_Lottor]'},
{'type': 'iana', 'index': 'iana', 'id': '212695eaca0ed17bfbd0676f7738d669', 'Service Name': 'tcpmux', 'Port Number': '1', 'Transport Protocol': 'udp', 'Description': 'TCP Port Service Multiplexer', 'Assignee': '[Mark_Lottor]', 'Contact': '[Mark_Lottor]'},
{'type': 'iana', 'index': 'iana', 'id': '212695eaca0ed17bfbd0676f7738d669', 'Service Name': 'compressnet', 'Port Number': '2', 'Transport Protocol': 'tcp', 'Description': 'Management Utility'},
{'type': 'iana', 'index': 'iana', 'id': '212695eaca0ed17bfbd0676f7738d669', 'Service Name': 'compressnet', 'Port Number': '2', 'Transport Protocol': 'udp', 'Description': 'Management Utility'},
{'type': 'iana', 'index': 'iana', 'id': '212695eaca0ed17bfbd0676f7738d669', 'Service Name': 'compressnet', 'Port Number': '3', 'Transport Protocol': 'tcp', 'Description': 'Compression Process', 'Assignee': '[Bernie_Volz]', 'Contact': '[Bernie_Volz]'},
{'type': 'iana', 'index': 'iana', 'id': '212695eaca0ed17bfbd0676f7738d669', 'Service Name': 'compressnet', 'Port Number': '3', 'Transport Protocol': 'udp', 'Description': 'Compression Process', 'Assignee': '[Bernie_Volz]', 'Contact': '[Bernie_Volz]'},
{'type': 'iana', 'index': 'iana', 'id': '212695eaca0ed17bfbd0676f7738d669', 'Port Number': '4', 'Transport Protocol': 'tcp', 'Description': 'Unassigned'},
{'type': 'iana', 'index': 'iana', 'id': '212695eaca0ed17bfbd0676f7738d669', 'Port Number': '4', 'Transport Protocol': 'udp', 'Description': 'Unassigned'}
]
"""
```

