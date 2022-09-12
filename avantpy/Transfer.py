from . import download
from . import utils
from . import upload


class Transfer():

    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.type = kwargs.pop('type', self.name)
        self.index = kwargs.pop('index', self.name)
        self.json = kwargs.pop('json')
        self.data = list()
        self.transfer(**kwargs)

    def transfer(self, **kwargs):
        if self.json:
            self.data = download.JSON(url=self.json, **kwargs).data
        self.data = utils.edit(self.data,
                               keys={
                                   'id': '{}ID'.format(self.name),
                                   'type': '{}type'.format(self.name),
                                   'index': '{}index'.format(self.name),
                               })
        self.template = kwargs.pop('template', self.data)
        upload.Template(name=self.name,
                        template=self.template,
                        **kwargs
                        )
        self.data = utils.add(self.data,
                              type=self.type,
                              index=self.index,
                              id=utils.generateID
                              )
        for i in range(5):
            print(self.data[i])
        upload.UpsertBulk(self.data, **kwargs)
