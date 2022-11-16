""" A class to execute custom search and scroll search in AvantData """

import avantpy
import logging
import json
logging.basicConfig(level=logging.INFO)

# Searches for the index IANA in avantdata

SE = avantpy.download.Search('https://prod.avantdata.com.br', index='IANA')

"""
INFO:avantpy.download.Search:Searching IANA in https://192.168.102.133
INFO:avantpy.download.Search:Total of 56039 documents found
INFO:avantpy.download.Search:Over 5000 found. Starting scroll search
INFO:avantpy.download.Search:5000/56039 downloaded documents
INFO:avantpy.download.Search:10000/56039 downloaded documents
INFO:avantpy.download.Search:15000/56039 downloaded documents
INFO:avantpy.download.Search:20000/56039 downloaded documents
INFO:avantpy.download.Search:25000/56039 downloaded documents
INFO:avantpy.download.Search:30000/56039 downloaded documents
INFO:avantpy.download.Search:35000/56039 downloaded documents
INFO:avantpy.download.Search:40000/56039 downloaded documents
INFO:avantpy.download.Search:45000/56039 downloaded documents
INFO:avantpy.download.Search:50000/56039 downloaded documents
INFO:avantpy.download.Search:55000/56039 downloaded documents
INFO:avantpy.download.Search:56039 downloaded documents
"""

logging.info(len(SE.data))

"""
INFO:root:56039
"""

logging.info(json.dumps(SE.data[20095:20100], indent=4))

"""
INFO:root:[
    {
        "id": "6e0bff4cfd8d29eaad03a6ca3a9ae306",
        "type": "iana",
        "index": "iana",
        "serviceName": "arn",
        "transportProtocol": "tcp",
        "description": "Active Registry Network for distribution of values and streams",
        "assignee": "Mictron",
        "contact": "Michael_Wiklund",
        "registrationDate": 1381968000000,
        "assignmentNotes": "Defined TXT keys: None",
        "GenerateTime": 1668606445000
    },
    {
        "id": "6371eb6b2eba2ac7de9d41e3c089771f",
        "type": "iana",
        "index": "iana",
        "serviceName": "aroundsound",
        "description": "AroundSound's information sharing protocol",
        "assignee": "Winzig_LLC",
        "contact": "Around_Sound",
        "registrationDate": 1319065200000,
        "assignmentNotes": "Defined TXT keys: Proprietary",
        "GenerateTime": 1668606445000
    },
    {
        "id": "7e8bc75f665a97947f27622e0015a82c",
        "type": "iana",
        "index": "iana",
        "serviceName": "atlassianapp",
        "description": "Atlassian Application (JIRA, Confluence, Fisheye, Crucible, Crowd, Bamboo) discovery service",
        "assignee": "Denise_Fernandez",
        "contact": "Denise_Fernandez",
        "assignmentNotes": "Defined TXT keys: app.url",
        "GenerateTime": 1668606445000
    },
    {
        "id": "0ba8436e2a51bb7d5898eb077fd6cd47",
        "type": "iana",
        "index": "iana",
        "serviceName": "audirvana-ap",
        "transportProtocol": "tcp",
        "description": "Audirvana Remote Access Protocol",
        "assignee": "Audirvana_SCS",
        "contact": "Damien_Plisson",
        "registrationDate": 1437436800000,
        "assignmentNotes": "Defined TXT keys: txtvers, protovers",
        "GenerateTime": 1668606445000
    },
    {
        "id": "a8c6b8e29935e588df2fc046bd998489",
        "type": "iana",
        "index": "iana",
        "serviceName": "av-chat-ring-01",
        "transportProtocol": "tcp",
        "description": "TCP SpyChat Stream Message Exchange",
        "assignee": "Alexios_Vasileiadis",
        "contact": "Alexios_Vasileiadis",
        "registrationDate": 1525305600000,
        "assignmentNotes": "Defined TXT keys: There are two TXT record keys: 1st key: \"txt-vers\" associated with an 'int' entry. 2nd key: \"conn-stat\" associated with an 'int' entry.",
        "GenerateTime": 1668606445000
    }
]
"""