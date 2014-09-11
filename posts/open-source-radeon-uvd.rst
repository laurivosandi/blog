.. title: Open-source Radeon Unified Video Decoder
.. date: 2013-07-08
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: Radeon, UVD, VDPAU, VA-API

Open-source Radeon Unified Video Decoder
========================================

This is a follow up for my previous post about hardware video decoding on AMD
Radeon. Phoronix writes that AMD had a huge codedrop for Radeon and
kernel/Mesa3D guys have been busy merging those changes. With Linux kernel 3.10,
upcoming Mesa 9.2 and proper firmware blob from AMD we should expect to see
AMD Radeon UVD (*Unified Video Decoder*) working with mostly open-source
software stack, thus freeing us from the buggy AMD Catalyst driver.

So first of all the kernel, Ubuntu 12.04 LTS (Precise Pangolin) features kernel 3.5 and Ubuntu 13.04 (Raring Ringtail) features kernel 3.8. In those cases you might try to fetch the 3.10 tarball and compile it yourself. Ubuntu 13.10 (Saucy Salamander) ships with 3.10 so no extra hassle there.

Secondly the Mesa driver, Ubuntu 13.10 feature freeze is not there yet, so we might see those Mesa changesets there eventually but currently you have to do a git clone and manually install from the source.
  
Thirdly and finally, the firmware - My Zacate based AMD E-450 processor featuring
Radeon 6320 graphics requires SUMO2_uvd.bin which should be placed in
/lib/firmware/radeon. In Ubuntu 13.10 the firmware blob seems to be there but
appearently any previous releases are missing it, fortunately you can fetch
the blobs from http://people.freedesktop.org/~agd5f/radeon_ucode/.

Following snippets assume Ubuntu 13.10 alpha installation:

Install Mesa dependencies:

.. code:: bash

    sudo apt-get install \
        build-essential \
        git \
        autoconf \
        bison \
        libxcb-xfixes0-dev \
        libudev-dev \
        libvdpau-dev \
        llvm \
        vdpauinfo
    sudo apt-get build-dep mesa
  
Clone Mesa Git repository:

.. code:: bash
  
    git clone git://anongit.freedesktop.org/mesa/mesa
  
Run autotools, configure and make:

.. code:: bash

    ./autogen.sh
    CFLAGS="-O3 -march=native" CXXFLAGS=$CFLAGS ./configure \
        --with-dri-drivers=radeon \
        --with-gallium-drivers=r600 \
        --enable-vdpau \
        --enable-glx-tls
    make -j4
    sudo make install

Reconfigure linker:

.. code:: bash

    echo -en "/usr/local/lib/dri\n/usr/local/lib/vdpau" | sudo tee /etc/ld.so.conf.d/vdpau-extra.conf
    sudo ldconfig

VLC shipped with Ubuntu does not support VDPAU, but *mplayer* with it's neat 
graphical user interface wrapper *smplayer* will do just fine:

.. code:: bash

    sudo apt-get install mplayer2 smplayer  

If you find that the HDMI audio output is disabled, try passing the Radeon kernel module extra argument:

.. code:: bash

    sudo sed -i -e 's/GRUB_CMDLINE_LINUX_DEFAULT="/GRUB_CMDLINE_LINUX_DEFAULT="radeon.audio=1 /g' /etc/default/grub
    sudo update-grub
    sudo reboot

Final step is to tell *mplayer* to pipe encoded video stream to the hardware decoder.
If you're going to use just the SMplayer frontend, set the video output driver to "vdpau".

.. code:: bash

    echo "vc=ffh264vdpau,ffmpeg12vdpau,ffvc1vdpau,ffwmv3vdpau" >> ~/.mplayer/config
    echo "vo=vdpau,xv" >> ~/.mplayer/config

The processor load for 1080p playback is neat 10-20% compared to the 30-60% of the 
proprietary AMD Catalyst and XvBA combo.

