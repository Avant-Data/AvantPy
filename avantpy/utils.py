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


def edit(data, **kwargs):
    import re
    def regexReplace(value, toReplace):
        for k,v in toReplace.items():
            value = re.sub(k, v, value)
        return value
    def replaceMap(value, toReplace):
        if callable(toReplace):
            toReplace = [toReplace]
        if isinstance(toReplace, (tuple,list,set)):
            for item in toReplace:
                if callable(item):
                    value = item(value)
                elif type(item) is dict and item and value:
                    value = regexReplace(value, item)
        elif type(toReplace) is dict and toReplace and value:
            value = regexReplace(value, toReplace)
        return value
    threads = kwargs.pop('threads', None)
    keysReplace = kwargs.get('keys')
    valuesReplace = kwargs.get('values')
    entireReplace = kwargs.get('entire', {})
    if threads:
        return threadList(edit, data, **kwargs, workers=threads)
    if type(data) is dict:
        tDict = dict()
        for key,value in data.items():
            if keysReplace:
                key = replaceMap(key, keysReplace)
            if isinstance(value, (tuple,list,set,dict)):
                tDict[key] = edit(value, **kwargs)
            else:
                if valuesReplace:
                    value = replaceMap(value, valuesReplace)
                if key in entireReplace.keys():
                    value = replaceMap(value, entireReplace[key])
                if value is not None:
                    tDict[key] = value
        return tDict
    elif isinstance(data, (tuple,list,set)):
        tList = list()
        for item in data:
            if isinstance(item, (tuple,list,set,dict)):
                tList.append(edit(item, **kwargs))
            else:
                if valuesReplace:
                    item = replaceMap(item, valuesReplace)
                if item is not None:
                    tList.append(item)
        if type(data) is tuple:
            return tuple(tList)
        elif type(data) is set:
            return set(tList)
        return tList


def threadList(method, lst, **kwargs):
    import concurrent.futures
    from functools import partial
    workers = kwargs.pop('workers', 1)
    lists = unflatten(lst, kwargs.pop('chunks', workers))
    completeList = list()
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        for result in executor.map(partial(method,**kwargs), lists):
            completeList.extend(result)
        return completeList

def humanSize(bytes, units=[' bytes','KB','MB','GB','TB', 'PB', 'EB']):
    """ Returns a human readable string representation of bytes """
    return str(bytes) + units[0] if bytes < 1024 else humanSize(bytes>>10, units[1:])

def camelCase(s):
    import re
    if s:
        s = re.sub(r'(_|-)+', ' ', str(s)).title().replace(' ', '')
        return ''.join([s[0].lower(), s[1:]])
    return s

def removeEmpty(s):
    """Return None if a value is empty

    Replace empty values with None

    Args:
        s (str): String to be checked

    Returns:
        The returned `s` with empty values replace by None
    """
    if type(s) is bool:
        return s
    if s:
        return s
    return None


def flatten(lists: list) -> list:
    """Flatten all elements in a list

    Flatten all lists within a list to prepare it for indexing

    Args:
        lists: (:obj:`list` of :obj:`list`): Lists to be flattened 

    Returns:
        The flattened list
    """
    return [l for ls in lists for l in ls]


def unflatten(lst: list, chunks: int) -> list:
    pace = max(1,len(lst)//chunks)
    return [lst[i:i+pace] for i in range(0, len(lst), pace)]


def getObj(dic, *args):    
        for obj in args:
            if obj:
                dic = dic.get(obj)
        return dic


def strToType(s):
    from ast import literal_eval
    try:
        return type(literal_eval(s))
    except Exception:
        return type(s)


def dateToEpochMillis(s: str) -> int:
    if type(s) is str:
        import dateparser
        return int(dateparser.parse(s).strftime('%s'))*1000
    return s


def add(lst, **kwargs) -> list:
    threads = kwargs.pop('threads', None)
    if threads:
        return threadList(add, lst, **kwargs, workers=threads)
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