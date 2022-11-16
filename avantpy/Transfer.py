from . import download
from . import utils
from . import upload
from typing import Any


class Transfer():
    """Transfer Downloader and Uploader

    A class to download and upload data to avantdata

    Args:
        **kwargs (any): Arguments to be passed to Template, UpsertBulk and some other classes

    Attributes:
        name (str): name of the template
        type (str): type to be passed to UpsertBulk (will be the same as `name` if None)
        index (str): index to be passed to UpsertBulk (will be the same as `name` if None)
        data (list(dict)): List of dictionaries to be indexed [{"key1":..., "key2":..., "key3":..., ...},...]
        json (dict): json to be downloaded in case data is not passed

    Examples:
        >>> from avantpy import Transfer
        >>> import logging
        >>> logging.basicConfig(level=logging.INFO)
        >>> Transfer(data=[{'key1': 'test', 'key2': 'test'},{'key3': 'test'}], name='data_transfer_test', baseurl='https://avantshow.avantdata.com.br')
        INFO:avantpy.upload.Template:Uploading template data_transfer_test
        INFO:avantpy.upload.Template:{"acknowledged":true}
        INFO:avantpy.upload.UpsertBulk:Total: 2
        INFO:avantpy.upload.UpsertBulk:Updated: 0, Created: 2. 
        INFO:avantpy.upload.UpsertBulk:2 successfully executed with 0 failures
        INFO:avantpy.upload.UpsertBulk:Created: 2 / Updated: 0 / Failed: 0
        Transfer executed with 2 documents
    """

    def __init__(self, **kwargs: Any):
        self.name = kwargs.get('name')
        self.type = kwargs.get('type', self.name)
        self.index = kwargs.get('index', self.name)
        self.json = kwargs.get('json')
        self.data = kwargs.get('data', list())
        self.transfer(**kwargs)

    def __repr__(self):
        return 'Transfer executed with {} documents'.format(len(self.data))

    def transfer(self, **kwargs):
        """transfer method that is executed within the class call"""
        if self.json:
            self.data = download.JSON(request=self.json, **kwargs).data
        self.template = kwargs.pop('template', self.data)
        template = upload.Template(#name=self.name,
                        template=self.template,
                        **kwargs
                        )
        template.upload()
        self.data = utils.edit(self.data,
                               keys={
                                   'id': '{}ID'.format(self.name),
                                   'type': '{}type'.format(self.name),
                                   'index': '{}index'.format(self.name),
                               })
        self.data = utils.add(self.data,
                              type=self.type,
                              index=self.index,
                              id=utils.generateID
                              )
        kwargs.pop('data', None)
        upsert = upload.UpsertBulk(self.data, **kwargs)
        upsert.upload()
