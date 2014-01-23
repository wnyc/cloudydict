from django.core.files.storage import Storage as _Storage
from cloudydict import cloudydict
from django.conf import settings
from StringIO import StringIO


class Storage(_Storage):
    def __init__(self, bucket, *args, **kwargs):
        self.bucket = bucket
        self.dict = cloudydict(bucket, *args, **kwargs)

    def _open(self, name, mode='rb'):
        if 'w' in mode or 'a' in mode:
            raise IOError("Permission denied (cannot yet open cloudydict.djang_storage.Storage objects with writable flags)")
        try:
            return StringIO(self.dict[name].read())
        except KeyError, e:
            raise IOError(e)

    def modified_time(self, name):
        try:
            return self.dict[name].last_modified
        except AttributeError:
            return None 

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
        return name

    def size(self, name):
        try:
            self.dict[name].size
        except KeyError:
            return None

    def url(self, name):
        try:
            return "http://" + self.dict[name].url
        except KeyError:
            return None


class StorageFromSettings(Storage):
    def __init__(self):
        if hasattr(settings, 'CLOUDYDICT_STORAGE_SERVER_OPTIONS_SECRET'):
            config = settings.CLOUDYDICT_STORAGE_SERVER_OPTIONS_SECRET
        elif hasattr(settings, 'CLOUDY_DICT_STORAGE_SERVER_OPTIONS'):
            import warnings
            warnings.warn('Use of the CLOUDY_DICT_STORAGE_SERVER_OPTIONS settings is unsafe in DEBUG mode.  '
                          'Use CLOUDYDICT_STORAGE_SERVER_OPTIONS_SECRET instead',
                          warnings.DeprecationWarning)
            config = settings.CLOUDY_DICT_STORAGE_SERVER_OPTIONS
        else:
            raise AttributeError('Use of cloudydict.django_storage.StorageFromSettings requires CLOUDYDICT_STORAGE_SERVER_OPTIONS_SECRET in django.conf.settings')        
        Storage.__init__(self, *config)



