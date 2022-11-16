""" Downloading a JSON from CISA, creating a template and sending JSON data to avantdata"""

import avantpy
import logging
logging.basicConfig(level=logging.INFO)

NAME = 'testing_json'
URL = 'https://avantshow.avantdata.com.br'

# Downloads the JSON, selecting the key `vulnerabilities`, which contains the data as a list of dictionaries
kevs = avantpy.download.JSON(request='https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json', select='vulnerabilities')
# Set dataList to be the downloaded list of dictionaries
dataList = kevs.data

# Create and upload the template to AvantData
template = avantpy.upload.Template(name=NAME, template=dataList, baseurl=URL)
template.upload()

# Insert the keys id, type and index in each dictionary of dataList
dataList = avantpy.utils.add(dataList, id=avantpy.utils.generateID, type=NAME, index=NAME)

# Upload dataList to AvantData
upsert = avantpy.upload.UpsertBulk(dataList, baseurl=URL)
upsert.upload()

"""
INFO:avantpy.download.JSON:Reading https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
INFO:avantpy.download.JSON:<Response [200]> with 730KB. 857 dictionaries added to data attribute
INFO:avantpy.upload.Template:Uploading template testing_json
INFO:avantpy.upload.Template:{"acknowledged":true}
INFO:avantpy.upload.UpsertBulk:Total: 857
INFO:avantpy.upload.UpsertBulk:Updated: 0, Created 857. 
INFO:avantpy.upload.UpsertBulk:857 successfully executed with 0 failures
INFO:avantpy.upload.UpsertBulk:Created: 857 / Updated: 0 / Failed: 0
"""