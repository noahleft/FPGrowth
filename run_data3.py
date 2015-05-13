#!/usr/local/bin/pypy
import time

start = time.clock()
from FPGrowth.FPGrowth import FPGrowth
from mem_moniter import memory_usage_ps

print('start',memory_usage_ps())

dataset3=FPGrowth('data/dataset3.data.tra',100)
dataset3.process()

end = time.clock()
sec = '%.3f' %(end-start)
print('time elapse:',sec)
print('end',memory_usage_ps())
