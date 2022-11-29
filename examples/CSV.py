""" Downloading a CSV from MITRE, creating a template and sending CSV data to avantdata"""
import avantpy
import logging
import json
logging.basicConfig(level=logging.INFO)

URL = 'https://cve.mitre.org/data/downloads/allitems.csv'
BASEURL = 'https://avantshow.avantdata.com.br/'
NAME = 'testing_csv'


# Downloads the CSV of CVEs from MITRE, where the keys are at line 3 (start at 2 because 0 is line 1)
cves = avantpy.download.CSV(URL, start=2)
# Jumps 7 lines because line 4 to 10 from the CSV are not data
dataList = cves.data[7:]

# Transforms "References" into a dictionary (in the CSV, the item separator is "   |   " and the key separator is ":")
for i, cve in enumerate(dataList):
    if cve.get('References'):
        dataList[i]['References'] = dict(reference.strip().split(':', 1) for reference in cve.get('References').split('   |   '))

# Remove all empty data
dataList = avantpy.utils.edit(dataList, values=avantpy.utils.removeEmpty)

# Create and upload the template to AvantData, appending data if some other key is added to the CSV in the future
template = avantpy.upload.Template(name=NAME,
                                   template=dataList,
                                   baseurl=BASEURL,
                                   append=True)
template.upload()

# Insert the keys id, type and index in each dictionary of dataList
dataList = avantpy.utils.add(dataList, id=avantpy.utils.generateID, type=NAME, index=NAME)

# Upload dataList to AvantData
upsert = avantpy.upload.UpsertBulk(dataList, baseurl=BASEURL)
upsert.upload()