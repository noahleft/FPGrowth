#!/usr/local/bin/pypy

def memory_usage_ps():
  import subprocess,os
  out = subprocess.Popen(['ps', 'v', '-p', str(os.getpid())],
  stdout=subprocess.PIPE).communicate()[0].split(b'\n')
  vsz_index = out[0].split().index(b'RSS')
  mem = float(out[1].split()[vsz_index])
  return mem

