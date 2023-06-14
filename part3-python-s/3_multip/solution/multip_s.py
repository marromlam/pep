#!/usr/bin/env python3

import math
import multiprocessing as mp

def my_sqrt(n):
    return math.sqrt(n)

proc_pool = mp.Pool()
sqrt_array_temp = [proc_pool.apply_async(my_sqrt, (n, )) for n in range(int(1e4))]
sqrt_array = [val.get() for val in sqrt_array_temp]
print(sqrt_array[-1])
