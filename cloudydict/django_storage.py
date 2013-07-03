from django.core.files.storage import Storage as _Storage
from cloudydict import cloudydict
from django.conf import settings

class Storage(_Storage):
    def __init__(self, bucket, *args, **kwargs):
        self.dict = cloudydict(bucket, *args, **kwargs)

    def _open(self, name):
        return self.dict[name]

    def delete(self, name):
        del(self.dict[name])

    def exists(self, name):
        return name in self.dict

    def listdir(self, name):
        raise NotImplemented()

    def _save(self, name, content):
        self.dict[name] = content.file.read()
        k = self.dict[name]
        k.make_public()

    def size(self, name):
        self[name].size

    def url(self, name):
        self[name].url
