.. title: Setting up wireless USB dongle on Raspberry Pi
.. date: 2013-06-30
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: Raspbian, Debian, Ralink, interfaces

Setting up wireless USB dongle on Raspberry Pi
==============================================

DealExtreme ships `802.11bgn wireless USB dongles <http://dx.com/p/mini-usb-2-4ghz-150mbps-802-11b-g-n-wifi-wireless-network-card-adapter-black-120933>`_
for 6.30 USD and of course I had to get one of those.
This one shows up as:

.. code:: bash

    Bus 001 Device 004: ID 148f:5370 Ralink Technology, Corp. RT5370 Wireless Adapter

The required driver and firmware blob seem to be available in Raspbian Wheezy, so setting up */etc/network/interfaces* is the last step to get this dongle working:

.. code:: bash

    auto lo
    iface lo inet loopback

    auto eth0
    allow-hotplug eth0
    iface eth0 inet dhcp

    auto wlan0
    allow-hotplug wlan0
    iface wlan0 inet dhcp
        wpa-ssid "lauri-802.11bgn"   # Your wireless network name
        wpa-psk "replace-me"         # Your WPA/WPA2 password

After that you should of course restart NetworkManager and networking services:

.. code:: bash

    sudo service network-manager restart
    sudo service networking restart

This howto should work for Ubuntu and other Debian-like operating systems aswell.

