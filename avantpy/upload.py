# -*- coding: utf-8 -*-

""" def uploadToIndex(self, **kwargs):
    chunk = kwargs.get('chunk', 1000)
    clusterToIndex = kwargs.get('clusterToIndex', 'AvantData')
    debugToIndex = kwargs.get('debugToIndex', 'False')
    url = kwargs.get('url', '')
    import requests
    import json
    jsonToSend = {'body': chunk}
    headers = {"cluster": clusterToIndex, "debug": debugToIndex}
    responseBulk = requests.put(url=url+self.urlUpsertBulk, headers=headers,
                                data=json.dumps(jsonToSend), verify=self.verifySSL)
    try:
        responseJson = json.loads(responseBulk.text)
        if self.debug(responseJson, 'items'):
            successful, failed = (0, 0)
            for item in self.debug(responseJson, 'items'):
                try:
                    successful += self.debug(item, 'update>_shards>successful')
                    failed += self.debug(item, 'update>_shards>failed')
                except:
                    failed += 1
                    print(self.debug(item, 'update>error'))
            if successful + failed > 0:
                print('Successful:', successful, '/ Failed:', failed)
                self.indexed += successful
    except Exception as e:
        print(responseBulk.text, '\n', e)
 """