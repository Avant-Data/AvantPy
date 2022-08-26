from time import perf_counter
import avantpy

#url = 'https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv'
#url = 'file:///home/avantwks23/Projetos/AvantPy/.github/workflows/service-names-port-numbers.csv'
url = 'file:///home/kalish/projects/avantdata/AvantPy/.github/workflows/service-names-port-numbers.csv'
ianaList = avantpy.download.CSV(url).list
for i in range(5):
    # print(ianaList[i])
    pass


ianaList = avantpy.utils.filter(ianaList,
                                keysMap=avantpy.utils.camelCase,
                                valuesMap=avantpy.utils.removeEmpty,
                                valuesRegex={
                                    '[\[\]]': '',
                                    '_': ' '
                                },
                                # threads=10
                                )
starTime = perf_counter()
ianaList = avantpy.utils.add(ianaList,
                             type='iana',
                             index='iana',
                             id=avantpy.utils.generateID,
                             # threads=10
                             )
for i in range(5):
    pass  # print(ianaList[i])

endTime = perf_counter()
print(endTime-starTime, 'seconds elapsed')
