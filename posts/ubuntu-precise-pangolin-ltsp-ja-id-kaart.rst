.. title: Ubuntu 12.04, LTSP ja ID-kaart
.. date: 2012-07-28 10:19:03
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: LTSP, Ubuntu, Debian, Cubietruck, PKCS#11, OpenSC, pcscd, PCSC-Lite, OpenSC, ID-card, ID-kaart, NFS, nbd, OpenSSH

Ubuntu 12.04, LTSP ja ID-kaart
==============================

Juhend eeldab `Ubuntu 12.04 desktop või server <http://releases.ubuntu.com/12.04.5/>`_  paigaldust.

Serveri seadistamine
--------------------

Esiteks uuenda pakette:

.. code:: bash

    apt-get update
    apt-get dist-upgrade

Paigalda LTSP serveri metapakett, see paigaldab DHCP serveri ja muud LTSP jaoks tarvilikud teenused:

.. code:: bash

    apt-get install ltsp-server-standalone wget ca-certificates apt-transport-https

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

    echo "deb http://packages.koodur.com precise ltsp" | sudo tee /etc/apt/sources.list.d/koodur-ltsp-packages.list
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B8A6153D
    apt-get update
    apt-get install -y openssh-server

Lisa Eesti ID-kaardi ametliku tarkvara varamu:

.. code:: bash

    echo "deb https://installer.id.ee/media/ubuntu/ precise main" > /etc/apt/sources.list.d/ria-repository.list
    wget https://installer.id.ee/media/install-scripts/ria-public.key -O - | apt-key add -
    apt-get update
    apt-get install -y estonianidcard

Lisa Xsession skript mis näitab uut PCSC-lite sokkli asukohta:

.. code:: bash

    echo "export PCSCLITE_CSOCK_NAME=\$HOME/.pcscd.comm" > /etc/X11/Xsession.d/80-pcsclite

    
PXE-võimelise terminali tarkvara seadistamine
---------------------------------------------

Võrgu kaudu alglaadimist võimaldavad enamus x86 masinaid millel on vähegi modernne võrgukaart.
Esiteks loo terminali juurfailisüsteem:

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

    echo "deb http://packages.koodur.com precise ltsp" | sudo tee /etc/apt/sources.list.d/koodur-ltsp-packages.list
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B8A6153D   
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


Cubietruckide kasutamine terminalina
------------------------------------

Terminalina saab väga edukalt kasutada ka Cubietrucki.
Teoorias peaks saama ltsp-build-image skripti abil luua ka armhf SquashFS tõmmiseid
mida terminal siis nbd abil monteeriks nagu LTSP5-s tavaks aga käesolev juhend
tugineb hoopis NFS tehnoloogiale.
Esiteks paigalda serverisse armhf emulatsioonikiht:

.. code:: bash

    sudo apt-get install qemu-user-static binfmt-support

Sikuta Ubuntu 12.04 armhf juurfailisüsteem:

.. code:: bash

    wget -c http://s3.armhf.com/dist/basefs/ubuntu-precise-12.04.4-armhf.com-20140603.tar.xz
    sudo mkdir -p /opt/ltsp/cubietruck
    sudo tar xvf ubuntu-precise-12.04.4-armhf.com-20140603.tar.xz -C /opt/ltsp/cubietruck
    sudo cp /usr/bin/qemu*-arm-static /opt/ltsp/cubietruck/usr/bin/
    
Lisa serveri SSH võti:

.. code:: bash

    ltsp-update-sshkeys
    
Ekspordi kataloog NFS serveriga failis **/etc/exports**:

.. code::

    /opt/ltsp/cubietruck   192.168.77.0/24(ro,no_root_squash)
    
Paigalda NFS server:

.. code:: bash

    sudo apt-get install nfs-kernel-server

Sisene Cubietrucki juurfailisüsteemi:

.. code:: bash

    sudo mount --bind /proc /opt/ltsp/cubietruck/proc
    sudo mount --bind /dev /opt/ltsp/cubietruck/dev
    sudo mount --bind /dev/pts /opt/ltsp/cubietruck/dev/pts
    sudo chroot /opt/ltsp/cubietruck

LDM-i ning sessiooni vaikimisi keele seadmiseks kasuta /etc/default/locale faili.
Paraku praegu eestikeelsed tõlked puuduvad LDM-il endal ning seetõttu on sisselogimisviip
inglisekeelne:

.. code:: bash

    echo 'LANG="et_EE.UTF-8"' > /etc/default/locale

Lähtesta võrguseaded failis /etc/network/interfaces:

.. code::

    auto lo
    iface lo inet loopback
    
Lähtesta nimeserver:

.. code:: bash

    echo "nameserver 8.8.8.8" | tee /etc/resolv.conf
    
Paigalda Igori kerneli moodulid:

.. code:: bash

    wget http://lauri.vosandi.com/ct/mod.tar
    tar xvf mod.tar -C /
    depmod  -a 3.4.98-sun7i+
    
Lisa minu tarkvara varamu:

.. code:: bash

    echo "deb http://packages.koodur.com precise main ltsp" > /etc/apt/sources.list.d/koodur.list
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B8A6153D
    
Uuenda pakettide nimekirju:

.. code:: bash

    apt-get update
    
Paigalda kohandatud OpenSSH, PCSC-deemon, LTSP-kliendi metapakett ja muu tilu-lilu:
    
.. code:: bash

    apt-get install -y openssh-client pcscd ltsp-client python-pip python-newt python-tz sunxi-tools xf86-video-fbturbo
    pip install socle
    
Uues PC-SC Lite teegis käivitatakse pcscd deemon automaatselt, see ei sobi LTSP jaoks:

.. code:: bash

    sed -i "s/exit 0/#exit 0 # Reverted to 1.6.0 behaviour for LTSP/g" /etc/init.d/pcscd
    touch /etc/default/pcscd
    
Seadista /etc/fstab:

.. code::

    proc /proc proc defaults 0 0
    none /tmp tmpfs defaults 0 0
    none /run tmpfs defaults 0 0
    none /var/lock tmpfs defaults 0 0
    none /var/log tmpfs defaults 0 0
    none /var/tmp tmpfs defaults 0 0
    


Lisa SSH kliendi seadistused, et terminal võimaldaks serveris ligipääsu terminalis jooksvale PCSC deemonile,
asenda 192.168.77.1 oma serveri IP-ga:

.. code:: bash

    echo "Host 192.168.77.1 server
        RemoteForward [~/.pcscd.comm] :[/var/run/pcscd/pcscd.comm]" >> /etc/ssh/ssh_config
    
Kui sisselogimishalduri aken ei ilmu ja jääb tsükklisse siis proovi jooksutada 
järgnevat käsku. Ubuntu 12.04 + qemu koosluses näiteks see käsk ei jookse, nii
et seda peaks korraks Cubietrucki raual otse käitama:

.. code:: bash

    /usr/lib/arm-linux-gnueabihf/gdk-pixbuf-2.0/gdk-pixbuf-query-loaders --update-cache
    
Kui sisselogimishaldur ei käivitu kontrolli, et masinanimi *server* lahenduks
LTSP serveri IP aadressiks.
Selle jaoks võib olla tarvis seadistada /etc/hosts faili.


Cubietrucki ette valmistamine
-----------------------------

Kuna PXE on x86 platvormi spetsiifiline siis säärast võimekust näiteks
Cubietrucki kasutada ei saa. Teoorias saaks u-booti kompileerida TFTP toega
nii et analoogselt PXE-le saaks Cubietrucki tegelikult panne kernelit laadima võrgust
aga Cubietrucki u-boot on üsna toores ning see eeldab võrgukaardi minimaalset tuge u-bootis.
Käesolev peatükk räägib peamiselt sellest kuidas kernel Cubietrucki sisemisele
mälule kirjutada ning võrgust juurfailisüsteemi haakima panna.

Ette valmistamiseks paigalda Cubietruckile LiveSuit abil Lubuntu tõmmis,
see keerab partitsioonitabeli õigeks muidu on alglaadimisega mingisugused anomaaliad:

.. code:: bash

    wget http://dl.cubieboard.org/software/a20-cubietruck/lubuntu/ct-lubuntu-nand-v2.0/ct-lubuntu-server-nand.img.gz
    tar xvf ct-lubuntu-server-nand.img.gz
    wget http://dl.cubieboard.org/software/tools/livesuit/LiveSuitV306_For_Linux64.zip
    unzip LiveSuitV306_For_Linux64.zip
    cd LiveSuit_for_Linux64/
    chmod +x LiveSuit.run
    ./LiveSuit.run
    sudo ~/Bin/LiveSuit/LiveSuit.sh

Kui Cubietruck on käima läinud ühenda UART-USB sillaga end käsurea külge ja 
paigalda Igori kernel, moodulid ja kohandatud alglaaduri argumendid:

.. code:: bash

    mount /dev/nanda /boot
    wget http://lauri.vosandi.com/ct/ct-vga.bin -O /boot/script.bin
    wget http://lauri.vosandi.com/ct/uImage -O /boot/uImage
    wget http://lauri.vosandi.com/ct/uEnv.ct -O /boot/uEnv.txt
    
Viimane neist sisaldab midagi järgnevat, mis sunnib kerneli küsima DHCP-ga IP-aadressi,
seejärel alglaadimist tegema DHCP serveri poolt ette antud NFS-serverist ning
käivitama LTSP initit.

.. code:: ini

    console=tty0
    extraargs=console=ttyS0,115200 root=/dev/nfs ip=dhcp ro panic=60 /sbin/init-ltsp
    nand_root=/dev/nandb

