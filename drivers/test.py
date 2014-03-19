#!  /usr/bin/env python

from ctypes import *
import os, errno, re, sys, struct
import os.path


def set_ld_library_path():
    libpath = os.getenv('LD_LIBRARY_PATH')
    here = os.getcwd()
    libpath = here if not libpath else here + ':' + libpath
    os.environ['LD_LIBRARY_PATH'] = libpath
    
set_ld_library_path()
libx1052 = cdll.LoadLibrary('libx1052_api.so')


status=libx1052.X1052_LibInit()
print status


slot=0
hDev = libx1052.X1052_DeviceOpen(slot)
print hDev

addr=0xC000C000
data=2
pData=c_void_p(data)

INTP = POINTER(c_int)
data = c_int(42)
addr = addressof(data)
print 'address:', addr, type(addr)
pData = cast(addr, INTP)
print 'pointer:', pData
print 'value:', pData[0]


## Read
ret=libx1052.X1052_Wishbone_CSR(hDev,c_uint(addr),pData,0)
print "data:", hex(pData[0])
print "pData:", pData

##Write
##ret=libx1052.X1052_Wishbone_CSR(hDev,c_uint(addr),pData,1);

