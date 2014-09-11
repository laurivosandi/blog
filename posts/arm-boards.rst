.. title: ARM boards
.. date: 2014-06-25
.. tags: ARM, Cubietruck

ARM boards
==========

Introduction
------------

This blogpost covers most SoC boards:

* `Raspberry Pi`_
* `HummingBoard`_
* `CuBox`_
* `Arndale board`_
* `Cubietruck`_



Raspberry Pi
------------

Raspberry Pi popularized the ARM board concept:

.. figure:: http://www.rpelectronics.com/Media/400/raspberry-pib.jpg

    Raspberry Pi model B

The truth is that it's using Broadcom BCM2835 SoC which has louzy specs for mainstream use:

* ARMv6 with floating point and SIMD extensions clocked at 700MHz
* 512MB RAM
* 100Mbps ethernet
* HDMI video output
* 1080p h264 video decoder
* Videocore 4 GPU
* 2x USB 2.0 ports
* 3.5mm audio jack

Boot methods:

* FAT32 partition on SD card

Community is of course massive:

* https://github.com/raspberrypi/
* #raspbian @ Freenode IRC

Origenboard
-----------

Origen 4 Quad Evaluation Board is based on Samsung Exynos 4210.

.. image:: http://img2.tgdaily.com/sites/default/files/stock/article_images/hardware/origen4quad.jpg
    :align: center
    

Arndale board
-------------

Arndale has two boards, the latest one called Arndale Octa Board Package
ships with Samsung Exynos 5420 octacore SoC:

.. image:: http://www.arndaleboard.org/wiki/images/0/0b/5420_board.png
    :align: center
    
The board seems to be manufactured by InSignal which is a Korean company. `Pyrustek <http://www.pyrustek.com/>`_ ships the board
from Korea for 199 USD pricetag excluding VAT and customs.

Arndale Octa Board Package specs:

* Four ARM Cortex-A15 cores with max clock at 1.3GHz
* Four ARM Cortex-A7 cores
* 3GB LPDDR3e RAM
* 100Mbps Ethernet
* 1080p 60fps video decoder
* Mali T628 MP6 GPU
* HDMI 1.4a connector
* 1x USB 3.0 port
* 3.5mm audio jack output (24bit DAC @96kHz)

Boot methods:

* eMMC internal storage
* MicroSD (?)

Community:

* http://www.arndaleboard.org/wiki/index.php/O_WiKi

HummingBoard
------------

`HummingBoard <http://imx.solid-run.com/wiki/index.php?title=HummingBoard_Hardware>`
is a Raspberry Pi compatible board oriented mainly towards
developers:

.. image:: http://imx.solid-run.com/wiki/images/5/51/HummingBoard.png
    :align: center

HummingBoard will most probably sport following spec
based on one of Freescale i.MX6 chips:

* Quad-core ARM Cortex A9
* 2GB RAM
* Broadcom BCM4329 802.11abgn wireless with Bluetooth 2.1
* Gigabit ethernet
* HDMI connector
* LVDS connector
* Coax S/PDIF digital audio output
* Infrared receiver
* MicroSD memory card slot
* mini PCI-E connector
* mSATA connector

CuBox
-----

CuBox-i4pro is a pretty neat ARM box:

.. image:: http://www.yung.jp/bony/wp-content/uploads/2014/03/cubox.jpg
    :align: center

* Quad-core ARM Cortex A9 clocked at 1GHz
* 2GB DDR3
* Vivante GC2000 GPU
* Gigabit ethernet
* HDMI video/audio output
* eSATA port
* 2x USB2.0 ports

Boot methods:

* MicroSD card


Cubietruck
----------

`Cubietruck <debian-jessie-sunxi-packages.html>`_ is Chinese Allwinner A20 SoC based board:

.. image:: http://www.seeedstudio.com/depot/images/product/Cubietruck_03.jpg
    :align: center

Cubietruck spec:

* Dual-core ARM Cortex-A7 @ 1GHz
* 2GB DDR2 @ 528MHz
* 8GB NAND Flash
* Mali400 MP2 GPU
* CedarX 2160p video decoder
* Broadcom BCM4329 802.11bgn wireless with Broadcom BCM40181 Bluetooth 4.0
* HDMI digital video/audio output
* **VGA analog video output**
* SPDIF digital audio output
* 1Gbps Realtek RTL8211E wired ethernet
* 1x **SATA 2.0 slot**
* 2x USB2.0 host
* 1x USB OTG

Boot methods:

* MicroSD card via on-board slot
* Internal NAND Flash
* SATA (via kernel and u-boot on internal NAND Flash)

Community is alive and kicking and among Chinese ARM SoC-s it is probably
the most progressive and upstream friendly:

* #linux-sunxi and #cubieboard @ Freenode IRC
    
Radxa Rock
----------

Radxa Rock is another Chinese Rockchip SoC based ARM board:

.. image:: http://www.seeedstudio.com/depot/images/product/radxa.jpg
    :align: center
    
Rockchip RK3188 SoC:

* Quad-core ARM Cortex-A9, 2GB RAM
* 8GB NAND Flash mälu
* MicroSD memory card slot
* Mali400 GPU
* HDMI pesa
* 100Mbps LAN
* 150Mbps 802.11bgn
* Bluetooth 4.0
* S/PDIF heliväljund
* 2x USB2.0 host pesa
* 1x USB OTG pesa

Community:

* #linux-rockchip @ Freenode IRC

