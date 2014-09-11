.. title: Cubietruck over NFS
.. tags: Cubietruck, Allwinner, NFS, Debian, dnsmasq
.. date: 2014-08-21

Introduction
------------

In this post I'll attempt to explain how to set up Cubietruck with NFS root [#diskless-debian]_.
This means that Cubietruck won't store any files on it's internal NAND or µSD card,
instead files are stored on a single NFS server.
The obvious benefit is that software is managed centrally.

.. [#diskless-debian] http://www.iram.fr/~blanchet/tutorials/read-only_diskless_debian7.pdf

Setting up NFS server
---------------------

We assume that Cubietruck's root filesystem will be bootstrapped at /var/lib/cubietruck:

.. code:: bash

    sudo mkdir -p /var/lib/cubietruck

Next step is to install NFS server software:

.. code:: bash

    sudo apt-get install nfs-kernel-server

Add to /etc/exports:

.. code:: bash

    /home                 192.168.81.0/24(rw)
    /var/lib/cubietruck   192.168.81.0/24(ro,no_root_squash)
    
NFS services have to be reloaded of course:

.. code:: bash

    sudo /etc/init.d/nfs-kernel-server reload
    
Setting up DHCP server
----------------------

In this case we're using dnsmasq to serve IP addresses for the Cubietrucks.
The configuration at /etc/dnsmasq.conf should be something like this:

.. code:: ini

    user=nobody
    group=nogroup
    interface=eth1
    listen-address=192.168.81.1
    domain=term.koodur.com
    dhcp-range=192.168.81.130,192.168.81.180,12h
    dhcp-option=option:root-path,"192.168.81.1:/var/lib/cubietruck"


Bootstrapping base system
-------------------------

In this case we're building Debian Jessie ARM branch root filesystem at /var/lib/cubietruck.
First get all the tools to bootstrap a Debian system:

.. code:: bash

    sudo apt-get install debootstrap qemu-user-static binfmt-support

Next step is to actually run *debootstrap*, note that since the
target architecture differs we need to copy over binaries related to
QEMU compatibility layer:

.. code:: bash

    sudo debootstrap --foreign --arch=armhf jessie /var/lib/cubietruck
    sudo cp /usr/bin/qemu*-arm-static /var/lib/cubietruck/usr/bin/
    sudo chroot /var/lib/cubietruck /debootstrap/debootstrap --second-stage

Chrooting
---------

From now on we can assume all commands will take place inside /var/lib/cubietruck,
before entering the chroot you probably want to mount /proc and /dev/pts:

    mkdir -p /var/lib/cubietruck/dev/pts
    mount --bind /dev/pts /var/lib/cubietruck/dev/pts
    mount --bind /proc /var/lib/cubietruck/proc/
    mount --bind /home /var/lib/cubietruck/home/
    
To make it more permantent you can add following to your host machine's /etc/fstab:

.. code::

    /dev/pts	/var/lib/cubietruck/dev/pts none bind 0 2
    /proc		/var/lib/cubietruck/proc none bind 0 2
    /home		/var/lib/cubietruck/home none bind 0 2
    
Then you can enter /var/lib/cubietruck simply by chrooting into that directory:

.. code:: bash

    chroot /var/lib/cubietruck
    
Create /etc/mtab:

.. code:: bash

    ln -s /proc/self/mounts /etc/mtab
    
Create /etc/resolv.conf:

.. code::

    nameserver 8.8.8.8
    
Debootstrap does not set any mountpoints so /etc/fstab has to be reconfigured:

.. code::

    proc /proc proc defaults 0 0
    /dev/nfs / nfs nolock 0 0
    none /tmp tmpfs defaults 0 0
    none /var/tmp tmpfs defaults 0 0
    none /var/lib/lightdm tmpfs defaults 0 0
    none /media tmpfs defaults 0 0
    none /var/log tmpfs defaults 0 0
    192.168.81.1:/home /home nfs nolock 1 2

    # Hide internal NAND mounting options from GUI    
    /dev/nand1 /mnt/nand1 auto noauto 1 2
    /dev/nand2 /mnt/nand2 auto noauto 1 2
    /dev/nanda /mnt/nanda auto noauto 1 2
    /dev/nandb /mnt/nandb auto noauto 1 2

Same applies to /etc/apt/sources.list:

.. code::

    deb http://ftp.ee.debian.org/debian/ jessie main
    deb-src http://ftp.ee.debian.org/debian/ jessie main

    deb http://security.debian.org/ jessie/updates main
    deb-src http://security.debian.org/ jessie/updates main

    # jessie-updates, previously known as 'volatile'
    deb http://ftp.ee.debian.org/debian/ jessie-updates main
    deb-src http://ftp.ee.debian.org/debian/ jessie-updates main

    # jessie-backports, previously on backports.debian.org
    deb http://ftp.ee.debian.org/debian/ jessie-backports main
    deb-src http://ftp.ee.debian.org/debian/ jessie-backports main

To get some extra junk you probably want to add my repository aswell:

.. code:: bash

    echo "deb http://packages.koodur.com jessie main" > /etc/apt/sources.list.d/koodur.list
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B8A6153D
    
And finally update package lists:

.. code:: bash

    apt-get update


Installing software for Cubietruck
----------------------------------

Following installs MATE desktop with all the bells and whistles:

.. code:: bash

    apt-get install nfs-common locales lightdm \
        mate-desktop-environment mate-media-pulse mate-settings-daemon-pulse pulseaudio \
        vdpauinfo libvdpau-sunxi libump xf86-video-fbturbo mpv estonianidcard \
        chromium-browser chromium-browser-l10n chromium-codecs-ffmpeg-extra \
        libreoffice libreoffice-l10n-et \
        mc htop iftop iotop nmap ntpdate alsa-utils
        
Reconfigure locales and timezones:

.. code:: bash

    dpkg-reconfigure locales
    dpkg-reconfigure tzdata
    
To get Bluetooth, WiFi and CedarX working fetch kernel modules:

.. code:: bash

    wget http://cdimage.koodur.com/cubietruck-kernel-mods.tar
    tar xvf cubietruck-kernel-mods.tar -C /lib/
    depmod  -a 3.4.98-sun7i+

Define modules to be loaded during boot at /etc/modules:

.. code::

    hci_uart
    gpio_sunxi
    bt_gpio
    wifi_gpio
    rfcomm
    hidp
    lirc_gpio
    sunxi_lirc
    #bcmdhd
    sunxi_ss

To make mpv default to hardware accelerated decoding, insert following to /etc/mpv/mpv.conf:

.. code:: ini

    vo=vdpau
    hwdec=vdpau
    hwdec-codecs=h264
    
To /etc/rc.local:

.. code:: bash

    chmod 777 /dev/g2d
    chmod 777 /dev/disp
    chmod 777 /dev/cedar_dev
    exit 0
   

To /etc/X11/xorg.conf:

.. code::

Section "Screen"
    Identifier  "VGA-0"
    Device      "/dev/fb0"
    Monitor     "LG"
EndSection

Section "Screen"
    Identifier  "HDMI-0"
    Device      "/dev/fb1"
    Monitor     "LG"
EndSection

Section "Device"
    Identifier  "/dev/fb0"
    Driver      "fbturbo"
    Option      "fbdev" "/dev/fb0"
    Option      "SwapBuffersWait" "true"
EndSection

Section "Device"
    Identifier  "/dev/fb1"
    Driver      "fbturbo"
    Option      "fbdev" "/dev/fb1"
    Option      "SwapBuffersWait" "true"
EndSection

To install Adobe Flash 11.5 [#flash]_:

.. code:: bash

    wget http://www.dl.cubieboard.org/media/flashplayerarm.tar.gz
    tar xvf flashplayerarm.tar.gz
    mv libpepflashplayer.so /usr/lib/chromium-browser/plugins/
    mv default etc/chromium-browser/default
    rm -fv flashplayerarm.tar.gz

.. [#flash] http://docs.cubieboard.org/tutorials/common/begining_on_lubuntu#flashplayer

Preparing Cubietruck
--------------------

At some point Cubietruck switched using from revision A of A20 processor to
revision B. Many scripts don't work currently with rev B [#revb]_ and the
suggested way to fix several NAND partitioning issues is to reflash Cubietruck
with official Lubuntu v2.0 image and then proceed with other installation methods. 

.. code:: bash

    wget http://dl.cubieboard.org/software/a20-cubietruck/lubuntu/ct-lubuntu-nand-v2.0/ct-lubuntu-server-nand.img.gz
    tar xvf ct-lubuntu-server-nand.img.gz

To install the image use LiveSuit:

.. code:: bash

    wget http://dl.cubieboard.org/software/tools/livesuit/LiveSuitV306_For_Linux64.zip
    unzip LiveSuitV306_For_Linux64.zip
    cd LiveSuit_for_Linux64/
    chmod +x LiveSuit.run
    ./LiveSuit.run
    sudo ~/Bin/LiveSuit/LiveSuit.sh
    
And point the program to the .img file uncompressed earlier.
Once the machine has booted up you can gain access to the commandline via UART header on the board.
Substitute kernel and boot arguments and reboot the machine:

.. code:: bash

    mount /dev/nanda /boot
    wget http://lauri.vosandi.com/ct/ct-vga.bin -O /boot/script.bin
    wget http://lauri.vosandi.com/ct/uImage -O /boot/uImage
    wget http://lauri.vosandi.com/ct/uEnv.ct -O /boot/uEnv.txt
    reboot
    
uImage and ct-vga.bin are directly from Igor Pečovnik's µSD image [#igor]_.
The last file is slightly customized u-boot configuration:

.. code:: ini

    console=tty0
    extraargs=console=ttyS0,115200 root=/dev/nfs ip=dhcp ro panic=60
    nand_root=/dev/nandb

.. [#revb] http://dl.cubieboard.org/software/a20-cubietruck/android/README
.. [#igor] http://www.igorpecovnik.com/2013/12/24/cubietruck-debian-wheezy-sd-card-image/

In case icons are missing it usually means chrooted package installation failed for some packages.
Try mounting rootfs read-write on a Cubietruck and run:

.. code:: bash

    /usr/lib/arm-linux-gnueabihf/gdk-pixbuf-2.0/gdk-pixbuf-query-loaders --update-cache

