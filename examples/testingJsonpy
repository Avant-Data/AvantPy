import avantpy
import logging
logging.basicConfig(level=logging.INFO)

NAME = 'testingjson'
ALIASES = 'testingJson'
URL = 'https://avantnightly.avantsec.com.br'

dataList = avantpy.download.JSON(request='https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json',
                                 select='vulnerabilities').data

avantpy.upload.Template(name=NAME,
                        template=dataList,
                        aliases=ALIASES,
                        baseurl=URL)

dataList = avantpy.utils.add(dataList,
                id=avantpy.utils.generateID,
                type=NAME,
                
                index=NAME)
avantpy.upload.UpsertBulk(dataList, baseurl=URL)
