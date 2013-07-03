import cloudydict.s3
import cloudydict.cloudfiles

_SERVICES = { 's3': cloudydict.s3,
              'cloudfiles': cloudydict.cloudfiles }

def factory(bucket, *args, **kwargs):
    service, bucket = bucket.split(':', 1)
    return _SERVICES[service].factory(bucket, *args, **kwargs)
    

def cloudydict(*args, **kwargs):
    return factory(*args, **kwargs)()
