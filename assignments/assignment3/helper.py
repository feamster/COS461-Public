'''
Helper module for the plot scripts.
'''

import re
import itertools
import matplotlib as m
import os
if os.uname()[0] == "Darwin":
    m.use("MacOSX")
else:
    m.use("Agg")
import matplotlib.pyplot as plt
import argparse
import math
#import termcolor as T

def read_list(fname, delim=','):
    lines = open(fname).xreadlines()
    ret = []
    for l in lines:
        ls = l.strip().split(delim)
        ls = map(lambda e: '0' if e.strip() == '' or e.strip() == 'ms' or e.strip() == 's' else e, ls)
        ret.append(ls)
    return ret

def ewma(alpha, values):
    if alpha == 0:
        return values
    ret = []
    prev = 0
    for v in values:
        prev = alpha * prev + (1 - alpha) * v
        ret.append(prev)
    return ret

def col(n, obj = None, clean = lambda e: e):
    """A versatile column extractor.

    col(n, [1,2,3]) => returns the nth value in the list
    col(n, [ [...], [...], ... ] => returns the nth column in this matrix
    col('blah', { ... }) => returns the blah-th value in the dict
    col(n) => partial function, useful in maps
    """
    if obj == None:
        def f(item):
            return clean(item[n])
        return f
    if type(obj) == type([]):
        if len(obj) > 0 and (type(obj[0]) == type([]) or type(obj[0]) == type({})):
            return map(col(n, clean=clean), obj)
    if type(obj) == type([]) or type(obj) == type({}):
        try:
            return clean(obj[n])
        except:
            #print T.colored('col(...): column "%s" not found!' % (n), 'red')
            return None
    # We wouldn't know what to do here, so just return None
    #print T.colored('col(...): column "%s" not found!' % (n), 'red')
    return None

def transpose(l):
    return zip(*l)

def avg(lst):
    return sum(map(float, lst)) / len(lst)

def stdev(lst):
    mean = avg(lst)
    var = avg(map(lambda e: (e - mean)**2, lst))
    return math.sqrt(var)

def xaxis(values, limit):
    l = len(values)
    return zip(*map(lambda (x,y): (x*1.0*limit/l, y), enumerate(values)))

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)

def cdf(values):
    values.sort()
    prob = 0
    l = len(values)
    x, y = [], []

    for v in values:
        prob += 1.0 / l
        x.append(v)
        y.append(prob)

    return (x, y)

def parse_cpu_usage(fname, nprocessors=8):
    """Returns (user,system,nice,iowait,hirq,sirq,steal) tuples
	aggregated over all processors.  DOES NOT RETURN IDLE times."""

    data = grouper(nprocessors, open(fname).readlines())

    """Typical line looks like:
    Cpu0  :  0.0%us,  1.0%sy,  0.0%ni, 97.0%id,  0.0%wa,  0.0%hi,  2.0%si,  0.0%st
    """
    ret = [] 
    for collection in data:
        total = [0]*8
        for cpu in collection:
          usages = cpu.split(':')[1]
          usages = map(lambda e: e.split('%')[0],
                       usages.split(','))
          for i in xrange(len(usages)):
              total[i] += float(usages[i])
        total = map(lambda t: t/nprocessors, total)
		# Skip idle time
        ret.append(total[0:3] + total[4:])
    return ret

def pc95(lst):
    l = len(lst)
    return sorted(lst)[ int(0.95 * l) ]

def pc99(lst):
    l = len(lst)
    return sorted(lst)[ int(0.99 * l) ]

def coeff_variation(lst):
    return stdev(lst) / avg(lst)

