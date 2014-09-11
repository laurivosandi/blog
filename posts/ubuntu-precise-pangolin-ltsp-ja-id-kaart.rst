.. title: Ubuntu 12.04, LTSP ja ID-kaart
.. date: 2012-07-28 10:19:03
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: Ubuntu, PKCS#11, OpenSC, pcscd, PCSC-Lite, OpenSC, ID-card, ID-kaart

Ubuntu 12.04, LTSP ja ID-kaart
==============================

Juhend eeldab `Ubuntu 12.04 desktop <http://www.ubuntu.com/download/desktop>`_  paigladust. Uuenda pakette:

.. code:: bash

    apt-get update
    apt-get dist-upgrade

Paigalda LTSP serveri metapakett, see paigaldab DHCP serveri ja muud LTSP jaoks tarvilikud teenused:

.. code:: bash

    apt-get install ltsp-server-standalone

Seadista võrk failis /etc/network/interfaces, asenda 192.168.77.1 omale sobiliku IP-ga:

.. code:: bash

    echo "auto lo
    iface lo inet loopback
              
    auto eth0
    iface eth0 inet dhcp
   
    auto eth1
    iface eth1 inet static
        address 192.168.77.1
        netmask 255.255.255.0" > /etc/network/interfaces

Asenda DHCP serveri seadistuste failis 192.168.0.0/24 alamvõrk:

.. code:: bash

    sed -i "s/192\.168\.0\./192.168.77./g" /etc/ltsp/dhcpd.conf

Taaskäivita võrguteenused:

.. code:: bash

    /etc/init.d/networking restart
    /etc/init.d/network-manager restart
    /etc/init.d/isc-dhcp-server restart
    /etc/init.d/nbd-server restart

Paigalda modifitseeritud OpenSSH server LTSP serverisse:

.. code:: bash

    echo "deb http://packages.koodur.com precise ltsp" | sudo tee /etc/apt/sources.list.d/v6sa-ltsp-hacks-precise.list
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B8A6153D   
    apt-get update
    apt-get install -y openssh-server

Lisa Eesti ID-kaardi ametliku tarkvara varamu:

.. code:: bash

    echo deb http://ftp.id.eesti.ee/pub/id/signed_repository/ubuntu precise main >
         /etc/apt/sources.list.d/ria-repository.list
    wget https://installer.id.ee/media/install-scripts/ria-public.key -O - |
         apt-key add -
    apt-get update
    apt-get install -y estonianidcard

Lisa Xsession skript mis näitab uut PCSC-lite sokkli asukohta:

.. code:: bash

    echo "export PCSCLITE_CSOCK_NAME=\$HOME/.pcscd.comm" > /etc/X11/Xsession.d/80-pcsclite

Loo terminali juurfailisüsteem:

.. code:: bash

    MIRROR="http://fi.archive.ubuntu.com/ubuntu/" \
    LANG=C \
    ARCH=i386 \
    ltsp-build-client

Sisene terminali juurfailisüsteemi:

.. code:: bash

    chroot /opt/ltsp/i386 /bin/bash

Lisa modifitseeritud OpenSSH klient ka terminali juurfailisüsteemi:

.. code:: bash

    echo "deb http://packages.koodur.com precise ltsp" | sudo tee /etc/apt/sources.list.d/v6sa-ltsp-hacks-precise.list
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B8A6153D   
    apt-get update
    apt-get install -y openssh-client

Paigalda muud ID-kaardi jaoks tarvilikud komponendid:

.. code:: bash

    apt-get install -y pcscd

Uues PC-SC Lite teegis käivitatakse pcscd deemon automaatselt, see ei sobi LTSP jaoks:

.. code:: bash

    sed -i "s/exit 0/#exit 0 # Reverted to 1.6.0 behaviour for LTSP/g" /etc/init.d/pcscd
    touch /etc/default/pcscd

Lisa SSH kliendi seadistused, asenda 192.168.77.1 oma serveri IP-ga:

.. code:: bash

    echo "Host 192.168.77.1
        RemoteForward [~/.pcscd.comm] :[/var/run/pcscd/pcscd.comm]" >> /etc/ssh/ssh_config

VIA terminalide UniChrome graafika tüürelite seis on suht halb seega ma lülitaks välja ka 3D kiirenduse:

.. code:: bash

    echo "Section \"Module\"
        Disable \"glx\"
        Disable \"dri\"
    EndSection" > /etc/X11/xorg.conf

Välju terminali juurikast:

.. code:: bash

    exit

Uuenda terminali juurfailisüsteemi SquashFS tõmmist:

.. code:: bash

    ARCH=i386 ltsp-update-image

NB! Ubuntu Unity on üsna uimane LTSP peal, soovitan valida Gnome Classic (No effects) sessioni sisselogimishalduris.

