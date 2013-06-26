import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from cloudydict import common


class RemoteObject(common.RemoteObject):
    def __init__(self, key):
        self.key = key
        self.value = None

    def as_string(self):
        if self.value is None:
            self.value = self.key.get_contents_as_string()
        return self.value


class CloudyDict(common.DictsLittleHelper):
    def __init__(self, **kwargs):
        self.connection = S3Connection(*self.connection_args, **self.connection_kwargs)
        try:
            self.bucket = self.connection.get_bucket(self.key)
        except boto.exception.S3ResponseError:
            self.bucket = self.connection.create_bucket(self.key)
        for key, value in kwargs.items():
            self[key] = value

    def __setitem__(self, key, value):
        k = Key(self.bucket)
        k.key = key
        k.set_contents_from_string(value)

    def __getitem__(self, k):
        key = self.bucket.get_key(k)
        if key is None:
            raise KeyError(k)
        return RemoteObject(key)

    def __iter__(self):
        for key in self.bucket.list():
            yield key.key

    def __contains__(self, key):
        try:
            self[key]
            return True
        except KeyError:
            return False

    def __delitem__(self, key):
        self.bucket.delete_key(key)
        

def factory(bucket_key, *args, **kwargs):
    class S3Cloudydict(CloudyDict):
        connection_args = args
        connection_kwargs = kwargs 
        key = bucket_key
    return S3Cloudydict


def s3_dict(*args, **kwargs):
    return factory(*args, **kwargs)()

def cloudydict(*args, **kwargs):
    return s3_dict(*args, **kwargs)
