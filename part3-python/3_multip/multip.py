#!/usr/bin/env python

import math
import multiprocessing as mp

def my_sqrt(n):
    return math.sqrt(n)

proc_pool = mp.Pool()
sqrt_array = proc_pool.map(my_sqrt, range(int(1e7)))
print sqrt_array[-1]
