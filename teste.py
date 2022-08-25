import avantpy

#url = 'https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv'
url = 'file:///home/avantwks23/Projetos/AvantPy/.github/workflows/service-names-port-numbers.csv'
ianaList = avantpy.download.CSV(url).list
for i in range(5):
    print(ianaList[i])


ianaList = avantpy.utils.filter(ianaList,
                                keysMap=avantpy.utils.camelCase,
                                valuesMap=avantpy.utils.removeEmpty,
                                valuesRegex={
                                    '[\[\]]': '',
                                    '_': ' '
                                    }
                                )
ianaList = avantpy.utils.add(ianaList,
                             type='iana',
                             index='iana',
                             id=avantpy.utils.generateID
                             )
for i in range(1337, 1342):
    print(ianaList[i])