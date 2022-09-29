import avantpy
import logging
logging.basicConfig(level=logging.INFO)

#testJ = avantpy.download.JSON('https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json', select='vulnerabilities')
#print(testJ)
s = avantpy.download.Search('https://prod.avantdata.com.br', index='ZoneH', format=True)
print(s.data)
""" dataList = []
dataList.append({'id':'6fee099da7dfbb67599d7fa7389de898', 'type':'test', 'index':'test', 'testKey': 'firstValue'})
dataList.append({'id':'58f77dcc14a41b2984e298e86db85c73', 'type':'test', 'index':'test', 'testKey': 'secondValue'})
dataList.append({'id':'ed23fa12819a63198b5c0b171ebbbf2d', 'type':'test', 'index':'test', 'testKey': 'thirdValue'})
avantpy.upload.UpsertBulk(dataList, baseurl='https://192.168.102.133/') """