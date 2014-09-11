.. title: Messing with I²C
.. tags: I2C, Cubietruck
.. date: 2013-10-31

Messing with I²C
================

I²C (Integer-Integrated Circuit) also known as I2C, IIC, I-squared-C is a 
multimaster serial single-ended computer bus which originates from 
Philips semiconductor division. It is commonly used to attach
low-speed peripherals to motherboards.

If you happen to have I²C controller which is recognized by the kernel
you can run *i2cdetect* to enumerate slaves sitting on the bus [#i2cdetect]_.
You can easily see if your kernel has recognized any
I²C controllers just by checking whether any /dev/i2c-* block devices are present.
The only required argument is the number of the bus, where zero translates
to */dev/i2c-0*.

.. code:: bash

    i2cdetect 0

I am not sure what' going on with the slave UU on the first I²C of Cubietruck,
but as far as I know I am currently running a kernel that does not actually
power up that particual I²C bus:

.. code::

    WARNING! This program can confuse your I2C bus, cause data loss and worse!
    I will probe file /dev/i2c-0.
    I will probe address range 0x03-0x77.
    Continue? [Y/n] y
         0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
    10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    30: -- -- -- -- UU -- -- -- -- -- -- -- -- -- -- -- 
    40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    70: -- -- -- -- -- -- -- --     

The second bus gives me some output:

.. code::

    WARNING! This program can confuse your I2C bus, cause data loss and worse!
    I will probe file /dev/i2c-1.
    I will probe address range 0x03-0x77.
    Continue? [Y/n] y
         0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
    10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    30: -- -- -- -- -- -- -- 37 -- -- 3a -- -- -- -- -- 
    40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    50: 50 -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    70: -- -- -- -- -- -- -- --    
    
Interestingly all the slaves dissapear when I unplug the HDMI 
cable from my Cubietruck, that's because the second I²C bus is connected
to HDMI port. 

You can use *i2c-tools -l* to list I²C controllers:

.. code:: bash

    i2c-tools -l
    

    
.. code::

    i2c-0	i2c       	sunxi-i2c.0                     	I2C adapter
    i2c-1	i2c       	sunxi-hdmi-i2c                  	I2C adapter
    
 


You probably have to install *i2c-tools* in order to use that command:

.. code:: bash

    sudo apt-get install i2c-tools picocom



In this example we'll connect an I²C based accelerometer to a computer's USB 
port via Buspirate. Frist off we need tools to talk to the Buspirate and
I²C devices:

.. code:: bash

    sudo apt-get install i2c-tools picocom

Buspirate is a nifty tool for converting USB port to various other ports:
SPI, I²C.

.. code:: bash

    picocom -b 115200 -p n -d 8 /dev/ttyUSB0
    
This should open up Buspirate prompt:

.. code::

    Bus Pirate v3b
    Firmware v5.10 (r559)  Bootloader v4.4
    DEVID:0x0447 REVID:0x3043 (24FJ64GA002 B5)
    http://dangerousprototypes.com
    HiZ>

Typing m and pressing Enter outputs the list of wire protocols this particular Buspirate
can emulate:

.. code::

    HiZ>m
    1. HiZ
    2. 1-WIRE
    3. UART
    4. I²C
    5. SPI
    6. 2WIRE
    7. 3WIRE
    8. LCD
    9. DIO
    x. exit(without change)

To enter I²C mode press 4 and Enter. You'll be greeted with I²C prompt which 
actually accepts some Buspirate commands like enabling power on 3.3V and 5V pins:

.. code::

    I²C>W
    Power supplies ON
    
You can use I²C command (1) to enumerate slaves connected to the bus.
This is what I get with GY-50 accelerometer attached:

.. code::

    I²C>(1)
    Searching I²C address space. Found devices at:
    0xD2(0x69 W) 0xD3(0x69 R) 

With DS1307 I get following:

.. code::

    I²C>(1)
    Searching I²C address space. Found devices at:
    0xA0(0x50 W) 0xA1(0x50 R)
    
DS1307 does not respond properly with 3.3V volt power supply.

.. [#i2cdetect] `Scanning a I²C bus for available slave devices <http://e2e.ti.com/support/microcontrollers/tiva_arm/f/908/t/235977.aspx>`_
