#!  /usr/bin/env python
#   :vi:ts=4 sw=4 et

from ctypes import *
import os, errno, re, sys, struct
import os.path

# python 2.4 kludge
if not 'SEEK_SET' in dir(os):
    os.SEEK_SET = 0

# unsigned formats to unpack words
fmt = { 1: 'B', 2: 'H', 4: 'I', 8: 'L' }


RR_BAR_0      = 0x00000000

bar_map = {
    0 : RR_BAR_0,
}



class FileMem:

    def __init__(self, fpath):
        """get a file descriptor for the Gennum device"""
        self.fid = open(fpath,'r+')
        
    def __del__(self):
        self.fid.close()
        
    def find(self,address):
        line=self.fid.readline()
        val=0
        pos=line.find('@0x%08X:' % (address))
        if pos<0:
            self.fid.seek(0)
            lines = self.fid.read()
            pos = lines.find('@0x%08X:' % (address))
            if pos >=0:
                self.fid.seek(pos)
                line=self.fid.readline()
        if pos>=0:
            val=re.search('@0x%08X: 0x([0-9a-f]{8})' % (address),line, re.IGNORECASE).group(1)
            val=int(val,16)
        return {'pos':pos, 'val':val} 
        


    def iread(self, bar, offset, width):
        """do a read by means of the ioctl interface

            bar = 0
            offset = address within bar
            width = data size (1, 2, or 4 bytes)
        """
        address = bar_map[bar] + offset
        ret=self.find(address)
        print "R: @0x%08X: 0x%08x (%d)" % (address, ret['val'],ret['pos'])  
        return ret['val']

    def read(self, bar, offset, width):
        """do a read by means of lseek+read

            bar = 0
            offset = address within bar
            width = data size (1, 2, or 4 bytes)
        """
        return self.iread(bar, offset, width)

    def iwrite(self, bar, offset, width, datum):
        """do a write by means of the ioctl interface

            bar = 0
            offset = address within bar
            width = data size (1, 2, 4 or 8 bytes)
            datum = value to be written
        """
        address = bar_map[bar] + offset
        wstr="@0x%08X: 0x%08x" % (address,datum)
        ret=self.find(address)
        if ret["pos"]>=0:
            self.fid.seek(ret["pos"])
        print "W: %s" % (wstr)
        self.fid.write(wstr+"\n")


    def write(self, bar, offset, width, datum):
        """do a write by means of lseek+write

            bar = 0
            offset = address within bar
            width = data size (1, 2, 4 or 8 bytes)
            datum = value to be written
        """
        return self.iwrite(bar, offset, width, datum)

    def irqwait(self):
        """wait for an interrupt"""
        raise NameError('Undef function') 
        return 0;

    def irqena(self):
        """enable the interrupt line"""
        raise NameError('Undef function') 
        return 0;

    def getdmasize(self):
        """return the size of the allocated DMA buffer (in bytes)"""
        raise NameError('Undef function') 
        return 0;

    def getplist(self):
        """get a list of pages for DMA access

        The addresses returned, shifted by 12 bits, give the physical
        addresses of the allocated pages
        """
        raise NameError('Undef function') 
        plist = Plist()
        self.lib.rr_getplist(self.fd, plist);
        return plist

    def info(self):
        """get a string describing the interface the driver is bound to

        The syntax of the string is
            vendor:device/dubvendor:subdevice@bus:devfn
        """
        return ''
        
    def parse_addr(self, addr):
        """take a string of the form
               vendor:device[/subvendor:subdevice][@bus:devfn]
        and return a dictionary object with the corresponding values,
        initialized to RR_DEVSEL_UNUSED when absent
        """
        raise NameError('Undef function') 
        return None

    def bind(self, device):
        """bind the rawrabbit driver to a device

        The device is specified with a syntax described in parse_addr
        """
        d = self.parse_addr(device)
        self.errno=0
        return self.errno
    