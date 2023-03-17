from typing import Callable, Set, Tuple, Union, Optional, List, Dict, Any


def generateID(data: Any) -> str:
    """Generates a 32 character hexadecimal hash, ideal to beused as an id
    when indexing a document to avoid document duplication

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

def edit(
    data: Union[List[dict], Tuple[dict], Set[dict]],
    keys: Optional[Union[dict, list, tuple, set, Callable]] = None,
    values: Optional[Union[dict, list, tuple, set, Callable]] = None,
    items: Optional[Dict[Union[str, int, float, bool], Union[str,
                                                             Callable]]] = {},
) -> Union[List[dict], Tuple[dict], Set[dict]]:
    """Edit a list of dictionaries applying functions or regex in keys and values

    Args:
        data: List of dictionaries to edit
        keys: Functions or dictionaries with format {pattern, replace} to be applied to keys
        values: Functions or dictionaries with format {pattern, replace} to be applied to values
        items: Dictionary with format {key, function or {pattern, replace}} to be applied to values with corresponding keys
    Returns:
        The edited list
    """
    import re
    def regex_replace(value, toReplace):
        for k, v in toReplace.items():
            value = re.sub(k, v, value)
        return value

    def replace_map(value, toReplace):
        if callable(toReplace):
            toReplace = [toReplace]
        if isinstance(toReplace, (tuple, list, set)):
            for item in toReplace:
                if callable(item):
                    value = item(value)
                elif type(item) is dict and item and isinstance(value, str):
                    value = regex_replace(value, item)
        elif type(toReplace) is dict and toReplace and isinstance(value, str):
            value = regex_replace(value, toReplace)
        return value
    if type(data) is dict:
        tDict = dict()
        for key, value in data.items():
            if keys:
                key = replace_map(key, keys)
            if isinstance(value, (tuple, list, set, dict)):
                tDict[key] = edit(value, keys, values, items)
            else:
                if values:
                    value = replace_map(value, values)
                if key in items.keys():
                    value = replace_map(value, items[key])
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
                    item = replace_map(item, values)
                if item is not None:
                    tList.append(item)
        if type(data) is tuple:
            return tuple(tList)
        elif type(data) is set:
            return set(tList)
        return tList

def get_url(url: str) -> str:
        """This function returns a URL string.
        
        If the `url` argument is not empty, the function simply returns it.
        
        If the `url` argument is empty, the function creates a UDP socket and connects to the IP address and port
        of Google's public DNS server (8.8.8.8 on port 80) to get the IP address of the host. It then formats the IP
        address as a string and returns it with the `https://` protocol prefix.
        
        Args:
            url: string representing the URL that the function will try to retrieve.
        
        Returns:
            str: The URL to use for API requests.
        """
        if not url:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            host_ip = s.getsockname()[0]
            s.close()
            return 'https://{}'.format(host_ip)
        return url


def human_size(
    bytes: int,
    units: Optional[list] = [' bytes', 'KB', 'MB', 'GB', 'TB', 'PB',
                             'EB']) -> str:
    """Returns a human readable string representation of bytes

    Args:
        bytes: Number of bytes to convert to human readable
        units: Suffix list

    Returns:
        The string in plain read format
    """
    return str(bytes) + units[0] if bytes < 1024 else human_size(
        bytes >> 10, units[1:])


def camel_case(s: str) -> str:
    """Puts the string in camelCase format

    Args:
        s: String to be changed

    Returns:
        The string formatted as camelCase
    """
    import re
    if s:
        s = re.sub(r'(_|-)+', ' ', str(s)).title().replace(' ', '')
        return ''.join([s[0].lower(), s[1:]])
    return s


def remove_empty(s: str) -> str:
    """Replace empty values with None

    Args:
        s: String to be checked

    Returns:
        The string with empty values replace by None
    """
    if type(s) is bool:
        return s
    if s:
        return s
    return None

def flatten(lists: List[list]) -> list:
    """Flatten all list elements in a list

    Args:
        lists: Lists to be flattened 

    Returns:
        The flattened list
    """
    return [l for ls in lists for l in ls]


def unflatten(lst: list, chunks: Optional[int] = 1) -> list:
    """Unlatten all list elements in a list

    Args:
        lst: List to be unflattened
        chunks: Number of lists to be inside the list 

    Returns:
        The unflattened list
    """
    unflattened = []
    pace = max(1, len(lst) // chunks)
    surplus = 0
    for i in range(0, len(lst), pace):
        if i + pace + len(lst) % chunks == len(lst):
            surplus = len(lst) % chunks
        unflattened.append(lst[i:i + pace + surplus])
        if surplus > 0:
            break
    return unflattened


def get_data(dic: dict, *args: Optional[Union[str, int, float, bool]]) -> dict:
    """A way to extract only necessary data inside a dictionary

    Args:
        dic: dictionary to have the data extracted
        args: keys inside the dictionary

    Returns:
        Another dictionary with passed keys
    """
    rdic = dict()
    for data in args:
        value = dic.get(data)
        if isinstance(value, dict):
            rdic.update(**value)
        else:
            rdic.update({data: value})
    if rdic:
        return rdic
    return dic

def str_to_type(s: str) -> type:
    """Deduces the data type of a string

    Args:
        s: string to be deducted

    Returns:
        Estimated string type
    """
    from ast import literal_eval
    try:
        return type(literal_eval(s))
    except Exception:
        return type(s)


def date_to_epoch_millis(s: str) -> int:
    """Parses the date and transforms it into epoch millis format

    Args:
        s: string containing the date to be parsed

    Returns:
        Data integer in epoch millis format
    """
    if type(s) is str:
        import dateparser
        try:
            return int(dateparser.parse(s).strftime('%s'))*1000
        except Exception:
            pass
    return s


def add(lst: List[dict], **kwargs: Any) -> list:
    """Add keys and values to each dictionary of a list

    Args:
        lst: list containing dictionaries
        kwargs: keys and values to be added. The values can also be a function to be applied to each dictionary

    Returns:
        The list with added keys and values
    """
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