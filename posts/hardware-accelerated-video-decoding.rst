.. title: AMD Radeon hardware video decoding
.. date: 2013-06-24 08:27:19
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: VA-API, VDPAU, VLC, Catalyst, Radeon

AMD Radeon hardware video decoding
==================================

I was looking for something
to house some good old 3.5" harddisks when I came across mini-ITX form factor.
I had to get a solid motherboard where to connect the disks and
after lots of browsing I decided to order Asus E45M1-I Deluxe motherboard
which fits nicely in a mini-ITX case.
This particular motherboard features AMD Dual-Core Processor E-450 with
AMD Radeon HD 6320 graphics. As a technology enthusiast I was also curious to
see how CPU+GPU fused into one chip performs. Of course this video chipset
is far from high-end but I think this marks the beginning of something greater -
in the following ten or twenty years we will see more and more
features synthesized into same chip. The x86 cores of this processor 
are rather slow but okay for everyday web browsing, but 1080p video playback
if definitely a no-no on the x86 cores alone.

The hardware video decoding on AMD Radeon video cards is unfortunately kind of sloppy.
After messing around couple of days I concluded that using Ubuntu 12.04.2 LTS
and AMD Catalyst 13.4 drivers results the least issues.
The ultimate buzzkill is that there is currently no fully open-source stack for 
video decoding for AMD Radeon video cards.
The open-source Gallium driver (*xserver-xorg-video-radeon*) performs well 3D-wise but there is no UVD (*Unified Video Decoder*) support.
As I've understood the GPGPU portion (*UVD and OpenCL*) of the AMD Radeon cards is only supported via AMD Catalyst drivers.
The Splitted Desktop's proprietary AMD Radeon XvBA (*X-Video Bitstream Acceleation*)
plugin for the open-source libva (*Video Acceleration API*) library is
pretty much unmaintained and that particular version (0.7.8) works properly
with the Xorg server version (1.11.3) shipped in Ubuntu 12.04.
On the Xorg version (1.13.3) shipped with Ubuntu 13.04 the video 
decoding acceleration seemed to work once, and for some reason the VLC 
was unable to initialize video decoder for any subsequent tries.
The *fglrx* package in Ubuntu 12.04 also seems to be somewhat outdated, even 
with *fglrx-updates* I experienced tearing/stutter in some cases.
The Unity desktop also lags horribly on AMD Radeon, therefore I switched to less
resource-hungry Cinnamon. Following snippets assume Ubuntu 12.04.2 LTS installation.

First of all get the AMD Catalyst driver:

.. code:: bash

    wget http://www2.ati.com/drivers/linux/amd-catalyst-13.4-linux-x86.x86_64.zip
    unzip amd-catalyst-13.4-linux-x86.x86_64.zip
    chmod +x amd-catalyst-13.4-linux-x86.x86_64.run

Optionally install Cinnamon:

.. code:: bash

    sudo add-apt-repository ppa:gwendal-lebihan-dev/cinnamon-stable
    sudo apt-get update
    sudo apt-get install cinnamon

Fetch build dependencies:

.. code:: bash

    sudo apt-get install \
        build-essential \
        cdbs \
        dh-make \
        dkms \
        execstack \
        dh-modaliases \
        fakeroot \
        libqtgui4 \
        lib32gcc1

Build and install the packages for Ubuntu:

.. code:: bash

    sudo sh ./amd-catalyst-13.4-linux-x86.x86_64.run \
        --buildpkg Ubuntu/precise
    sudo dpkg -i fglrx*.deb

Install XvBA driver and VLC:

.. code:: bash

    sudo apt-get install \
        xvba-va-driver \
        libva-glx1 \
        libva-x11-1 \
        vainfo \
        vlc

Reset xorg.conf, enable resize & rotate, enable H.264/MPEG-4 AVC level 5.1 support,
enable vsync to fix any video tearing issues and disable overscan to get rid of black borders:

.. code:: bash

    sudo amdconfig --initial -f
    sudo amdconfig --set-pcs-str="DDX,EnableRandR12,FALSE"
    sudo amdconfig --set-pcs-u32=MCIL,HWUVD_H264Level51Support,1
    sudo amdconfig --sync-video=on
    sudo amdconfig --set-pcs-val=MCIL,DigitalHDTVDefaultUnderscan,0

Reboot the machine and enjoy :)

For additional fine-tuning check out AMD Catalyst Control Center:

.. code:: bash

    sudo amdcccle
