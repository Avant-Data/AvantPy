from avantpy import utils

def test_generateID():
    assert utils.generateID(
        'Generate ID with MD5 hash text') == '3b3331b428cc68278b975d0d177b9948'

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

def test_camel_case():
    assert utils.camel_case('hello_world') == 'helloWorld'

def test_remove_empty():
    assert utils.remove_empty('') == None

def test_flatten():
    assert utils.flatten([[],[],[],[]]) == []

def test_unflatten():
    assert utils.unflatten([1, 2, 3, 4, 5, 6], 2) == [[1, 2, 3], [4, 5, 6]]

def test_get_data():
    dic = {"name": "John", "age": 30, "gender": "male", "country": "USA"}
    result = utils.get_data(dic, "name", "age")
    assert result == {"name": "John", "age": 30}

def test_str_to_type():
    assert utils.str_to_type("5") == int
    assert utils.str_to_type("3.14") == float
    assert utils.str_to_type("True") == bool
    assert utils.str_to_type("hello") == str
    assert utils.str_to_type("[1, 2, 3]") == list
    assert utils.str_to_type("{'name': 'John', 'age': 30}") == dict

def test_add():
    lst = [{"name": "Alice"}, {"name": "Bob"}]
    assert utils.add(lst, age=30, city="New York") == [
        {"name": "Alice", "age": 30, "city": "New York"},
        {"name": "Bob", "age": 30, "city": "New York"}
    ]