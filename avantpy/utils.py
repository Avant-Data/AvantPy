# -*- coding: utf-8 -*-

class Utils:
    
    def __init__(self, *args, **kwargs):
        super(Utils, self).__init__(*args, **kwargs)

    def generateID(self, data):
        import hashlib
        return hashlib.md5(data.encode('utf-8')).hexdigest()

    def distributionChecker(self, distribution):
        from pkg_resources import WorkingSet, DistributionNotFound
        try:
            return WorkingSet().require(distribution)
        except DistributionNotFound as e:
            return e

    def flatten(self, lists):
        return [l for ls in [i for i in lists if i] for l in ls]
    
    def removeEmpty(self, obj):
        return {k:v for k,v in obj.items() if v}
    
    def doThreading(self, function, argsList, threadingCount):
        from threading import Thread
        for t in range(len(argsList)//threadingCount+1):
            threadList = []
            for a in range(t*threadingCount,(t+1)*threadingCount):
                if len(argsList) > a:
                    thread = Thread(target=function, args=(argsList[a],))
                    threadList.append(thread)
                    thread.start()
                else:
                    break
            for threads in threadList:
                threads.join()


    #Construindo

    def uploadToIndex(self, **kwargs):
        chunk = kwargs.get('chunk', 1000)
        clusterToIndex = kwargs.get('clusterToIndex', 'AvantData')
        debugToIndex = kwargs.get('debugToIndex', 'False')
        url = kwargs.get('url', '')
        import requests
        import json
        jsonToSend = {'body': chunk}     
        headers = {"cluster": clusterToIndex, "debug": debugToIndex}
        responseBulk = requests.put(url=url+self.urlUpsertBulk, headers=headers, data=json.dumps(jsonToSend), verify=self.verifySSL)
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
                    print('Successful:', successful ,'/ Failed:', failed)
                    self.indexed += successful
        except Exception as e:
            print(responseBulk.text,'\n',e)