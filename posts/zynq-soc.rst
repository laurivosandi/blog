.. title: Zynq-7000 All Programmable SoC
.. date: 2014-05-28
.. tags: TU Berlin, Zynq-7000, ZYBO, Zedboard, SoC, FPGA, VHDL

Zynq-7000 All Programmable SoC
==============================

Introduction
------------

The FPGA-s are getting hotter topic every day. Unfortunately there are few
FPGA manufacturers nowadays and they're reluctant to give out specs
to build open-source VHDL/Verilog to bitstream compilers.

However I do recognize the need for such technology and hopefully one day
there will be enough competition in this particular field which means that
better (open-source) tools will be available.

In Advanced Embedded Systems Project course we were given Xilinx boards to
develop an application using FPGAs.

Xilinx has several product series:

* Spartan is FPGA based on 45nm technology
* Virtex is FPGA based on 28nm tech
* Zynq incorporates dual-core ARM processor onto the same die with Atrix-7 programmable logic (PL)

In this post I wanted to introduce some boards for beginners.
As Spartan and Virtex boards don't include ARM processor by default I am going
to focus on Zynq-7000 boards, namely Zedboard and ZYBO.


Zedboard
--------

Zedboard is shipped with Zynq-7000 All Programmabe SoC XC7Z020-CLG484-1
which combines two ARM Cortex A9 cores and
Xilinx programmable logic in a single device [#zedboard]_.
Digilent sells this device for 495USD, but students get a discounted price of 319USD
which includes device-locked license for ISE.
Shipping to EU probably adds another 59USD totaling in 378 USD which is approximately 277 EUR.
With import taxes it adds up to about 341 EUR.

.. figure:: http://www.zedboard.org/sites/default/files/product_spec_images/ZedBoard_RevA_sideA_0_0%20%281%29_0.jpg

    Zedboard is the most mainstream beginner board


Zedboard specs:

* Dual-core ARM Cortex A9 @ 667MHz
* NEON single and double precision extensions
* 512MB DDR3 RAM
* 256MB Quad-SPI Flash
* 1Gbps LAN
* Built-in USB-UART bridge
* USB OTG port
* HDMI output (1080p at 60Hz /w audio)
* VGA output
* 128x32 pixel OLED display
* 9x programmable LED-s
* 8 DMA channels with 4 of them allocated to PL

The XC7Z020 SoC contains Atrix-7 PL which has:

* 85k logic cells
* ~1.3 million ASIC gates
* 53,200 look-up tables (LUT)
* 106,400 flip-flops
* 560kB (140 x 36kB) Block RAM
* 220 DSP slices (Multiplier-Accumulator) organized to 18 x 25
* 276 GMACs

In the lab I managed to get Xillinux [#xillinux]_ booting on it.

.. [#zedboard] http://www.zedboard.org/product/zedboard
.. [#xillinux] http://xillybus.com/xillinux


ZYBO
----

Digilent's ZYBO [#zybo]_ features Zynq-7000 All Programmable SoC ZYNQ XC7Z010-1CLG400C.
The price for students is 125 USD for the board + 20 USD for accessories and Vivaldo voucher + 59 USD shipping to EU =
204 USD which is approximately 150 EUR.
With import taxes it adds up to 188EUR.

.. figure:: http://www.digilentinc.com/Data/Products/ZYBO/ZYBO-revB-obl-600.png

    ZYBO is probably the cheapest board available

The ARM cores are the same as Zedboards's, it's the PL that differs:

* 28k logic cells
* ~430k ASIC gates
* 17,600 look-up tables (LUT)
* 35,200 flip-flops
* 240 kB  (60 x 36kB) Block RAM
* 80 DSP slices
* 100 GMACs

More details will follow once I get this board.

.. [#zybo] http://www.digilentinc.com/Products/Detail.cfm?NavPath=2,719,1197&Prod=ZYBO
