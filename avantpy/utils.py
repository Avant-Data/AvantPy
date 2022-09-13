# -*- coding: utf-8 -*-
from typing import Callable, Set, Tuple, Union, Optional, List, Dict, Any


def generateID(data: Any) -> str:
    """Generates a 32 character hexadecimal hash, ideal to be used as an id when indexing a document to avoid document duplication

    Args:
        data: Input to generate the md5 hash

    Returns:
        The generated md5 hash
    """
    import hashlib
    if type(data) is not str:
        import json
        data = json.dumps(data)
    return hashlib.md5(data.encode('utf-8')).hexdigest()


def edit(data: Union[List[dict], Tuple[dict], Set[dict]],
         keys: Optional[Union[Callable, dict, list, tuple, set]] = None,
         values: Optional[Union[Callable, dict, list, tuple, set]] = None,
         items: Optional[Dict[Union[str, int, float, bool], Union[str, Callable]]] = {},
         threads: Optional[int] = None
         ) -> Union[List[dict], Tuple[dict], Set[dict]]:
    """Edit a list of dictionaries applying functions or regex in keys and values

    Args:
        data: List of dictionaries to edit
        keys: Functions or dictionaries with format {pattern, replace} to be applied to keys
        values: Functions or dictionaries with format {pattern, replace} to be applied to values
        items: Dictionary with format {key, function or {pattern, replace}} to be applied to values with corresponding keys
        threads: Number of threads to execute list editing

    Returns:
        The edited list
    """
    import re

    def regexReplace(value, toReplace):
        for k, v in toReplace.items():
            value = re.sub(k, v, value)
        return value

    def replaceMap(value, toReplace):
        if callable(toReplace):
            toReplace = [toReplace]
        if isinstance(toReplace, (tuple, list, set)):
            for item in toReplace:
                if callable(item):
                    value = item(value)
                elif type(item) is dict and item and value:
                    value = regexReplace(value, item)
        elif type(toReplace) is dict and toReplace and value:
            value = regexReplace(value, toReplace)
        return value

    if threads:
        return threadList(edit, data, keys, values, items, workers=threads)
    if type(data) is dict:
        tDict = dict()
        for key, value in data.items():
            if keys:
                key = replaceMap(key, keys)
            if isinstance(value, (tuple, list, set, dict)):
                tDict[key] = edit(value, keys, values, items)
            else:
                if values:
                    value = replaceMap(value, values)
                if key in items.keys():
                    value = replaceMap(value, items[key])
                if value is not None:
                    tDict[key] = value
        return tDict
    elif isinstance(data, (tuple, list, set)):
        tList = list()
        for item in data:
            if isinstance(item, (tuple, list, set, dict)):
                tList.append(edit(item, keys, values, items))
            else:
                if values:
                    item = replaceMap(item, values)
                if item is not None:
                    tList.append(item)
        if type(data) is tuple:
            return tuple(tList)
        elif type(data) is set:
            return set(tList)
        return tList


def threadList(method: Callable, data: list, **kwargs):
    """Executes a function in a list with ThreadPoolExecutor

    Args:
        method: Function to execute with ThreadPoolExecutor
        data: List to be broken into several lists
        workers: Number of threads
        chunks: Number of parts to divide the list

    Returns:
        The list after the function with threads has been executed
    """
    import concurrent.futures
    from functools import partial
    workers = kwargs.pop('workers', 1)
    lists = unflatten(data, kwargs.pop('chunks', workers))
    completeList = list()
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        for result in executor.map(partial(method, **kwargs), lists):
            completeList.extend(result)
        return completeList


def humanSize(bytes, units=[' bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']):
    """ Returns a human readable string representation of bytes """
    return str(bytes) + units[0] if bytes < 1024 else humanSize(bytes >> 10, units[1:])


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
    pace = max(1, len(lst)//chunks)
    return [lst[i:i+pace] for i in range(0, len(lst), pace)]


def getData(dic, *args):
    for data in args:
        if data:
            dic = dic.get(data)
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
        newDict.update({k: v for k, v in l.items()})
        newLst.append(newDict)
    return newLst
