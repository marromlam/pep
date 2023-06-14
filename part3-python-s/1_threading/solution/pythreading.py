#!/usr/bin/env python

import sys
from threading import Thread

def decrement(n, tid):
  while n>0:
    n -= 1
  print "thread %d result: " % tid, n
      
thread1 = Thread(target=decrement, args=(1e8,1))
thread1.start()
thread2 = Thread(target=decrement, args=(1e8,2))
thread2.start()
thread1.join()
thread2.join()
