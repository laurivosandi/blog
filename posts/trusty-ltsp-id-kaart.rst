.. published: 2014-10-30
.. flags: hidden

Cubietruckide kasutamine terminalina
------------------------------------

Terminalina saab väga edukalt kasutada ka Cubietrucki.
Teoorias peaks saama ltsp-build-image skripti abil luua ka armhf SquashFS tõmmiseid
mida terminal siis nbd abil monteeriks nagu LTSP5-s tavaks aga käesolev juhend
tugineb hoopis NFS tehnoloogiale.
Esiteks paigalda serverisse armhf emulatsioonikiht:

.. code:: bash

    sudo apt-get install qemu-user-static binfmt-support
    
Nüüd saad debootstrappida amd64 masina peal jessie armhf haru:

.. code:: bash

    sudo debootstrap --foreign --arch=armhf testing /opt/ltsp/cubietruck
    sudo cp /usr/bin/qemu*-arm-static /opt/ltsp/cubietruck/usr/bin/
    sudo chroot /opt/ltsp/cubietruck /debootstrap/debootstrap --second-stage
    
Lisa serveri SSH võti:

.. code:: bash

    sudo mkdir -p /opt/ltsp/cubietruck/etc/ssh/
    ssh-keyscan 192.168.77.1 server | sudo tee /opt/ltsp/cubietruck/etc/ssh/ssh_known_hosts
    
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
    
Loo mtab:

.. code:: bash

    ln -s /proc/self/mounts /etc/mtab
    
Kohanda Cubietrucki tarkvara varamuid failis **/etc/apt/sources.list**:

.. code::

    deb http://ftp.ee.debian.org/debian/ jessie main
    deb http://security.debian.org/ jessie/updates main
    deb http://ftp.ee.debian.org/debian/ jessie-updates main
    deb http://ftp.ee.debian.org/debian/ jessie-backports main

Lisa minu tarkvara varamu:

.. code:: bash

    echo "deb http://packages.koodur.com jessie main ltsp" > /etc/apt/sources.list.d/koodur.list
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B8A6153D
    
Pinni minu OpenSSH pakett. Ubuntu 12.04 pcscd versioon on niivõrd vana, et
jessie libpcsclite ei suuda temaga rääkida. Minu varamus on 12.04-st
porditud pcscd ja libccid:

.. code:: bash

    echo -en "Package: openssh-client\nPin: version 1:5.9p1-5ubuntu1.4koodur0\nPin-Priority: 900\n" > \
        /etc/apt/preferences.d/openssh-client.pref
    echo -en "Package: pcscd\nPin: version 1.7.4-2ubuntu2\nPin-Priority: 900\n" > \
        /etc/apt/preferences.d/pcscd.pref
    echo -en "Package: libccid\nPin: version 1.4.5-1\nPin-Priority: 900\n" > \
        /etc/apt/preferences.d/libccid.pref
    
Uuenda pakettide nimekirju:

.. code:: bash

    apt-get update
    
Paigalda kohandatud OpenSSH, PCSC-deemon, LTSP-kliendi metapakett ja muu tilu-lilu:
    
.. code:: bash

    apt-get install -y openssh-client pcscd ltsp-client python-pip python-newt python-tz sunxi-tools
    pip install socle
    
Uues PC-SC Lite teegis käivitatakse pcscd deemon automaatselt, see ei sobi LTSP jaoks:

.. code:: bash

    sed -i "s/exit 0/#exit 0 # Reverted to 1.6.0 behaviour for LTSP/g" /etc/init.d/pcscd
    touch /etc/default/pcscd

Lisa SSH kliendi seadistused et terminal võimaldaks serveris ligipääsu terminalis jooksvale PCSC deemonile,
asenda 192.168.77.1 oma serveri IP-ga:

.. code:: bash

    echo "Host 192.168.0.1 server
        RemoteForward [~/.pcscd.comm] :[/var/run/pcscd/pcscd.comm]" >> /etc/ssh/ssh_config
    
Kui sisselogimishalduri aken ei ilmu ja jääb tsükklisse siis proovi jooksutada 
järgnevat käsku. Ubuntu 12.04 + qemu koosluses näiteks see käsk ei jookse, nii
et seda peaks korraks Cubietrucki raual otse käitama:

.. code:: bash

    /usr/lib/arm-linux-gnueabihf/gdk-pixbuf-2.0/gdk-pixbuf-query-loaders --update-cache
    

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
    extraargs=console=ttyS0,115200 root=/dev/nfs ip=dhcp ro panic=60 init=/sbin/init-ltsp
    nand_root=/dev/nandb


