.. title: Hexacore
.. date: 2010-06-18 14:25:41
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: AMD, multicore

Hexacore
========

Altough desktop PCs are slowly becoming obsolete, I acquired a new PC box to speed up compilation times and virtualization.

Here's the list of components assembled:

* AMD Phenom II x6 1055T 2.8GHz processor
* Gigabyte GA-880GM-UD2H motherboard
* 2x Apacer 2GB 1333MHz CL9 memory modules
* 2x Western Digital 1TB 64MB SATA2 disks
* Akasa Freedom tower AK-CC017 heatpipe cooling
* Chieftec BD-02B-SL-OP minitower case
* Chieftec 550W APS-550S power supply

I was much behind with latest technological advancements in PC field, so here goes what I learned. This processor has six cores running at 2.8GHz, L2 cache of 3MB, L3 cache of 6MB and TDP of 125W. AMD already has processors with 12 cores coming up. AMD's AM3 socket processors (Phenom II series) support DDR3 memory modules. DDR3 modules are clocked at various speeds - 800, 1066, 1333 and 1600 megahertz. At the moment 1333MHz seems to have best price/performance ratio.

AMD and nVidia manufacture AM3 chipsets, but to my knowledge nVidia chipsets don't perform that well. AMD is numbering chipsets like 790, 880 etc. - basically the bigger number, the better. It pretty much depends how much money you can spend on a motherboard. While considering manufacturer of the motherboard I have got the impression that Gigabyte has the best quality followed by Asus. The fact is that there aren't many AM3 motherboard manufacturers. Besides those two MSI and Asrock are also selling AM3 motherboards altough I wouldn't recommended those. On the contrary I have an Asrock AM2 board ticking over 3 years now.

Most of AMD's northbridges also have ATI Radeon 3xxx or 4xxx graphics integrated. At the moment Radeon proprietary drivers are lacking support for latest Ubuntu releases (Lucid Lynx 10.04). This Gigabyte motherboard has Radeon 4250. The open-source driver inclded in Ubuntu supports 2D acceleration so watching movies works, but 3D is disabled. Hopefully the driver situation improves in following months. This chip also includes digital audio outputs. This means that onboard HDMI and DVI sockets are directly connected to northbridge.

Besides graphics this motherboard has SB710 southbridge. There's gigabit ethernet link usng Realtek 8111C chip. Analog audio outputs are connected to Realtek ALC892 HD audio chip. Both of them work perfectly under Ubuntu 10.04.

For those who are interested, `here <http://pastebin.com/yhnqPE2d>`_  is output of lspci.

To get temperature sensors working with gkrellm you need to manually install `k10temp <http://swiss.ubuntuforums.org/showthread.php?p=8406822>`_  module, Ubuntu 10.04 kernel doesn't have this enabled.

Initially Ubuntu recognized only two channels on the sound card, I had to install ALSA backported modules. Afterwards I could have access to all the channels on the board:

.. code:: bash

    sudo apt-get install linux-backports-modules-alsa-$(uname -r)

Conclusion is that Ubuntu Lucid Lynx 10.04 supports this combination of  parts quite well.

UPDATE: This video card now has some 3D support, window manager effects basically work.

