from cloudydict.s3 import factory 

d = factory('wnyc.org-adeprince-dictcloud-test2') 
d = d()
d['a'] = '3'
d.setdefault('b', '4')
print d['a'].tell()
print str(d['a'])
print d['a'].strip()
print str(d['a'])
print d.keys()
print d.values()
print d.items()
print dir(d['a'])
print d['a'].size
del(d['a'])
print 'a' in d
