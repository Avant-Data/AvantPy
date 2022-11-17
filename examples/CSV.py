""" Downloading a CSV from MITRE, creating a template and sending CSV data to avantdata"""
import avantpy
import logging
import json
logging.basicConfig(level=logging.INFO)

URL = 'https://cve.mitre.org/data/downloads/allitems.csv'
URL = 'file:///home/avantwks23/Projetos/AvantPy/.github/workflows/allitems.csv'


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
#print(json.dumps(dataList[400:500], indent=4))

template = avantpy.upload.Template(name='testing_csv',
                                   template=dataList,
                                   baseurl='https://avantshow.avantdata.com.br',
                                   regenerate=True if dataList else False)

print(json.dumps(template.getTemplateDict(dataList), indent=4))
#template.upload()
#jsonized = json.dumps(dataList[:10], indent=4)
# template.upload()
