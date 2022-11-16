from . import download
from . import utils
from . import upload


class Transfer():

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.type = kwargs.get('type', self.name)
        self.index = kwargs.get('index', self.name)
        self.json = kwargs.get('json')
        self.data = kwargs.get('data', list())
        self.transfer(**kwargs)

    def transfer(self, **kwargs):
        if self.json:
            self.data = download.JSON(url=self.json, **kwargs).data
        self.template = kwargs.pop('template', self.data)
        upload.Template(#name=self.name,
                        template=self.template,
                        **kwargs
                        )
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
        upload.UpsertBulk(self.data, **kwargs)
