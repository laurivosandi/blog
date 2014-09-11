.. tags: Cubietruck, sunxi, ARM, Debian

Products & Services
===================

Cubietruck
----------

Cubietruck [#cubietruck.com]_ is a neat ARM board that runs Debian, Fedora, Ubuntu and other
Linux distributions:

.. image:: http://i00.i.aliimg.com/wsphoto/v2/1370367878_1/Cubieboard-3-cubietruck-free-shipping.jpg
    :width: 50%
    :align: right
    
.. image:: http://www.seeedstudio.com/depot/bmz_cache/a/a728b5d3ca999882c51679ab4a676840.image.530x397.jpg
    :width: 50%
    :align: right

* Dual-core ARM Cortex-A7 @ 1GHz
* 2GB DDR2 @ 528MHz
* 8GB NAND Flash on-board storage
* Mali400 MP2 GPU
* CedarX 2160p hardware video decoder
* HDMI digital video output
* VGA analoog video output
* SPDIF digital audio output
* 1Gbps Realtek RTL8211E wired network interface
* Broadcom BCM4329 802.11bgn wireless network interface
* Broadcom BCM40181 Bluetooth 4.0 interface
* 2x USB2.0 host
* 1x USB OTG
* 1x microSD slot
* 1x SATA 2.0 slot
* Plenty of GPIO pins that can be configured to SPI, I²C, UART etc modes
* LiPo voltage stabilizer

I usually have one or two for sale with me and couple more at Tallinn.
Pricing depends on who you are:

* 99EUR for students, with simple plexiglas case
* 159EUR for businesses, with simple plexiglas case
* 169EUR for businesses, with black case

.. [#cubietruck.com] http://www.cubietruck.com/

Diskless workstations
---------------------

Cubietrucks booting from local area network are enough to cope with todays demanding web.
Considering trends moving towards standards-compliant web
it makes sense to minimize software stack running on
workstations and focus on the browser platform.

.. figure:: img/nfsroot.svg

The workstations are completely maintenance free, there is no harddisk or fan attached.
The software, configuration and user files are stored on central fileserver.
This solution requires gigabit capable local area network to decrease the latency
of launching applications.

.. important:: This is not traditional terminal-server solution, the software actually runs on the workstation!

We use rock-solid Debian as foundation and build our solution on top of
open-source and libre software.
We're shipping with Chromium 34 with full Estonian ID-card authentication and signing support.
Currently 1080p h264 playback via standalone application is supported.
Adobe Flash version 14 is supported via PepperPlugin API of Chromium.
LibreOffice 4.3 is available from Debian repositories.
The hardware works also with old screens which makes it possible to postpone
hardware procurement.
Unfortunately there is no Skype available for this particular setup.
Firefox usage is discouraged as it does not perform well on this hardware.
We are working hard to enable hardware accelerated video decoding for Youtube.

Our pricing is pretty flexible, includes 3-year limited warranty and initial setup:

* 169EUR per Cubietruck
* 489EUR per fileserver
* 199EUR for two 2TB harddisks in RAID1 configuration

You will get handed full documentation and sources of the solution and
we will try to do our best to avoid vendor lock-in.


Small to medium office backbone
-------------------------------

Utilizing OpenVPN, OpenLDAP, Puppet and other well-known tools
we can maintain desktops and roaming laptops while keeping consistent
usernames, passwords and storage plus central management of the machines.

Our pricing is flexible depending on your needs:

* 19EUR per year account maintenance fee including 500GB cloud storage for up to 5 devices
* 99EUR per month managing dedicated server park with same feature set for up to 100 machines for you organization

Coming in 2015: Kerberos based single sign-on and OwnCloud or similar with proper file synchronization.
