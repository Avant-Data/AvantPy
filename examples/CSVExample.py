from time import perf_counter
import avantpy
import logging
logging.basicConfig(level=logging.INFO)

#url = 'https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv'
url = 'file:///home/avantwks23/Projetos/AvantPy/.github/workflows/service-names-port-numbers.csv'
#url = 'file:///home/kalish/projects/avantdata/AvantPy/.github/workflows/service-names-port-numbers.csv'
ianaList = avantpy.download.CSV(url).data
for i in range(5):
    print(ianaList[i])

starTime = perf_counter()
ianaList = avantpy.utils.edit(ianaList,
                              keys=avantpy.utils.camelCase,
                              values=[
                                  avantpy.utils.removeEmpty,
                                  {
                                      '[\[\]]': '',
                                      '_': ' '
                                  }]
                              # threads=100
                              )
""" avantpy.upload.Template(name='iana_teste',
                        template=ianaList,
                        aliases='IANA',
                        baseurl='https://192.168.102.133/',
                       ) """
ianaList = avantpy.utils.add(ianaList,
                             type='iana_teste',
                             index='iana_teste',
                             id=avantpy.utils.generateID,
                             # threads=10
                             )
""" avantpy.upload.UpsertBulk(ianaList,
                          baseurl='https://192.168.102.133/',
                          threads=10
                          ) """
for i in range(5):
    print(ianaList[i])

endTime = perf_counter()
print(endTime-starTime, 'seconds elapsed')

