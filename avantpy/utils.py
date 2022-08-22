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


def removeEmpty(data, **kwargs):
    """Remove all empty values inside lists, tuples, sets or dictionaries

    Remove everything that is empty from lists, tuples, sets or dictionaries

    Args:
        data: List, set, tuple or dict with empty values to be removed
        all: (bool, optional): Remove empty and False values from `data`

    Returns:
        The returned `data` with empty values removed
    """
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
        return tDict


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
    newLst = []
    for l in lst:
        newDict = dict()
        for kwarg in kwargs:
            newDict[kwarg] = kwargs.get(kwarg)
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