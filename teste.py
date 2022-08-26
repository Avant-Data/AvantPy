from time import perf_counter
import avantpy

#url = 'https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv'
url = 'file:///home/avantwks23/Projetos/AvantPy/.github/workflows/service-names-port-numbers.csv'
#url = 'file:///home/kalish/projects/avantdata/AvantPy/.github/workflows/service-names-port-numbers.csv'
ianaList = avantpy.download.CSV(url).list
for i in range(5): print(ianaList[i])

starTime = perf_counter()
ianaList = avantpy.utils.filter(ianaList,
                                keysMap=avantpy.utils.camelCase,
                                valuesMap=avantpy.utils.removeEmpty,
                                valuesRegex={
                                    '[\[\]]': '',
                                    '_': ' '
                                },
                                #threads=100
                                )
""" avantpy.upload.Template(name='iana_teste',
                        template=ianaList,
                        baseurl='https://avantnightly.avantsec.com.br/'
                       ) """
ianaList = avantpy.utils.add(ianaList,
                             type='iana',
                             index='iana',
                             id=avantpy.utils.generateID,
                             # threads=10
                             )
#avantpy.upload.UpserBulk(ianaList)
for i in range(5): print(ianaList[i])

endTime = perf_counter()
print(endTime-starTime, 'seconds elapsed')
