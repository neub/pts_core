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
from pts_core.misc.ptsexcept import *

##-------------------------------------------------------------------------------------------------
##                                           SPI class                                           --
##-------------------------------------------------------------------------------------------------

class COpenCoresSPI:

    R_RX   = [0x00, 0x04, 0x08, 0x0C]
    R_TX   = [0x00, 0x04, 0x08, 0x0C]
    R_CTRL = 0x10
    R_DIV  = 0x14
    R_SS   = 0x18

    LGH_MASK   = (0x7F)
    CTRL_GO    = (1<<8)
    CTRL_BSY   = (1<<8)
    CTRL_RXNEG = (1<<9)
    CTRL_TXNEG = (1<<10)
    CTRL_LSB   = (1<<11)
    CTRL_IE    = (1<<12)
    CTRL_ASS   = (0<<13)

    DIV_MASK = (0xFFFF)

    SS_SEL = [0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40]

    conf = 0x0

    def wr_reg(self, addr, val):
        self.bus.write(self.base + addr,val)

    def rd_reg(self,addr):
        return self.bus.read(self.base + addr)

    def __init__(self, bus, base, divider):
        self.bus = bus;
        self.base = base;
        self.wr_reg(self.R_DIV, (divider & self.DIV_MASK));
        # default configuration
        self.conf = self.CTRL_ASS # | self.CTRL_TXNEG

    def wait_busy(self):
        tmo = 1000
        while(self.rd_reg(self.R_CTRL) & self.CTRL_BSY):
            tmo = tmo -1
            if tmo <= 0:
                raise PtsError("Timeout waiting on busy flag")

    def config(self, ass, rx_neg, tx_neg, lsb, ie):
        self.conf = 0
        if(ass):
            self.conf |= self.CTRL_ASS
        if(tx_neg):
            self.conf |= self.CTRL_TXNEG
        if(rx_neg):
            self.conf |= self.CTRL_RXNEG
        if(lsb):
            self.conf |= self.CTRL_LSB
        if(ie):
            self.conf |= self.CTRL_IE
    
        # slave = slave number (0 to 7)
        # data = byte data array to send, in case if read fill with dummy data of the right size
        # This transaction has been modified for this test!!

    def transaction(self, slave, data):

        self.wr_reg(self.R_SS, self.SS_SEL[slave])
        
        txrx = [0x00000000, 0x00000000, 0x00000000, 0x00000000]
        txrx[0] = 0x00FFFFFF & data
        self.wr_reg(self.R_CTRL, 0)
        self.wr_reg(self.R_TX[0], txrx[0])
        
        ctrl_reg = self.CTRL_ASS | self.CTRL_GO | 24
        self.wr_reg(self.R_CTRL, ctrl_reg)
        
        tmo = 100
        while(((self.rd_reg(self.R_CTRL) >> 8) & 0x00000001) == 1):
            tmo = tmo -1
            if tmo <= 0:
                msg = "ERROR: DAC IC3 or IC7: Not responding"
                raise PtsError(msg)
        
        ##Resetting
        self.wr_reg(self.R_SS, 0)
        self.wr_reg(self.R_CTRL, 0)
        return txrx

    def transaction2(self, slave, data):
        txrx = [0x00000000, 0x00000000, 0x00000000, 0x00000000]
        for i in range(0,len(data)):
            txrx[i/4] += (data[i]<<((i%4)*8))
            #print("tx[%d]=%.8X data[%d]=%.2X") %(i,txrx[i/4],i,data[i])
    
        for i in range(0, len(txrx)):
            self.wr_reg(self.R_TX[i], txrx[i])
    
        self.wr_reg(self.R_SS, self.SS_SEL[slave])
        self.wr_reg(self.R_CTRL, (self.LGH_MASK & (len(data)<<3)) | self.CTRL_GO | self.conf)
        self.wait_busy()
    
        for i in range(0, len(txrx)):
            txrx[i] = self.rd_reg(self.R_RX[i])
            #print("rx[%d]=%.8X") %(i,txrx[i])
    
        return txrx