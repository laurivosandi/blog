.. title: Ralink rt73 in Access Point mode
.. date: 2010-05-30 18:14:26
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: hostapd, Ralink, rt73, access point, kuumpunkt, hotspot, HostAP

Ralink rt73 in Access Point mode
================================

This is a follow-up to my previous post about a USB wireless dongle I had acquired some weeks ago.

As I said this device shows up as:

.. code:: bash

    Bus 002 Device 008: ID 148f:2573 Ralink Technology, Corp. 
        RT2501USB Wireless Adapter

There seems to be some ambiquity about the vendorid/productid because this matches multiple chipsets. Usually it is pointing to rt73 chipset but be warned!

Firstly I installed Gentoo in VirtualBox since I didn't want to mess with my Estobuntu install. The rt2x00 guys have landed in Linux Git repository and they have a branch there with most up-to-date drivers. Note that this pulls over 100MB of changsets!:

.. code:: bash

    cd /usr/src
    git clone 
        git://git.kernel.org/pub/scm/linux/kernel/git/ivd/rt2x00.git 
        linux-rt2x00
    ln -s linux-rt2x00 linux
    cd linux
    make menuconfig # Enable rt2x00 modules under networking device drivers
    make -j4
    make modules_install
    make install
    nano /boot/grub/grub.conf

Next I installed hostapd. Note that "iwconfig wlan0 mode master" DOES NOT work anymore. Instead hostapd is used which is relies on new mac80211 framework in kernel to set wireless card settings. Gentoo had hostapd version 0.6.9 in portage which failed with this card, I installed manually 0.7.2:

.. code:: bash

    wget http://hostap.epitest.fi/releases/hostapd-0.7.2.tar.gz
    tar xvzf hostapd-0.7.2.tar.gz
    cd hostapd
    cp defconfig .config
    nano .config # Enable CONFIG_DRIVER_NL80211 there
    make
    make install

Afterward I created hostapd.conf with content like this:

.. code:: ini

    interface=wlan0
    driver=nl80211
    ssid=test
    channel=1

Note that before starting hostapd I needed firmware for this card. Firmware wasn't shipped within the Git branch. I had to copy it from my Estobuntu install. The file in question is /lib/firmware/rt73.bin, I placed it in the same place in my virtual machine:

.. code:: bash

    hostapd -dd /path/to/hostapd.conf

The AP should be visible now. Next step is to set IP for the card:

.. code:: bash

    ifconfig wlan0 192.168.100

Finally I had to configure DHCP server in /etc/dhcp/dhcpd.conf and restart DHCP server.
