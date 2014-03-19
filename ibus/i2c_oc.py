#!   /usr/bin/env   python
#    coding: utf8
'''
@author: Samuel Iglesias Gonsalvez (siglesia@cern.ch)
@author: Benoit Rat (benoit<AT>sevensols.com)
@licence: GPL v2 or later.
@ref: http://www.ohwr.org
@ref: http://www.sevensols.com
'''

##-------------------------------------------------------------------------------------------------
##                               GNU LESSER GENERAL PUBLIC LICENSE                                |
##                              ------------------------------------                              |
## This source file is free software; you can redistribute it and/or modify it under the terms of |
## the GNU Lesser General Public License as published by the Free Software Foundation; either     |
## version 2.1 of the License, or (at your option) any later version.                             |
## This source is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;       |
## without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.      |
## See the GNU Lesser General Public License for more details.                                    |
## You should have received a copy of the GNU Lesser General Public License along with this       |
## source; if not, download it from http://www.gnu.org/licenses/lgpl-2.1.html                     |
##-------------------------------------------------------------------------------------------------

import sys
import time


##-------------------------------------------------------------------------------------------------
##                                           I2C class                                           --
##-------------------------------------------------------------------------------------------------
class COpenCoresI2C:
    '''
    Class to control the Core I2C from OpenCores 
    
    @ref: http://opencores.org/project,i2c
    '''

    R_PREL = 0x0
    R_PREH = 0x4
    R_CTR  = 0x8
    R_TXR  = 0xC
    R_RXR  = 0xC
    R_CR   = 0x10
    R_SR   = 0x10

    CTR_EN   = (1<<7)
    CR_STA   = (1<<7)
    CR_STO   = (1<<6)
    CR_WR    = (1<<4)
    CR_RD    = (1<<5)
    CR_NACK  = (1<<3)
    SR_RXACK = (1<<7)
    SR_TIP   = (1<<1)


    def __init__(self, bus, base, prescaler):
        '''
        Constructor
        @param bus: The main wishbone bus to access to the I2C core
        @param base: The WB base address of this core
        @param prescaler: divide the core frequency by `prescaler+1` 
        to obtain a lower frequency for I2C clock. 
        '''
        self.bus = bus;
        self.base =base;
        self.wr_reg(self.R_CTR, 0);
        self.wr_reg(self.R_PREL, (prescaler & 0xff))
        self.wr_reg(self.R_PREH, (prescaler >> 8))
        self.wr_reg(self.R_CTR, self.CTR_EN);

    def wr_reg(self, addr, val):
        self.bus.write(self.base + addr,val)

    def rd_reg(self,addr):
        return self.bus.read(self.base + addr)

    def wait_busy(self):
        tmo = 0
        while(self.rd_reg(self.R_SR) & self.SR_TIP):
            tmo = tmo+1
            if tmo > 1000:
                msg = "ERROR: EEPROM IC31: Not responding"
                raise PtsError(msg)

    def start(self, addr, write_mode):
        addr = addr << 1
        if(write_mode == False):
            addr = addr | 1;
        self.wr_reg(self.R_TXR, addr);
        self.wr_reg(self.R_CR, self.CR_STA | self.CR_WR);
        self.wait_busy()
        if(self.rd_reg(self.R_SR) & self.SR_RXACK):
            pass

    def write(self, data, last):
        self.wr_reg(self.R_TXR, data);
        cmd = self.CR_WR;
        if(last):
            cmd = cmd | self.CR_STO;
        self.wr_reg(self.R_CR, cmd);
        self.wait_busy();
        if(self.rd_reg(self.R_SR) & self.SR_RXACK):
            pass

    def read(self, last):
        cmd = self.CR_RD;
        if(last):
            cmd = cmd | self.CR_STO | self.CR_NACK;
        self.wr_reg(self.R_CR, cmd);
        self.wait_busy();
        return self.rd_reg(self.R_RXR);

    def scan_bus(self):
        for i in range(0,128):
            self.wr_reg(self.R_TXR, i<<1);
            self.wr_reg(self.R_CR, self.CR_STA | self.CR_WR);
            self.wait_busy()
            if(not self.rd_reg(self.R_SR) & self.SR_RXACK):
                # print("scan_bus:Found device at addr %x" % i)
                return i
            self.wr_reg(self.R_CR, self.CR_STO);
            self.wait_busy()

    def scan(self):
        periph_addr = []
        for i in range(0,128):
            self.wr_reg(self.R_TXR, i<<1)
            self.wr_reg(self.R_CR, self.CR_STA | self.CR_WR)
            self.wait_busy()
            if(not self.rd_reg(self.R_SR) & self.SR_RXACK):
                # print("scan:Device found at address: 0x%.2X") % i
                periph_addr.append(i)
            self.wr_reg(self.R_CR, self.CR_STO);
            self.wait_busy()
        return periph_addr