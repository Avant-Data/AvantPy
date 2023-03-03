from avantpy import utils

def test_generateID():
    assert utils.generateID(
        'Generate ID with MD5 hash text') == '3b3331b428cc68278b975d0d177b9948'

def test_remove_empty():
    assert utils.remove_empty('') == None

def test_flatten():
    assert utils.flatten([[],[],[],[]]) == []

def test_edit():
    data = [{'name': 'John', 'age': 30}, {'name': 'Jane', 'age': 25}]
    keys = {'name': 'firstName'}
    values = {'John': 'Jonathan'}
    items = {'age': lambda x: x + 1}
    expected_output = [{'firstName': 'Jonathan', 'age': 31}, {'firstName': 'Jane', 'age': 26}]
    assert utils.edit(data, keys, values, items) == expected_output

def test_human_size():
    assert utils.human_size(0) == '0 bytes'
    assert utils.human_size(1023) == '1023 bytes'
    assert utils.human_size(1024) == '1KB'
    assert utils.human_size(1048576) == '1MB'
    assert utils.human_size(1099511627776) == '1TB'