"""
This is a one line example of how to upload documents to AvantData

Transfer class:
Download data, create template and upload documents.

Transfer example arguments:
data: the list of dictionaries to be uploaded
name: Set the name, index and type of the template to "data_transfer_test"
baseurl: Set the baseurl destiny to https://192.168.102.133
All arguments of avantpy.upload.UpsertBulk and avantpy.upload.Tempalte can also be passed
"""

from avantpy import Transfer

Transfer(data=[{'key1': 'test', 'key2': 'test'},{'key3': 'test'}], name='data_transfer_test', baseurl='https://192.168.102.133')