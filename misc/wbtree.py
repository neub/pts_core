#!  /usr/bin/env python
from numpy.core.numeric import NaN
from ptsexcept import *

class GenericPeriph:

    BAR=0
    regs={}
    fields={}

    def __init__(self, bus, base_addr):
        self.bus = bus
        self.base_addr = base_addr

        
    def rd_reg(self, offset):
        return self.bus.iread(self.BAR, self.base_addr+offset, 4)

    def wr_reg(self, offset, value):
        #print '@0x%08x < 0x%08x' % (self.base_addr+offset, value)
        self.bus.iwrite(self.BAR, self.base_addr+offset, 4, value)
        
    def wr_bit(self, addr, bit, value):
        reg = self.rd_reg(addr)
        if(0==value):
            reg &= ~(1<<bit)
        else:
            reg |= (1<<bit)
        self.wr_reg(addr, reg)

    def rd_bit(self, addr, bit):
        if(self.rd_reg(addr) & (1<<bit)):
            return 1
        else:
            return 0    

    def rdb_reg(self,offset,position, width=1):
        data=self.rd_reg(offset)
        return (data >> position) & (pow(2,width)-1)
    
    def wrb_reg(self,offset,val, position, width=1):
        data=self.rd_reg(offset)
        mask=pow(2,width)-1 << position
        data= (data & ~mask) | ((val << position) & mask)
        #print '@0x%03x < 0x%08x (%d, %d, %08X, %d)' % (offset, data, val, position,mask, width)
        self.wr_reg(offset,data)
        
    def bitreg_write(self,fldname,value):
        if self.fields.has_key(fldname):
            self.wrb_reg(self.fields[fldname][0],value,self.fields[fldname][1],self.fields[fldname][2])
            
    def bitreg_read(self,fldname):
        if self.fields.has_key(fldname):
            return self.rdb_reg(self.fields[fldname][0],self.fields[fldname][1],self.fields[fldname][2])
        else:
            raise PtsInvalid("field '%s' is does not exist" % (fldname))
                
    def bitreg_desc(self, fldname, offset, fldpos, width=1):
        position=fldpos+8*(offset%4)
        offset-=(offset%4)
        if self.fields.has_key(fldname):
            raise NameError('Field name already used by this peripheral') 
        if self.regs.has_key(str(offset)) == 0:
            self.regs[str(offset)]={}
        self.regs[str(offset)][fldname]=position
        self.fields[fldname]=(offset,position,width)
        
    def bitreg_print(self,offset,fldname=None):
        data=self.rd_reg(offset)
        if fldname==None:
            print '@0x%08X: 0x%08x' % (offset+self.base_addr, data)
            for fldname in self.regs[str(offset)]:
                #print self.regs[str(offset)][fld], (data >> fld) & 1  
                print "%-15s (%02d) => %d , " % (fldname, self.regs[str(offset)][fldname], (data >> self.regs[str(offset)][fldname]) &1)
        else:
            print fldname , " => ", (data >> self.regs[str(offset)][fldname]) &1
            
    def bitreg_check(self,offset,act_val,expect_val):
        msg=""
        reg=self.regs[str(offset)]
        #print 'act = %08x, exp=%08x' % ( act_val,expect_val)
        for val in reg:
            mask = 1 << reg[val]
            #print  val,"...", reg[val] ,">", mask
            if act_val & mask != expect_val & mask:
                msg+=val+" don't have correct value\n"
        return msg