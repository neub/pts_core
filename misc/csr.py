#!/usr/bin/python

import sys
import time


class CCSR:

	def __init__(self, bus, base_addr):
		self.base_addr = base_addr;
		self.bus = bus;

	def wr_reg(self, addr, val):
		#print("                wr:%.8X reg:%.8X")%(val,(self.base_addr+addr))
		self.bus.write(self.base_addr +  addr, val)

	def rd_reg(self, addr):
		reg = self.bus.read(self.base_addr + addr)
		#print("                reg:%.8X value:%.8X")%((self.base_addr+addr), reg)
		return reg

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
		
	def toogle_bit(self,addr,bit):
		self.wr_bit(addr, bit, ~self.rd_bit(addr, bit))

	def wr_bits(self,addr,value, pos, width):
		reg = self.rd_reg(addr)
		mask=(((1<<width)-1) << (pos))
		#print "value=0x%x & mask=0x%08x @0x%08X" % (value, mask,addr) 
		reg = (reg & ~mask) | ((int(value) << pos) & mask) 
		self.wr_reg(addr, reg)
		
		
	def rd_bits(self,addr,pos, width):
		reg = self.rd_reg(addr)
		return self.get_bits(reg, pos, width)
	
	def get_bits(self,reg,pos,width):
		return (reg >> pos) & ((1<<width)-1)