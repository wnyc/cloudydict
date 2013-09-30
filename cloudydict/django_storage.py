from django.core.files.storage import Storage as _Storage
from cloudydict import cloudydict
from django.conf import settings


class Storage(_Storage):
    def __init__(self, bucket, *args, **kwargs):
        self.bucket = bucket
        self.dict = cloudydict(bucket, *args, **kwargs)

    def _open(self, name, mode='rb'):
        if 'w' in mode or 'a' in mode:
            raise IOERROR("Permission denied (cannot yet open cloudydict.djang_storage.Storage objects with writable flags)")
        return self.dict[name]

    def delete(self, name):
        del(self.dict[name])

    def exists(self, name):
        return name in self.dict

    def listdir(self, name):
        raise NotImplemented()

    def _save(self, name, content):
        if hasattr(content, 'file'):
            self.dict[name] = content.file.read()
        elif hasattr(content, 'read'):
            self.dict[name] = content.read()
        else:
            self.dict[name] = content
            
        k = self.dict[name]
        k.make_public()

    def size(self, name):
        try:
            self.dict[name].size
        except KeyError:
            return None

    def url(self, name):
        try:
            self.dict[name].url
        except KeyError:
            return None

class StorageFromSettings(Storage):
    def __init__(self):
        Storage.__init__(self, *settings.CLOUDY_DICT_STORAGE_SERVER_OPTIONS)

