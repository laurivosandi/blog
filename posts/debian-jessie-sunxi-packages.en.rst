.. title: Debian Jessie packages for Cubieboard and Cubietruck
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. date: 2014-04-04
.. tags: Debian, sunxi, Cubietruck, Cubieboard, VDPAU, SmartCard, PKCS#11, CedarX, OpenSC, VA-API

Debian Jessie packages for Cubieboard and Cubietruck
====================================================

Introduction
------------

Over past months I've been working hard to get the
Debian running on my
`Cubietruck <cubietruck-demo.html>`_ with all the bells and whistles.
I wanted to have usable Chromium, hardware accelerated video playback,
MATE desktop and full Estonian ID-card support.

.. figure:: http://nas.koodur.com/~lauri/public/Photos/Cubieboard/hypercubie.jpg
    :width: 80%

    Cubietruck running Chromium, Estonian ID-card utility and playing back 720p video stream


Basics
------

I used build script from 
`Igor Pečovnik <http://www.igorpecovnik.com/>`_ which includes
wireless drivers as the basis for root filesystem.
Of course I replaced *wheezy* with *jessie* and tweaked the script to fit my needs.
Unfortunately MATE packages are not there yet for Debian and
VDPAU drivers haven't been packaged aswell.
Chromium packaging seems to be quite broken in Debian armel/armhf branch generally.
To build my packages I used pbuilder in conjunction with QEMU ARM emulation.


Adding repository
-----------------

Just add following to your Debian Jessie root filesystem /etc/apt/sources.list:

.. code:: bash

    echo "deb http://packages.koodur.com jessie main" | \
        sudo tee /etc/apt/sources.list.d/koodur.list
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B8A6153D


Video decoding acceleration
---------------------------

Cubieboard2 and Cubietruck both support 4K video decoding.
Open-source software stack is finally available for 
video decoding using `CedarX <http://linux-sunxi.org/CedarX/Reverse_Engineering>`_.
        
To enable VDPAU video decoding acceleration install VDPAU driver,
libump for shared memory access and fbturbo driver for Xorg:

.. code:: bash

    sudo apt-get install vdpauinfo libvdpau-sunxi libump xf86-video-fbturbo

Make sure you can access the kernel driver from userspace by adding following to
*/etc/rc.local*:

.. code:: bash

    chmod 777 /dev/g2d
    chmod 777 /dev/disp
    chmod 777 /dev/cedar_dev
    exit 0


You also need to fine-tune /etc/xorg.conf so fbturbo Xorg driver would be used:

.. code::

    Section "Screen"
        Identifier  "VGA-0"
        Device      "/dev/fb0"
        Monitor     "LG"
        Option      "DPMS" "false"
    EndSection

    Section "Screen"
        Identifier  "HDMI-0"
        Device      "/dev/fb1"
        Monitor     "LG"
        Option      "DPMS" "false"
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

mpv
---
    
As a video player I strongly suggest mplayer's successor mpv
which is already available in Debian Jessie.
It supports VDPAU and VA-API video acceleration backends and streaming over HTTPS:

.. code:: bash

    sudo apt-get install mpv
    
You probably want to put following in */etc/mpv/mpv.conf* aswell:

.. code:: ini

    vo=vdpau
    hwdec=vdpau
    hwdec-codecs=h264
    
sunxi-tools
-----------

The sunxi-tools package versioning hasn't settled yet, but prelimiary
package which contains *fex2bin*, *bin2fex* and *nand-part* utils is available:

.. code:: bash

    sudo apt-get install sunxi-tools
    
MATE desktop
------------

Some MATE desktop 1.8 packages have landed in Debian Jessie.
I backported the remaining ones aswell so the well known command to install
MATE desktop works:

.. code:: bash

    sudo apt-get install mate-desktop-environment \
        xorg lightdm \
        network-manager network-manager-gnome \
        mate-media-pulse mate-settings-daemon-pulse pulseaudio
    
Pulseaudio switching between HDMI and analog output seems to work well.
SPDIF also shows up, but unfortunately I haven't got audio equipment to test it with.

Chromium
--------

Iceweasel aka Firefox is availabe in Debian repositories but it's rather
bloated for Cubieboard.
I managed to backport Chromium from Ubuntu repositories to Debian Jessie.
Interestingly the Chromium build on Debian Wheezy crashed with segfault.
I tried to dig deeper but eventually gave up since it works perfectly on Debian Jessie:

.. code:: bash

    sudo apt-get install chromium-browser
    
Of course hardware accelerated video decoding is not supported in
Chromium (yet!)

Estonian ID-card
----------------

Packages are available, simply issue:

.. code:: bash

    sudo apt-get install estonianidcard

I also included a Bash snippet that automagically enables ID-card support for
Chromium.


Summary
-------
There are still several things I haven't figured out exactly:
the Lima open-source 3D driver should be ready for Cubietruck really soon and
I did not manage to get the Bluetooth firmware loaded to the Bluetooth chip just yet.

Nevertheless Cubietruck loaded with this packages is pretty neat desktop replacement
if you use desktop to mainly work on remote servers,
use plain text editor to code, watch movies and listen to music.

Once Lima drivers and Wayland are ready it should be a matter of recompiling
MATE packages to use Wayland so it should be possible to have really smooth
MATE desktop experience on top of OpenGL ES.

