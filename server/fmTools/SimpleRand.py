# -*- coding: ISO-8859-1 -*-
# fmTools package                          Frank Lübeck / Max Neunhöffer

"""This module provides a very simple but fast random integer generator. Usage:  
r = RandObj([bound][, seed])
while 1:
  x = r.next()
  ...

Here the calls of r.next() give pseudo random integers in the range 0 to
bound-1; the period of the sequence is of length 3**18.

In a threading environment, each thread should call RandObj on its own.

Furthermore, there is a function 

ShuffleList(l[, seed])

that pseudo randomly permutes the entries of a list l in place.
"""

CVS = '$Id: SimpleRand.py,v 1.4 2004/10/07 02:13:52 neunhoef Exp $'

class RandObj:
  """RandObj([bound][, seed])
returns an object that delivers via its .next() method a sequence of pseudo
random integers in the range 0 to bound-1. The integer arguments are optional. 
The default for 'bound' is its maximal possible value 3**18.
Example:
  r = RandObj(5)
  for i in range(10):
    print r.next()+1
for simulating a die 10 times.
"""
  m = 3**18
  a = 4
  c = 217420199
  def __init__(self, bound=3**18, seed=123456):
    self.seed = seed % self.m
    self.bound = bound
  def next(self):
    self.seed = (self.a * self.seed + self.c) % self.m
    return self.seed % self.bound
  # Reuse the following three lines and rename the method thereafter from
  # "nextequaldist" to "nextequaldistfuture" to get the old behaviour
  #def nextequaldist(self,maxval):
  #  # FIXME: Old (buggy) behaviour
  #  return self.next() % maxval
  def nextequaldist(self,maxval):
    # Delivers a pseudo random number in xrange(maxval), equally distributed:
    return int(self.next() * maxval / self.bound)
    # The int tries to make a short int from the result, which is good as
    # long as maxval is small
  def ShuffleList(self,l):
      for k in range(len(l), 0, -1):
        pos = self.nextequaldist(k)
        if pos < k-1:
          t = l[k-1]
          l[k-1] = l[pos]
          l[pos] = t


    
def ShuffleList(l, seed=654321):
  """ShuffleList(l[, seed])
permutes the entries of a list l pseudo randomly in place. An integer
argument 'seed' is optional.
"""
  r = RandObj(seed=seed)
  for k in range(len(l), 0, -1):
    pos = r.next() % k
    if pos < k-1:
      t = l[k-1]
      l[k-1] = l[pos]
      l[pos] = t


    
