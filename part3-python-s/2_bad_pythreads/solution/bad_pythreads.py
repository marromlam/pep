#!/usr/bin/env python

import threading

NUM_THREADS = 10
x = 0
threads = [None] * NUM_THREADS

def we_are_adding(id):
  global x
  
  for i in xrange(0,1000000):
    x = x + 1
    
  print "I'm thread %d and x for me is %d" % (id, x)


for i in range(0,NUM_THREADS):
  threads[i] = threading.Thread(target=we_are_adding, args=(i,))
  threads[i].start()

for i in range(0,NUM_THREADS):
  threads[i].join()

print "I'm the main thread and x for me is %d" % x
