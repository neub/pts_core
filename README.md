Core files for  PTS (production test suites)
=========================

This project proposed a shared library for all the diferent production
test suite.

The organization of the directory is as follow

* `doc`: An extended documentation of this library
* `drivers`: The class to connect directly with the device (PCie, VME, MTD, ...)
, a kernel driver and a C library might be needed.
* `ibus`: Class that represent internal bus in the device: I2C, OneWire, SPI, etc.
* `misc`: Miscellanous class in order to ease the programation.
* `periph`: Class to handle a specific peripheral (i,e. the PLL AD9516.)
* `tools`: Other tools that could be usefull for device (FRU generator for EEPROM)

A more detailed information can be found in the `doc` folder.





