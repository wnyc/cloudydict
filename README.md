cloudydict
==========

![alt text](/cloud.jpg)

Cloudydict is a cross vendor compatibility layer that makes all cloud
file services look as much like a python dict as possible.

Use cloudydict instead of boto or cloudfiles and enjoy simple
dictionary based access to your files.

Installation
------------

Its on Pypi.  Just run this:

    $ pip install --upgrade cloudydict

Tutorial
--------

You might want to take a look at cloudydict's homepage: http://wnyc.github.io/cloudydict/

Manifesto
---------

Python dicts are awesome.  The cloud is awesome.  So why do the python
APIs for these services suck so much?

The intuitive API to retrieve something with boto from S3 should be:

    cloud = S3Connection().get_bucket(<my_bucket>)
    value = cloud[<my key>]

So why is it boto requres I say: 

    cloud = S3Connection().get_bucket(<my_bucket>)
    key = cloud.get_key(<key>)
    value = key.get_contents_as_string()

Similarly why does Rackspace require I say: 

    cloud = cloudfiles.get_connection().get_container(<my_bucket>)
    obj = cloud.get_object(<key>)
    value = obj.read()

Testing for membership is equally cumbersome.  In python I might write: 

    if key in cloud

Boto requires I write:

    if cloud.get_key(<key>) is None:

Cloudfiles requires I write: 

    try:
      cloud.get_object(<key>)
    except NoSuchObject:
      pass

Cloud files are a dictionary.  They should act like one.  Cloudydict fixes that. 

Tutorial
--------

This tutorial assumes you are using Amazon S3 and have already setup your .boto configuration file. 

Normally when you create a dictionary in python it suffices to say: 

    a = dict() 


In cloudydict you need to provide one more piece of information.  The name of your bucket in which you store your key/value pairs. 

    from cloudydict.s3 import factory
    my_dict_class = factory(<my bucket name>) 

`my_dict_class` is analogous to the `dict` function in python.  It
isn't the dictionary itself but rather a constructor to it.  It is
more or less compatible with dict; saying this:

    d = my_dict_class(a='1', b='2')

will add the files `a` and `b` to your bucket; these will hold files
with the contents of `1` and `2` respectively.

Cloudydict differs somewhat from python's `dict` in one regard:
instances of python's `dict` are private.  Cloudydict instances
associated with the same bucket are shares, so a second object like
this:

    e = my_dict_class(c='3')

will be able to see a and b.  

We can test for set membership in cloudydict:

    'c' in d # should be true
    'q' in d # should be false

We can add values:

   d['d'] = 'foobar'

We can remove values:

   del(d['a'])

We can list values:

    print d.items()

And we can retrieve items

    print d['a']

You might note that cloudydict does not return a string, but rather an
instance of `cloudydict.common.RemoteObject`.  RemoteObject is a lazy
evaluating proxy that emulates fairly well the behavior of both a
read only file and a string.  It tries to do so fairly efficiently too,
so for example when interacting with back ends that support it, string
slicing will result in HTTP range requests.  Similarly treating the
RemoteObject as a file and calling `readline` repeatedly will result in
streaming behavior.

The "dual duck type" model of RemoteObject does fail for methods that
have different behaviors between implementations.  For example, iter
on a string and file return individual character and lines
respectively.  This is resolved by picking whichever approach is less
accessible by a standard python convention; in the case of iter, the file __iter__ semantics are provided by default.  Those desiring string semantics need to wrap their RemoteObject in a call to str like this: `str(d[<key>])`

Storage into cloudydict is similarly limited.  Three types of data may
be stored in cloudydict: file like objects that have a `read` method,
strings or objects that have sanely when `str(<value>)` is called and
other RemoteObject instances.

When copying values between cloudydict instances never say this:

    d['z'] = str(e['d'])


Instead it is more efficient to pass the 
RemoteObject instance like this:

    d['z'] = e['d']


Cloudydict is aware of some of the special functionality some cloud
vendors offer.  For example, when copying between two S3 backed
dictionaries, cloudy dict can use Amazon's cross bucket copy commands.



