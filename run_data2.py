#!/usr/local/bin/pypy
import time

start = time.clock()
from FPGrowth.FPGrowth import FPGrowth
from mem_moniter import memory_usage_ps

print('start',memory_usage_ps())

dataset2=FPGrowth('data/dataset2.data.tra',6)
dataset2.process()

end = time.clock()
sec = '%.3f' %(end-start)
print('time elapse:',sec)
print('end',memory_usage_ps())
