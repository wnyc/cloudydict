import boto
from boto.s3.connection import S3Connection
from boto.s3.lifecycle import Lifecycle, Transition, Rule
from boto.s3.key import Key
from cloudydict import common
from datetime import datetime, timedelta

class RemoteObject(common.RemoteObject):
    def __init__(self, key, url, bucket=None):
        self.size = key.size
        self.key = key
        self.url = url
        self.bucket = bucket
        self.value = None

    @property
    def last_modified(self):
        return self.key.last_modified

    def as_string(self):
        if self.value is None:
            self.value = self.key.get_contents_as_string()
        return self.value

    def make_public(self):
        self.key.make_public()
        self.key.set_acl('public-read')

    def thaw(self, time):
        if isinstance(time, datetime):
            time = time - datetime.now()
        if isinstance(time, timedelta):
            time = time.days
        self.key.restore(days=time)

    def freeze(self, time=0):
        if time and isinstance(time, timedelta):
            time += timedelta(hours=12)
            transition = Transition(days=time.days, storage_class='GLACIER')
        elif time and isinstance(time, datetime):
            transition = Transition(days=(time-datetime.now()).days, storage_class='GLACIER')
        else:
            transition = Transition(days=time, storage_class='GLACIER')

        key = self.key.key
        rule = Rule(key, key, 'Enabled', transition=transition)

        lifecycle = Lifecycle()
        lifecycle.append(rule)
        self.bucket.configure_lifecycle(lifecycle)

    def is_frozen(self):
        self.key.storage_class == 'GLACIER'

    def is_thawing(self):
        self.key.ongoing_restore
        
        

class CloudyDict(common.DictsLittleHelper):
    def __init__(self, **kwargs):
        self.connection = S3Connection(*self.connection_args, **self.connection_kwargs)
        try:
            self.bucket = self.connection.get_bucket(self.key)
            self.host = self.bucket.get_website_endpoint()
        except boto.exception.S3ResponseError:
            self.bucket = self.connection.create_bucket(self.key)
        for key, value in kwargs.items():
            self[key] = value

    def __setitem__(self, key, value):
        if isinstance(value, RemoteObject):
            self.bucket.copy_key(key, value.bucket.name, value.key.name)
            return 
        k = Key(self.bucket)
        k.key = key
        k.set_contents_from_string(value)

    def __getitem__(self, k):
        key = self.bucket.get_key(k)
        if key is None:
            raise KeyError(k)
        return RemoteObject(key,  self.host + "/" + key.key, self.bucket)

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

    def make_public(self):
        return self.bucket.make_public(recursive=True)



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
