.. title: Debian Lenny, LTSP ja ID-kaart
.. date: 2010-12-13 22:39:26
.. tags: Debian, LTSP, SmartCard, PKCS#11, ID-card, ID-kaart

Debian Lenny, LTSP ja ID-kaart
==============================

.. image: http://www.debian.org/logos/openlogo-nd-100.png

Serveri tarkvara paigaldus
--------------------------

Siin on siis väike juhend kuidas Debian Lenny'ga teha sama mida Estobuntu LTSP võimaldab. Pikalt see kord üksipulgi lahti ei seleta mis mida teeb nii et kui huvi on siis küsi e-posti vahendusel.

Kõigepealt paigalda serveris ID-kaardi tarkvara:

.. code:: bash

    echo deb http://id.smartlink.ee/repo/release/debian/ lenny main > 
        /etc/apt/sources.list.d/idkaart.list
    wget http://id.smartlink.ee/repo/apt-esteid-test.gpg.asc -O - | apt-key add -
    sudo aptitude update
    sudo aptitude dist-upgrade
    sudo aptitude install qdigidoc qesteidutil mozilla-esteid icedove-esteid

Luba repositooriumid:

.. code:: bash

    deb http://v6sa.itcollege.ee/ debian lenny
    deb http://backports.debian.org/debian-backports lenny-backports main

Seadista DHCP3 server:

.. code:: bash

    echo "subnet 192.168.0.0 netmask 255.255.255.0 {
        range 192.168.0.220 192.168.0.230;
        option broadcast-address 192.168.0.255;
        option routers 192.168.0.10;
        option subnet-mask 255.255.255.0;
        option root-path "/opt/ltsp/i386";
        filename "/ltsp/i386/pxelinux.0";
    }" > /etc/dhcp3/dhcpd.conf
    /etc/init.d/dhcp3-server restart

Paigalda tarkvara:

.. code:: bash

    apt-get install libpcsclite1 opensc openssh-server dhcp3-server
    apt-get install -t lenny-backports ltsp-server

Tee Xsessioni fail mis ütleb kus kohas PCSC-lite socket nüüd asub:

.. code:: bash

    echo "export PCSCLITE_CSOCK_NAME=$HOME/.pcscd.comm" > /etc/X11/Xsession.d/80-pcsclite

Terminali tarkvara paigaldus
----------------------------


Paigalda terminali tarkvara serveri /opt/ltsp/i386 alla:

.. code:: bash

    ltsp-build-client \
        --arch i386 \
        --backports-mirror "http://backports.debian.org/debian-backports" \
        --apt-key /etc/apt/trusted.gpg

Seadista NFS server:

.. code:: bash

    echo "/opt/ltsp/i386 192.168.0.0/24(no_root_squash,ro)" >> /etc/exports
    /etc/init.d/openbsd-inetd restart
    /etc/init.d/nfs-kernel-server restart

Sisene terminali juurikasse:

.. code:: bash

    chroot /opt/ltsp/i386

Lisa repositoorium:

.. code:: bash

    echo "deb http://lauri.vosandi.eu/ debian lenny" >> /etc/apt/sources.list
    apt-get update

Paigalda paketid:

.. code:: bash

    apt-get install openssh-client pcscd libccid

Lisa OpenSSH seadistused, asenda 192.168.0.10 serveri IP-ga:

.. code:: bash

    echo "Host 192.168.0.10
        RemoteForward [~/.pcscd.comm] :[/var/run/pcscd/pcscd.comm]" >> /etc/ssh/ssh_config

Välju terminali juurikast:

.. code:: bash

    exit

Käsitsi kompileerimine
----------------------


Paigalda vajalikud paketid:

.. code:: bash

    apt-get install libwrap0-dev libssl-dev libpam0g-dev libedit-dev libselinux1-dev libkrb5-dev libgtk2.0-dev hardening-includes libusb-1.0-0-dev mercurial flex autotools-dev libccid opensc
    apt-get install -t lenny-backports debhelper

Kompileeri modifitseeritud OpenSSH 5.5:

.. code:: bash

    hg clone http://lauri.vosandi.eu/hg/ltsp-esteid/openssh/
    cd openssh
    dpkg-buildpackage
    cd ..

Kompileeri PCSC-lite 1.6.5 + SVN muudatused:

.. code:: bash

    hg clone http://lauri.vosandi.eu/hg/ltsp-esteid/pcsclite/
    cd pcsclite
    dpkg-buildpackage
    cd ..


