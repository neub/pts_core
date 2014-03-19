#!/usr/bin/python

import sys
import time

from pts_core.misc.ptsexcept import *
##-------------------------------------------------------------------------------------------------
##                                         One Wire class                                        --
##-------------------------------------------------------------------------------------------------

class COpenCoresOneWire:

    R_CSR = 0x0
    R_CDR = 0x4

    CSR_DAT_MSK   = (1<<0)
    CSR_RST_MSK   = (1<<1)
    CSR_OVD_MSK   = (1<<2)
    CSR_CYC_MSK   = (1<<3)
    CSR_PWR_MSK   = (1<<4)
    CSR_IRQ_MSK   = (1<<6)
    CSR_IEN_MSK   = (1<<7)
    CSR_SEL_OFS   = 8
    CSR_SEL_MSK   = (0xF<<8)
    CSR_POWER_OFS = 16
    CSR_POWER_MSK = (0xFFFF<<16)
    CDR_NOR_MSK   = (0xFFFF<<0)
    CDR_OVD_OFS   = 16
    CDR_OVD_MSK   = (0XFFFF<<16)

    def wr_reg(self, addr, val):
        self.bus.write(self.base + addr,val)

    def rd_reg(self,addr):
        return self.bus.read(self.base + addr)

    def __init__(self, bus, base, clk_div_nor, clk_div_ovd):
        self.bus = bus
        self.base = base
        data = ((clk_div_nor & self.CDR_NOR_MSK) | ((clk_div_ovd<<self.CDR_OVD_OFS) & self.CDR_OVD_MSK))
        self.wr_reg(self.R_CDR, data)

    def reset(self, port):
        data = ((port<<self.CSR_SEL_OFS) & self.CSR_SEL_MSK) | self.CSR_CYC_MSK | self.CSR_RST_MSK
        self.wr_reg(self.R_CSR, data)
        tmo = 100
        while(self.rd_reg(self.R_CSR) & self.CSR_CYC_MSK):
            tmo = tmo -1
            if tmo <= 0:
                msg = "ERROR: TempID IC13: Not responding"
                raise PtsError(msg)
        reg = self.rd_reg(self.R_CSR)
        return ~reg & self.CSR_DAT_MSK

    def slot(self, port, bit):
        data = ((port<<self.CSR_SEL_OFS) & self.CSR_SEL_MSK) | self.CSR_CYC_MSK | (bit & self.CSR_DAT_MSK)
        self.wr_reg(self.R_CSR, data)
        tmo = 100
        while(self.rd_reg(self.R_CSR) & self.CSR_CYC_MSK):
            tmo = tmo -1
            if tmo <= 0:
                msg = "ERROR: TempID IC13: Not responding"
                raise PtsError(msg)
        reg = self.rd_reg(self.R_CSR)
        return reg & self.CSR_DAT_MSK

    def read_bit(self, port):
        return self.slot(port, 0x1)

    def write_bit(self, port, bit):
        return self.slot(port, bit)

    def read_byte(self, port):
        data = 0
        for i in range(8):
            data |= self.read_bit(port) << i
        return data

    def write_byte(self, port, byte):
        data = 0
        byte_old = byte
        for i in range(8):
            data |= self.write_bit(port, (byte & 0x1)) << i
            byte >>= 1
        if(byte_old == data):
            return 0
        else:
            return -1
    
    def write_block(self, port, block):
        if(160 < len(block)):
            return -1
        data = []
        for i in range(len(block)):
            data.append(self.write_byte(port, block[i]))
        return data

    def read_block(self, port, length):
        if(160 < length):
            return -1
        data = []
        for i in range(length):
            data.append(self.read_byte(port))
        return data