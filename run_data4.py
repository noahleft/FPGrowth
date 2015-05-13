#!/usr/local/bin/pypy
import time

start = time.clock()
from FPGrowth.FPGrowth import FPGrowth
from mem_moniter import memory_usage_ps

print('start',memory_usage_ps())

dataset4=FPGrowth('data/dataset4.data.tra',2000)
dataset4.process()

end = time.clock()
sec = '%.3f' %(end-start)
print('time elapse:',sec)
print('end',memory_usage_ps())
