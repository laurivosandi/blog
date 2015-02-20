.. published: 2014-11-06

Ubuntu 14.04 alglaadimine võrgust
=================================

Sissejuhatus
------------

Suvalise kaughaldussüsteemi kasutamine on mõistlik eelkõige serverite ning
pisut erinevate seadistustega masinate haldamisel.
Tööjaamade puhul on mõistlik iga tööjaam täpselt samade seadistustega teha.
Hoides juurfailisüsteemi NFS-serveris võib tööjaamadest kõvakettad eemaldada ning
arvutid võrgust tarkvara küsima panna PXE abil.
Käesolev juhend on läbi proovitud Ubuntu 14.04 amd64 serveri peal.
Selle sisse luuakse 14.04 i386 konteiner mis üle võrgu välja jagatakse.

Konteineri loomine ja seadistamine
----------------------------------

Loo Ubuntu 14.04 i386 konteiner:

.. code:: bash

    lxc-create -n workstation -t ubuntu -- -a i386 -r trusty
    lxc-start -n workstation

Sisene konteinerisse, paigalda Ubuntu töölaud ja välju:

.. code:: bash
    
    lxc-attach -n workstation -- apt-get install ubuntu-desktop linux-image-3.13.0 nfs-common

Lähtesta võrguseaded failis /var/lib/lxc/workstation/rootfs/etc/network/interfaces:

.. code::

    auto lo
    iface lo inet loopback

    auto eth0
    iface eth0 inet manual


Lähtesta /var/lib/lxc/workstation/rootfs/etc/fstab:

.. code::

    proc /proc proc defaults 0 0
    /dev/nfs / nfs defaults 1 1
    none /tmp tmpfs defaults 0 0
    none /run tmpfs defaults 0 0
    none /var/lock tmpfs defaults 0 0
    none /var/log tmpfs defaults 0 0
    none /var/lib/lightdm-data tmpfs defaults 0 0
    none /var/lib/lightdm tmpfs defaults 0 0
    none /var/tmp tmpfs defaults 0 0


Seadista initrd genereerimine ringi failis /var/lib/lxc/petsukas/rootfs/etc/initramfs-tools/initramfs.conf:

.. code:: bash

    MODULES=netboot
    COMPCACHE_SIZE=""
    COMPRESS=gzip
    BOOT=nfs
    DEVICE=
    NFSROOT=auto

Genereeri uued initrd failid:

.. code:: bash

    lxc-attach -n workstation -- update-initramfs -u -k all


Serveri seadistamine
--------------------
    
Alusmasinas paigalda TFTP, DHCP, DNS ja NFS serverid:

.. code:: bash

    apt-get install dnsmasq nfs-kernel-server pxelinux
    
Ekspordi juurfailisüsteem NFS-iga failis /etc/exports:

.. code:: bash
    
    /var/lib/lxc/workstation/rootfs 192.168.44.0/24(ro,no_root_squash)
    
Loo PXELINUX-i konfiguratsiooni jaoks kataloog:

.. code:: bash

    mkdir -p /var/lib/tftpboot/pxelinux.cfg

Ning sinna sisse /var/lib/tftpboot/pxelinux.cfg/default faili:

.. code::

    DEFAULT vesamenu.c32
    LABEL ubuntu-trusty-i386
    MENU LABEL Ubuntu 14.04 (32-bit)
    KERNEL /vmlinuz-3.13.0-39-generic
    APPEND /initrd=initrd.img-3.13.0-39-generic root=/dev/nfs nfsroot=192.168.44.1:/var/lib/lxc/petsukas/rootfs ro

Kopeeri PXELINUX alglaaduri tõmmis, tuum ja initrd:

.. code:: bash

    cp /usr/lib/PXELINUX/pxelinux.0 /var/lib/tftpboot/
    cp /usr/lib/syslinux/modules/bios/ldlinux.c32 /var/lib/tftpboot/
    cp /usr/lib/syslinux/modules/bios/vesamenu.c32 /var/lib/tftpboot/
    cp /usr/lib/syslinux/modules/bios/libcom32.c32 /var/lib/tftpboot/
    cp /usr/lib/syslinux/modules/bios/libutil.c32 /var/lib/tftpboot/
    cp -fv /var/lib/lxc/*/rootfs/boot/vmlinuz-* /var/lib/tftpboot/
    cp -fv /var/lib/lxc/*/rootfs/boot/initrd.img-* /var/lib/tftpboot/
    chmod 755 /var/lib/tftpboot/initrd.img-* /var/lib/tftpboot/vmlinuz*

Dnsmasq konfiguratsioon:

.. code:: ini

    user=nobody
    group=nogroup
    interface=eth1
    listen-address=192.168.44.1
    domain=nfsroot.koodur.com
    dhcp-range=192.168.44.100,192.168.44.200,12h
    dhcp-boot=pxelinux.0
    tftp-root=/var/lib/tftpboot
    enable-tftp

