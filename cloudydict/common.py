from StringIO import StringIO 

class RemoteObject:
    string_io = None
    underscores = 'add contains eq format ge getitem getslice gt hash le len lt mod mul ne reduce reduce_ex rmod rmul str unicode'.split()
    underscores = ["__%s__" % s for s in underscores]
    stringnames = 'capitalize center count decode encode endswith expandtabs find format index isalnum isalpha isdigit islower isspace istitle issuper join ljust lower lstrip partition replace rfind rindex rjust rpartition rsplit rstrip split splitlines startswith strip swapcase title translate upper zfill'.split()
    stringnames = set(underscores + stringnames)
    filenames = '__iter__ close isatty next read readline readlines seek tell'.split()

    def as_file(self):
        if self.string_io is None:
            self.string_io = StringIO(self.as_string())
        return self.string_io


    def __getattr__(self, key, *kwargs):
        try:
            return object.__getattr__(self, key)
        except AttributeError:
            if key in self.stringnames:
                return getattr(self.as_string(), key)
            if key in self.filenames:
                return getattr(self.as_file(), key)
            if kwargs:
                return kwargs[0]
            raise AttributeError(key)


class DictsLittleHelper:
    
    def values(self):
        return list(self.itervalues())

    def keys(self):
        return list(iter(self))

    def itervalues(self):
        for key in self.iterkeys():
            yield self[key]

    def iterkeys(self):
        for key in iter(self):
            yield key 
    
    def iteritems(self):
        for key in iter(self):
            yield key, self[key]

    def viewvalues(self):
        for key in self.iterkeys():
            yield self[key]

    def viewkeys(self):
        for key in iter(self):
            yield key 
    
    def viewitems(self):
        for key in iter(self):
            yield key, self[key]

    def items(self):
        return list(self.iteritems())

    def has_key(self, key):
        return key in self

    def get(self, key, default=None):
        if key in self:
            return self[key]
        return default

    def pop(self, k, *args):
        if len(args) not in (0, 1):
            raise TypeError('Zero or one default value parameters')
        if k in self:
            return self[k]
        if args:
            return args[0]
        raise KeyError(k)

    def update(self, *d, **kwargs):
        if len(d) not in (0, 1):
            raise TypeError('Update expected at most 1 parameter, %d provided' % len(*d))
        if len(d):
            d = d[0]
            if hasattr(d, 'keys'):
                for k in d.keys():
                    self[k] = d[k]
            else:
                for k, v in d:
                    self[k] = v
        for k, v in kwargs.iteritems():
            self[k] = v

    def setdefault(self, k, v):
        if k in self:
            return self[k]
        self[k] = v
        return v

    
            
