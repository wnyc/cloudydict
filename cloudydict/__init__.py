import cloudydict.s3
import cloudydict.cloudfiles

_SERVICES = { 's3': cloudydict.s3,
              'cloudfiles': cloudydict.cloudfiles }

def factory(bucket, *args, **kwargs):
    if ':' not in bucket:
        raise ValueError(('Cloudydict bucket selectors are of the form '
                          '"service:bucket name"  %r needs at least one :') % bucket )
    service, bucket = bucket.split(':', 1)
    return _SERVICES[service].factory(bucket, *args, **kwargs)
    

def cloudydict(*args, **kwargs):
    return factory(*args, **kwargs)()
