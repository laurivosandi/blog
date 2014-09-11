.. title: Improved internet sharing with Ubuntu
.. date: 2010-07-29 22:00:31
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: masquerade, iptables, internet sharing, dnsmasq

Improved internet sharing with Ubuntu
=====================================

This is a little howto about sharing internet with *dnsmasq* and Ubuntu.

Firstly let's create a script which will clean netfilter's routing tables, set up packet forwarding rules and allow only required services. Create firewall script in /etc/rc.firewall and append this script call to /etc/rc.local:

.. code:: bash

    #!/bin/bash
    
    # Echo commands and abort on errors
    set -x
    set -e
     
    # Define network interfaces:
    IFACE_WAN=eth0
    IFACE_LAN=eth1
    
    # Clean
    iptables -P INPUT ACCEPT
    iptables -P FORWARD ACCEPT
    iptables -P OUTPUT ACCEPT
    iptables -F
    iptables -t nat -F
    
    # Do masquerade
    iptables -A FORWARD -i $IFACE_WAN -o $IFACE_LAN -m state --state ESTABLISHED,RELATED -j ACCEPT
    iptables -A FORWARD -i $IFACE_LAN -o $IFACE_WAN -j ACCEPT
    iptables -t nat -A POSTROUTING -o $IFACE_WAN -j MASQUERADE
    
    # Enable packet forwarding
    echo 1 > /proc/sys/net/ipv4/ip_forward
    
    # Allow DHCP and DNS requests from LAN
    iptables -A INPUT -p udp -i $IFACE_LAN --dport 67 -j ACCEPT
    iptables -A INPUT -p udp -i $IFACE_LAN --dport 53 -j ACCEPT

Set executable bit and run it:

.. code:: bash

    sudo chmod +x /etc/rc.firewall
    sudo /etc/rc.firewall

Next step is to install *dnsmasq*:

.. code:: bash

    sudo apt-get install dnsmasq

Create *dnsmasq* configuration file in /etc/dnsmasq.conf:

.. code:: bash

    no-poll
    domain-needed
    bogus-priv
    strict-order
    interface=eth1
    bind-interfaces
    dhcp-range=192.168.0.10,192.168.0.200,255.255.255.0,48h
    dhcp-leasefile=/tmp/dnsmasq-leases.txt
    dhcp-authoritative
    resolv-file=/etc/resolv.conf.upstream
    log-queries

Next configure network interfaces in /etc/network/interfaces:

.. code:: bash

    # The loopback network interface
    auto lo
    iface lo inet loopback
     
    # WAN
    auto eth0
    iface eth0 inet dhcp
        post-up cp /etc/resolv.conf /etc/resolv.conf.upstream
        post-up echo "nameserver 127.0.0.1" > /etc/resolv.conf
    
    # LAN
    auto eth1
    iface eth1 inet static
        address 192.168.0.1
        netmask 255.255.255.0

Finally restart all the services:

.. code:: bash

    sudo /etc/init.d/networking restart
    sudo /etc/init.d/dnsmasq restart

If you have internet coming in on eth0 and other computers connected via eth1, they should receive proper IP address and DNS configuration from dnsmasq and internet sharing should work.
