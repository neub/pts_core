#!   /usr/bin/env   python
# -*- coding: utf-8 -*
'''
Created on Mar 11, 2014


    When all data bits have been read or written, a stop 
condition is established. In write mode, the master pulls 
the SDA line high during the 10th clock pulse to establish a 
stop condition. In read mode, the master issues a no 
acknowledge for the ninth clock pulse (that is, the SDA line 
remains high). The master then brings the SDA line low 
before the 10th clock pulse, and then high during the 10th 
clock pulse to establish a stop condition


@author: Benoit Rat (benoit<AT>sevensols.com)
@licence: GPL v2 or later.
@ref: http://www.ohwr.org
@ref: http://www.sevensols.com
'''
from pts_core.misc.ptsexcept import PtsInvalid

class AD56x2(object):
    '''
    Driver to control the AD5602/AD5612/AD5622 devices through i2c
    
    Vout = Vdd x (D /2^nbits)
    
    D is the decimal equivalent of the binary code that is loaded to the DAC register;
    It can range from:
        * 0 to 255  (AD5602), 
        * 0 to 1023 (AD5612)
        * 0 to 4095 (AD5622). 
    
    @ref: http://www.analog.com/static/imported-files/data_sheets/AD5602_5612_5622.pdf
    '''


    def __init__(self,i2c,i2c_addr,type):
        '''
        @param i2c: The I2C class object that represent the bus
        @param i2c_addr: Address of the chip on the I2C bus
        @param type: Tell if the number that correspond to X (ie, type=2 => AD5622 type)
        
        * Addr<=GND => i2c_addr= (0b0001100 | 0b11) <=> 0xF
        * Addr<=Vdd => i2c_addr= (0b0001100 | 0b00) <=> 0xC
        * Addr<=NC  => i2c_addr= (0b0001100 | 0b10) <=> 0xE
        '''
        self.i2c=i2c
        self.i2c_addr=i2c_addr
        if type < 0 and 2 < type:
            raise PtsInvalid("type must be 0,1 or 2")
        type=round(type)
        self.nbits=type*2+8
        self.shift=4-type*2;
        self.pdm=0
        
    def set_powerdown_mode(self,index):
        '''
        @param index: Index of the modes to select [0-3]
        
        When both bits are set to 0, the part works normally with its 
        usual power consumption of 100 µA maximum at 5 V. However, 
        for the three power-down modes, the supply current falls to 
        <150 nA (at 3 V). Not only does the supply current fall, but the 
        output stage is internally switched from the output of the 
        amplifier to a resistor network of known values. This gives the 
        advantage of knowing the output impedance of the part while 
        the part is in power-down mode. There are three different 
        options. The output is connected internally to GND through a 
        1 kΩ resistor, a 100 kΩ resistor, or it is left open-circuited 
        '''
        modes=["Normal","PD: 1kOhm Load","PD: 100kOhm Load","Power Down"]
        if index < 0 and 1 < len(modes):
            raise PtsInvalid("index must be between [0-%d]" % (len(modes)))
        print "Powerdown mode is #d %s " % (index, modes[index])
        self.pdm=index << 11 

    def wr_vout(self, ratio):
        '''
        @param ratio: Set the DAC output by following the formula:
            - Vout=Vdd x ratio
        Where Vdd is given by the hardware.
        '''
        
        if ratio < 0 and 1 < ratio:
            raise PtsInvalid("ratio must be between [0-1]")
        
        data=self.pdm | (round((2^self.nbits-1)*ratio) << self.shift)
        print "ratio=%f => data=0x%x" %(ratio,data)
        
        self.i2c.start(self.i2c_addr, True)
        self.i2c.write((data >> 8) & 0xFF, False)
        self.i2c.write((data & 0xFF), True)
        return 0;
    

