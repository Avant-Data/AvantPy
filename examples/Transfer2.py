"""
Transfer class:
Download data, create template and upload documents.

Transfer example arguments:
json: download https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
select: Extract values from key "vulnerabilities"
name: Set the name, index and type of the template to "cisakevs_teste"
aliases: Set the aliases of the template to "KEVS_CISA"
baseurl: Set the baseurl destiny to https://192.168.102.133
All arguments of avantpy.upload.UpsertBulk and avantpy.upload.Tempalte can also be passed
"""

from avantpy import Transfer
import logging
logging.basicConfig(level=logging.INFO)

Transfer(json='https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json',
         select='vulnerabilities',
         name='cisakevs_teste',
         aliases='KEVS_CISA',
         baseurl='https://192.168.102.133'
         )