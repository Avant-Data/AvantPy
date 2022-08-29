from . import download
from . import utils
from . import upload


class Transfer():

    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.type = kwargs.pop('type', self.name)
        self.index = kwargs.pop('index', self.name)
        self.json = kwargs.pop('json')
        self.list = list()
        self.transfer(**kwargs)

    def transfer(self, **kwargs):
        if self.json:
            self.list = download.JSON(url=self.json, **kwargs).list
        self.list = utils.edit(self.list,
                               keysReplace={
                                   'id': '{}ID'.format(self.name),
                                   'type': '{}type'.format(self.name),
                                   'index': '{}index'.format(self.name),
                               })
        self.template = kwargs.pop('template', self.list)
        upload.Template(name=self.name,
                        template=self.template,
                        **kwargs
                        )
        self.list = utils.add(self.list,
                              type=self.type,
                              index=self.index,
                              id=utils.generateID
                              )
        for i in range(5):
            print(self.list[i])
        upload.UpsertBulk(self.list, **kwargs)
