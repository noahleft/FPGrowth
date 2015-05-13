#!/usr/local/bin/pypy
import time

start = time.clock()
from FPGrowth.FPGrowth import FPGrowth
from mem_moniter import memory_usage_ps

print('start',memory_usage_ps())
dataset1=FPGrowth('data/dataset1.data.tra',10)
dataset1.process()

end = time.clock()
sec = '%.3f' %(end-start)
print('time elapse:',sec)
print('end',memory_usage_ps())
