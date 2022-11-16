""" A class to upload templates to AvantData with a given list of dictionaries or dictionary"""
from avantpy.upload import Template

template = Template(name='testing_simple_template', template=[{'someKey': 'someValue'}, {'anotherKey': 'anotherValue'}], baseurl='https://192.168.102.133')
template.upload()