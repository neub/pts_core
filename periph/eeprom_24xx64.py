#!   /usr/bin/env   python
#    coding: utf8
'''
@author: Julian Lewis (Julian.Lewis@cern.ch)
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

class C24xx64(object):
    '''
    Class to read/write on Micron 24AA64/24LC64/24FC64 
    64K I2C Serial EEPROM
    
    The i2c_addr is encoded in two part: 
     * Control Code = (0b1010 <<3)
     * Chip Select Address (Given by A0,A1,A2) 
    
    @ref: http://ww1.microchip.com/downloads/en/DeviceDoc/21189R.pdf
    '''


    def __init__(self, i2c, i2c_addr):
        '''
        Constructor
        @param i2c: The I2C class object
        @param i2c_adress: Address of the chip on the I2C bus 
        '''
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        
        
    def wr_data(self, mem_addr, data):
        if len(data) > 32:
            print "Maximum sequence write size is 32 byte!"
            return -1;
        self.i2c.start(self.i2c_addr, True)
        self.i2c.write((mem_addr >> 8), False)
        self.i2c.write((mem_addr & 0xFF), False)
        for i in range(len(data)-1):
            self.i2c.write(data[i],False)
        if len(data) > 1:
            i += 1
        else:
            i = 0
        self.i2c.write(data[i],True)
        return 0;

    def rd_data(self, mem_addr, size):
        self.i2c.start(self.i2c_addr, True)
        self.i2c.write((mem_addr >> 8), False)
        self.i2c.write((mem_addr & 0xFF), False)
        self.i2c.start(self.i2c_addr, False)
        data = []
        for i in range(size-1):
            data.append(self.i2c.read(False))
        data.append(self.i2c.read(True))
        return data;
