# -*- coding: utf-8 -*-


def generateID(data, **kwargs) -> str:
    """Generates a 32 character hexadecimal hash

    This function generates an md5 hash, ideal to be used as an id when indexing a document to avoid document duplication

    Args:
        data: Input to generate the md5 hash
        dumps: (bool, optional): Force `data` to be a string

    Returns:
        The generated md5 hash
    """
    import hashlib
    if kwargs.get('dumps') or not isinstance(data, str):
        import json
        data = json.dumps(data)
    return hashlib.md5(data.encode('utf-8')).hexdigest()


def filter(data, **kwargs):
    import re
    def mapReplace(value, toReplace):
        if callable(toReplace):
            toReplace = [toReplace]
        if isinstance(toReplace, (tuple,list,set)):
            for mapFunction in toReplace:
                value = mapFunction(value)
        return value
    def regexReplace(value, toReplace):
        if type(toReplace) is dict and value:
            for k,v in toReplace.items():
                value = re.sub(k, v, value)
        return value
    def strictReplace(value, toReplace):
        if type(toReplace) is dict:
            if value in toReplace.keys():
                value = toReplace[value]
        return value
    def priorityDecision(kwarg, item, word):
        for k,v in kwarg.items():
            if word in k:
                if 'map' in k.lower():
                    item = mapReplace(item, v)
                if 'regex' in k.lower():
                    item = regexReplace(item, v)
                if 'replace' in k.lower():
                    item = strictReplace(item, v)
        return item
    if type(data) is dict:
        tDict = dict()
        for key,value in data.items():
            key = priorityDecision(kwargs, key, 'key')
            if isinstance(value, (tuple,list,set,dict)):
                tDict[key] = filter(value, **kwargs)
            else:
                value = priorityDecision(kwargs, value, 'value')
                if value is not None:
                    tDict[key] = value
        return tDict
    elif isinstance(data, (tuple,list,set)):
        tList = list()
        for item in data:
            if isinstance(item, (tuple,list,set,dict)):
                tList.append(filter(item, **kwargs))
            else:
                item = priorityDecision(kwargs, item, 'value')
                if item is not None:
                    tList.append(item)
        if type(data) is tuple:
            return tuple(tList)
        elif type(data) is set:
            return set(tList)
        return tList


def thread(method, **kwargs):
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=kwargs.get('workers', 1)) as executor:
        executor.map(method, kwargs.get('chunks'))

def camelCase(s):
    import re
    if s:
        s = re.sub(r'(_|-)+', ' ', str(s)).title().replace(' ', '')
        return ''.join([s[0].lower(), s[1:]])
    return s

def removeEmpty(s):
    if type(s) is bool:
        return s
    if s:
        return s
    return None

""" def removeEmpty(data, **kwargs):
    Remove all empty values inside lists, tuples, sets or dictionaries

    Remove everything that is empty from lists, tuples, sets or dictionaries

    Args:
        data: List, set, tuple or dict with empty values to be removed
        all: (bool, optional): Remove empty and False values from `data`

    Returns:
        The returned `data` with empty values removed
    
    if isinstance(data, (tuple,list,set)):
        tList = list()
        for i in data:
            if type(i) is bool and not kwargs.get('all'):
                tList.append(i)
            else:
                if i:
                    if isinstance(i, (tuple,list,set,dict)):
                        tList.append(removeEmpty(i,**kwargs))
                    else:
                        tList.append(i)
        if type(data) is list:
            return tList
        if type(data) is tuple:
            return tuple(tList)
        if type(data) is set:
            return set(tList)
    if type(data) is dict:
        tDict = dict()
        for k,v in data.items():
            if type(v) is bool and not kwargs.get('all'):
                tDict[k] = v
            else:
                if v:
                    if isinstance(v, (tuple,list,set,dict)):
                        tDict[k] = removeEmpty(v,**kwargs)
                    else:
                        tDict[k] = v
        return tDict """


def flatten(lists: list) -> list:
    """Flatten all elements in a list

    Flatten all lists within a list to prepare it for indexing

    Args:
        lists: (:obj:`list` of :obj:`list`): Lists to be flattened 

    Returns:
        The flattened list
    """
    return [l for ls in lists for l in ls]


def add(lst, **kwargs) -> list:
    newLst = list()
    for l in lst:
        newDict = dict()
        for kwarg in kwargs:
            argument = kwargs.get(kwarg)
            if callable(argument):
                value = argument(l)
            else:
                value = argument
            newDict[kwarg] = value
        newDict.update({k:v for k,v in l.items()})
        newLst.append(newDict)
    return newLst


""" def camelCase(lst) -> list:
    from re import sub
    newLst = []
    for l in lst:
        newDict = dict
        for k,v in l.items():
            k = sub('[^\d\W]+', ' ', k).title().replace(' ', '')
            newDict[''.join([k[0].lower(), k[1:]])] = v
        newLst.append(newDict)
    return newLst """




"""
def filter(data, **kwargs):
    if type(data) is dict:
        tDict = dict()
        for key,value in data.items():
            keysMap = kwargs.get('keysMap')
            if callable(keysMap):
                keysMap = [keysMap]
            if isinstance(keysMap, (tuple,list,set)):
                for mapFunction in keysMap:
                    if callable(mapFunction):
                        key = mapFunction(key)
            keysReplace = kwargs.get('keysReplace')
            if type(keysReplace) is dict:
                if key in keysReplace.keys():
                    key = keysReplace[key]
            if isinstance(value, (tuple,list,set,dict)):
                tDict[key] = filter(value, **kwargs)
            else:
                valuesMap = kwargs.get('valuesMap')
                if callable(valuesMap):
                    valuesMap = [valuesMap]
                if isinstance(valuesMap, (tuple,list,set)):
                    for mapFunction in valuesMap:
                        if callable(mapFunction):
                            value = mapFunction(value)
                valuesReplace = kwargs.get('valuesReplace')
                if type(valuesReplace) is dict:
                    if value in valuesReplace.keys():
                        value = valuesReplace[value]
                tDict[key] = value
        return tDict
    elif isinstance(data, (tuple,list,set)):
        tList = list()
        for item in data:
            if isinstance(item, (tuple,list,set,dict)):
                tList.append(filter(item, **kwargs))
            else:
                valuesMap = kwargs.get('valuesMap')
                if callable(valuesMap):
                    valuesMap = [valuesMap]
                if isinstance(valuesMap, (tuple,list,set)):
                    for mapFunction in valuesMap:
                        if callable(mapFunction):
                            item = mapFunction(item)
                valuesReplace = kwargs.get('valuesReplace')
                if type(valuesReplace) is dict:
                    if item in valuesReplace.keys():
                        item = valuesReplace[item]
                tList.append(item)
        if type(data) is tuple:
            return tuple(tList)
        elif type(data) is set:
            return set(tList)
        return tList
"""