import avantpy

baseurl = 'https://docs.microsoft.com'
api = r'/api/contentbrowser/search/lifecycles?locale=en-us&facet=products&%24orderBy=start%20desc&%24top=10'
allLists = []


def loopRequests(api):
    jsonR = avantpy.download.JSON(baseurl+api).data
    allLists.extend(jsonR.get('results'))
    """ if '@nextLink' in jsonR.keys():
        loopRequests(jsonR.get('@nextLink')) """


loopRequests(api)
allLists = avantpy.utils.edit(allLists,
                              keys=avantpy.utils.camelCase,
                              values=avantpy.utils.removeEmpty,
                              entire={
                                'lastModified': avantpy.utils.dateToEpochMillis,
                                'start': avantpy.utils.dateToEpochMillis,
                                'end': avantpy.utils.dateToEpochMillis,
                                'url': {r'(/.*)': baseurl+r'\g<1>'}
                              })

avantpy.upload.Template(name='microsoft_end_of_life',
                        aliases='TWI',
                        template=allLists,
                        baseurl='https://prod.avantdata.com.br/',
                        typeMap={
                            'start': 'date',
                            'end': 'date',
                            'lastModified': 'date'
                        }
                        )
print(allLists)

""" allLists = avantpy.utils.add(allLists,
                             type='microsoft_end_of_life',
                             index='microsoft_end_of_life',
                             id=avantpy.utils.generateID,
                             )

avantpy.upload.UpsertBulk(allLists,
                          baseurl='https://prod.avantdata.com.br/'
                          ) """