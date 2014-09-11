.. title: Installing Debian
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. date: 2014-02-11
.. tags: Debian, MATE, VLC, fontconfig, tearing, Intel

Installing Debian
=================

Introduction
------------

Debian is a GNU/Linux distribution with a long history.
At any time given there are three releases of Debian available:
*stable*, *testing* and *unstable*.
As of this writing *wheezy* is labeled as *stable* and
*jessie* is labeled as *testing*.
The *stable* branch is known for being stable and secure but that comes with the price
of having not so up to date packages.
The *testing* branch usually has more up to date packages but you might
stuble upon some broken package.

For servers *stable* branch is reccommended.
For desktops and laptops you might have to upgrade some packages
to *testing*.
Even if you're attempting to install *testing* version of Debian,
picking the installer of *stable* version is a safe bet.
Occasionally *testing* images is broken.


Downloading
-----------

The easiest way to download Debian is to use the network install ISO:

.. code:: bash

    # Download Debian 7.3.0 amd64 netinstaller
    wget -c http://cdimage.debian.org/debian-cd/7.3.0/multi-arch/iso-cd/debian-7.3.0-amd64-i386-netinst.iso

Once you've got it, just become root and *cat* it to a memory stick:

.. code:: bash

    # Become root
    sudo -s
    
    # Remember to unmount any filesystems from the memory stick first.
    umount /dev/sdz*
    
    # Write ISO to memory stick
    cat debian-7.3.0-amd64-i386-netinst.iso > /dev/sdz
    
    # Make sure buffers are emptied before you pull out the memory stick
    sync

Installing
----------

Plug in the memory stick to the machine and boot from it.
The installer should be quite straightforward.
The BtrFS should be quite stable now and you can install root filesystem
on BtrFS formatted filesystem.
Note that most packages are installed off the internet with this ISO so
it is recommended to hook your machine up with an ethernet cable.
Unlike Ubuntu Debian does not contain any closed-source firmware blobs
so to perform installation over WiFi you might need to copy your
wireless card firmware from some other machine first.

Once the installation has completed and you've booted into your new system
you're most probably greeted with a command line if you didn't select graphical
interface in the installer.

Setting up OpenSSH server
-------------------------

OpenSSH server makes life much easier because you can use any other machine
to connect to the newly installed Debian box.

.. code:: bash

    sudo apt-get install openssh-server
    
Now you can use OpenSSH or Putty to connect from any other machine and
copy-paste stuff off this page ;)

    
Installing utils
----------------

Installing utilities that make life easier:

.. code:: bash

    sudo apt-get install -y \
        pciutils usbutils \
        lsb-release \
        acpitool \
        hdparm sdparm smartmontools \
        screen byobu \
        mc rsync \
        htop iptraf iotop iftop mtr nmap


Installing wireless chipset firmware
------------------------------------

As said, Debian doesn't ship with wireless chipset firmware by default
because most of them are closed-source.
To install firmware for Intel, Ralink, Realtek and others alike the
non-free repository has to be enabled:

.. code:: bash

    echo "deb http://ftp.de.debian.org/debian/ wheezy non-free" | \
        sudo tee /etc/apt/sources.list.d/non-free.list
    sudo apt-get update
    sudo apt-get install firmware-linux firmware-linux-nonfree \
        firmware-atheros firmware-brcm80211 firmware-libertas \
        firmware-ralink firmware-realtek zd1211-firmware

This applies to most Lenovo Thinkpad laptops.


Installing MATE desktop
-----------------------

Personally I'm dissapointed in KDE4, GNOME3 and Unity desktop environments.
MATE desktop evnironment continues the traditions of GNOME2 desktop.
MATE desktop provides anything you expect to work out-of-box on modern hardware:
wired/wireless network interface management, setting up Bluetooth keyboard/mouse,
mounting USB disks, volume control etc.

.. code:: bash


    wget -q http://repo.mate-desktop.org/debian/mate-archive-keyring.gpg -O- | sudo apt-key add -
    echo "deb http://packages.mate-desktop.org/repo/debian wheezy main" | \
        sudo tee /etc/apt/sources.list.d/mate-desktop.list
    sudo apt-get update
    sudo apt-get install mate-desktop-environment-extra \
        ntp \
        lightdm \
        network-manager network-manager-gnome \
        mate-media-pulse mate-settings-daemon-pulse \
        gedit gedit-plugins
        
If you use Bluetooth audio headset, have HDMI audio output,
want to play audio from remote source (laptop) or to remote sink (desktop),
need to switch inputs/outputs runtime or change volume per application
then you also might want to install PulseAudio:

.. code:: bash

    sudo apt-get install -t wheezy-backports \
        pulseaudio \
        pulseaudio-module-zeroconf \
        pulseaudio-module-bluetooth \
        pulseaudio-esound-compat \
        pulseaudio-utils \
        pavucontrol \
        paprefs

Once you've installed graphical user interface you might notice that
Debian installer left some entries about memory stick in the */etc/fstab*,
you probably have to remove them in order for the regular user to have
write access to USB memory sticks:

.. code::

    /dev/sdc1       /media/usb0     auto    rw,user,noauto  0       0
    /dev/sdc2       /media/usb1     auto    rw,user,noauto  0       0

I prefer to have Bluetooth disabled by default, you may still enable
it from the Bluetooth icon in the notification area:

.. code:: bash

    sudo sed /etc/default/bluetooth -i -e 's/BLUETOOTH_ENABLED=1$/BLUETOOTH_ENABLED=0/g'

    
Tiling window management
------------------------

Coming from Ubuntu you will probably miss the maximize, maximize left, maximize
right gestures you can do with dragging a window to the edge of a screen.
MATE desktop 1.8 will have that features, but 1.6 shipped in Debian repositories
does not include that yet. There is a
`quicktile <https://github.com/ssokolow/quicktile>`_ Python snippet which 
allows configuring Super+Left, Super+Right, Super+Up shortcuts to emulate
similar behaviour:

.. code:: bash

    echo "
    [general]
    cfg_schema = 1
    UseWorkarea = True
    ModMask = <Mod4>

    [keys]
    Up = maximize
    Left = left
    Right = right
    " > .config/quicktile.cfg

And launch it in every session by:

.. code:: bash

    echo "python quicktile.py -b &" >> ~/.xsession


Installing OpenOffice/LibreOffice
---------------------------------

OpenOffice has been deprecated in favour for LibreOffice:

.. code:: bash

    sudo apt-get install libreoffice
    
Installing Firefox
------------------

Since Debian wishes to provide optimized executable for their particular library
stack they had to compile their own version of Firefox. Unfortunately Mozilla
Corporation didn't allow Firefox branding for such binary.
Therefore in Debian you have to get along with Iceweasel which essentially is
unbranded version of Firefox:

.. code:: bash

    sudo apt-get install iceweasel

Installing Google Chrome
------------------------

Google Chrome is not distributed within Debian repositories because of various reasons.
You can install Google Chrome by adding it's repository. This of course only
works on x86 so Raspberry Pi and Cubieboard are out:

.. code:: bash

    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" | \
        sudo tee /etc/apt/sources.list.d/google-chrome.list
    sudo apt-get update
    sudo apt-get install google-chrome-beta
    
Chromium is the open-source project behind Google Chrome.
Unlike Google Chrome it does not support MP3 for HTML5 audio out-of-box.
Chromium is included in the main Debian repository:

.. code:: bash

    sudo apt-get install chromium
    
Note that Chromium builds on Debian *armel/armhf* are broken for some reason.

Installing Adobe Flash
----------------------

Adobe Flash is a potential backdoor for your Linux box so
installing it is strongly discouraged, instead you should
`switch Youtube to HTML5 <http://www.youtube.com/html5>`_.
If that is not enough you can install Adobe Flash by:

.. code:: bash

    apt-get install flashplugin-nonfree

Installing Oracle VirtualBox
----------------------------

I needed VirtualBox with USB forwarding support. This is unfortunately available
only with the closed-source extension pack available from Oracle.
The easiest way to install VirtualBox maintained by Oracle is to add
the proper APT repositories:

.. code:: bash

    wget -q http://download.virtualbox.org/virtualbox/debian/oracle_vbox.asc -O- | sudo apt-key add -
    echo "deb http://download.virtualbox.org/virtualbox/debian wheezy contrib" | \
            sudo tee /etc/apt/sources.list.d/oracle-virtualbox.list
    sudo apt-get update
    sudo apt-get install -y virtualbox-4.3
    
If you're certain that the open-source edition is good enough for you, just issue:

.. code:: bash

    sudo apt-get install virtualbox-ose

If you need userspace emulation to run binaries for other architectures then you might want to try out
QEMU userspace emulation:

.. code:: bash

    sudo apt-get install qemu-user


Installing GIMP

You may try to run Adobe Photoshop with *wine*, it actually runs
quite well but GIMP is enough for me. Besides with latest *gimp*
versions you can switch it to single-windowed mode (Windows -> Single-Window Mode):

.. code:: bash

    sudo apt-get install gimp
    
Installing up to date VLC
-------------------------

Wheezy ships with VLC 2.0.3, you can grab latest VLC 2.1.2 from Wheezy 
backports repository:

.. code:: bash

    echo "deb http://ftp.de.debian.org/debian wheezy-backports main contrib non-free" | \
        sudo tee /etc/apt/sources.list.d/wheezy-backports.list
    sudo apt-get update
    sudo apt-get install -y -t wheezy-backports \
        vlc libavcodec-extra-53

  
To change VLC theme, or generally speaking the theme for all Qt based applications
you need to install Qt configuration utility:

.. code:: bash

    sudo apt-get install qt4-qtconfig
    qtconfig
    
For Intel video cards enable GPU assisted decoding in the preferences menu of VLC.
Make sure you have installed following and checked that *vainfo* reports
support for some profiles:

.. code:: bash

    sudo apt-get install i965-va-driver vainfo


Installing Skype
----------------

Skype is yet another closed source binary blob, but it can be installed
via following:

.. code:: bash

    sudo dpkg --add-architecture i386
    sudo apt-get update
    sudo apt-get install -y libc6:i386 libasound2:i386 libgcc1:i386 \
        libqt4-dbus:i386 libqt4-network:i386 libqt4-xml:i386 \
        libqtcore4:i386 libqtgui4:i386 libqtwebkit4:i386 \
        libstdc++6:i386 libx11-6:i386 libxext6:i386 libxss1:i386 \
        libxv1:i386 libssl1.0.0:i386 libasound2-plugins:i386 libpulse0:i386
    wget -O /tmp/skype-install.deb http://www.skype.com/go/getskype-linux-deb
    sudo dpkg -i /tmp/skype-install.deb
    
Note that Skype has issues with PulseAudio.
If pulse0:i386 refuses to install try relocating PulseAudio client configuration:

.. code:: bash

    sudo mv /etc/pulse/client.conf /etc/pulse/client.conf.old


Fixing Thinkpad middle button scroll
------------------------------------

Just add following code snippet to X session startup scripts:

.. code:: bash

    echo '
    xinput set-int-prop "TPPS/2 IBM TrackPoint" "Evdev Wheel Emulation" 8 1
    xinput set-int-prop "TPPS/2 IBM TrackPoint" "Evdev Wheel Emulation Button" 8 2
    xinput set-int-prop "TPPS/2 IBM TrackPoint" "Evdev Wheel Emulation Axes" 8 6 7 4 5
    ' | sudo tee /etc/X11/Xsession.d/99thinkpad-wheel-emulation
    
And make sure you have installed *xinput*:

.. code:: bash

    sudo apt-get install xinput


Fixing font rendering
---------------------

If you've been a long time Ubuntu user you will probably notice
that fonts look ugly on Debian especially when you're using LCD screen
like the one you might find on a laptop. That's because Microsoft has patented
`subpixel rendering technology <http://en.wikipedia.org/wiki/Subpixel_rendering#Patents>`_
and by default Debian attempts to avoid legal repercussions in US by disabling
patented technologies. To enable beautiful font rendering just dump
following to */etc/fonts/local.conf*

.. code:: xml

    <?xml version='1.0'?>
    <!DOCTYPE fontconfig SYSTEM 'fonts.dtd'>
    <fontconfig>
     <match target="font">
      <edit mode="assign" name="rgba">
       <const>rgb</const>
      </edit>
     </match>
     <match target="font">
      <edit mode="assign" name="hinting">
       <bool>true</bool>
      </edit>
     </match>
     <match target="font">
      <edit mode="assign" name="hintstyle">
       <const>hintslight</const>
      </edit>
     </match>
     <match target="font">
      <edit mode="assign" name="antialias">
       <bool>true</bool>
      </edit>
     </match>
      <match target="font">
        <edit mode="assign" name="lcdfilter">
          <const>lcddefault</const>
        </edit>
      </match>
    </fontconfig>

You are also probably missing bunch of fonts.
As I've understood *ttf-liberation* package provides substitutes
for Windows fonts which have been traditionally supplied via
*ttf-mscorefonts-installer* or *msttcorefonts* package.

.. code:: bash

    sudo apt-get install \
        ttf-liberation \
        ttf-arphic-uming \
        ttf-wqy-zenhei \
        fonts-ipafont-mincho \
        fonts-ipafont-gothic \
        ttf-unfonts-core \
        fonts-sil-gentium fonts-sil-gentium-basic \
        ttf-dustin ttf-georgewilliams ttf-sjfonts \
        ttf-larabie-deco ttf-larabie-straight ttf-larabie-uncommon

Finally clear per-user fontconfig caches:

.. code:: bash

    sudo fc-cache -fv


Install kernel with Con Kolivas patches
---------------------------------------

Con Kolivas has provided his patches to enable Brain Fuck Scheduler for Linux 3.12 series
which should enable lower latency and better input/output scheduling for laptops.
To compile the kernel you might want to insert proper field values 
to */etc/kernel-pkg.conf*:

.. code:: makefile

    maintainer := Lauri Võsandi
    email := lauri.vosandi@gmail.com
    priority := Low
    debian = 99koodur0

Then you're good to go:

.. code:: bash

    # Install dependencies
    sudo apt-get install build-essential gawk libncurses5-dev kernel-package

    # Download kernel source
    wget -c https://www.kernel.org/pub/linux/kernel/v3.x/linux-3.12.9.tar.xz
    tar xvf linux-3.12.9.tar.xz
    mv linux-3.12.9 linux-3.12.9-ck2
    cd linux-3.12.9-ck2

    # Download and apply patches
    wget -c http://ck.kolivas.org/patches/3.0/3.12/3.12-ck2/patch-3.12-ck2.bz2
    bunzip2 patch-3.12-ck2.bz2
    patch -p1 < patch-3.12-ck2

    # Initialize default config for kernel source
    make oldconfig

    # Build kernel package
    nice fakeroot make-kpkg --initrd binary-arch -j32

The package should be in the top level directory:

.. code:: bash

    sudo dpkg -i ../linux-image-3.12.9-ck2_99koodur0_amd64.deb

In some cases *ionice* could also help out by throttling stressful I/O processes.


Installing Estonian ID-card software
------------------------------------

RIA does not ship binaries for Debian,
however the source is available and if you're up to it you can compile it.
Easiest way is to use an APT repository I've prepared:

.. code:: bash

    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B8A6153D
    echo "deb http://packages.koodur.com wheezy main" |
        sudo tee /etc/apt/sources.list.d/koodur.list
    sudo apt-get update
    sudo apt-get install estonianidcard

The kernels you may find in the same repository:
disabled ATA disk support, disabled InfiniBand,
enabled low-latency desktop pre-emption,
*Deadline* scheduler for input/output,
*Brain Fuck Scheduler* or *Completely Fair Scheduling* if the BFS is not available
for processes.


Installing packages from source
-------------------------------

In order to install packages from source you most probably need following:

.. code:: bash

    sudo apt-get install -y \
        build-essential bison flex gawk libncurses5-dev \
        kernel-package libxslt1-dev \
        make git bzr subversion autoconf libtool

Installing Ruby on Rails
------------------------

Install Ruby, Ruby package manager and development headers:

.. code:: bash

    sudo apt-get install ruby ruby-dev rubygems libsqlite3-dev

Install Ruby on Rails:

.. code:: bash

    sudo gem install rails -V

Why the frick RoR does not pick up sqlite bindings installed via APT?!

Installing hipster douchebag Sublime text editor
------------------------------------------------

Sublime is closed source binary blob, so again installing this is not
recommended if you care about your privacy:

.. code:: bash

    wget -c http://c758482.r82.cf2.rackcdn.com/Sublime%20Text%202.0.2%20x64.tar.bz2 -O /tmp/sublime.tar.bz2
    tar xvjf /tmp/sublime.tar.bz2 -C /opt
    sudo mv /opt/Sublime\ Text\ 2 /opt/sublime-text-2
    sudo ln -s /opt/sublime-text-2/sublime_text /usr/local/bin/sublime_text

Installing Arduino and Fritzing
-------------------------------

You most probably get outdated versions of Arduino and Fritzing from Debian Wheezy,
nevertheless:

.. code:: bash

    sudo apt-get install fritzing arduino

Install Django
--------------

Instal Python, PIP package manager, etc:

.. code:: bash

    sudo apt-get install \
        python-dev cython ipython python-pip \
        python-mysqldb python-jinja2 \
        python-geoip \
        geoip-database

And of course you can get up to date Python packages via *pip*:

.. code:: bash

    sudo pip install \
        mercurial \
        django sass cssselect python-cjson tinycss
        pillow \
        unicodecsv \
        splicetee pysendfile \
        beautifulsoup \
        inotifyx \
        xbcfg \
        pygal lxml cairosvg

Install docutils
----------------

To install docutils make sure you have fonts from LaTeX and PIP:

.. code:: bash

    sudo apt-get install python-pip
        python-matplotlib \
        texlive-fonts-extra \
    sudo pip install \
        pygments docutils rst2pdf

Installing multimedia tools
---------------------------

FFMPEG has been deprecated in favor for *libav-tools*,
*moc* is a nice command-line audio player:

.. code:: bash

    sudo apt-get install -y \
        moc libav-tools \
        libflac-dev libmad0-dev libogg-dev \
        libchromaprint0 \
        python-mutagen
        
Set file associations
---------------------

File associations have always been a mess in Linux, in my 
/usr/share/applications/defaults.list I have:

.. code:: ini

    [Default Applications]
    application/pdf=atril.desktop;evince.desktop
    image/jpeg=eom.desktop;gimp.desktop
    image/bmp=eom.desktop;gimp.desktop
    image/png=eom.desktop;gimp.desktop
    image/svg+xml=eom.desktop;inkscape.desktop
    text/html=chromium.desktop
    text/plain=pluma.desktop
    text/x-modelica=pluma.desktop
    text/x-python=pluma.desktop
    application/x-shellscript=pluma.desktop
    video/matroska=smplayer.desktop
    video/mpeg=smplayer.desktop
    audio/mpeg3=vlc.desktop
    audio/wav=vlc.desktop
    audio/vorbis=vlc.desktop
        
Add colourful command prompt
----------------------------

Remember that neat colorful command-prompt from Gentoo?
Well you can also have it in Debian:

.. code:: bash

    echo "
    if [[ \${EUID} == 0 ]] ; then
      PS1='\[\033[01;31m\]\h\[\033[01;34m\] \W \$\[\033[00m\] '
    else
      PS1='\[\033[01;32m\]\u@\h\[\033[01;34m\] \w \$\[\033[00m\] '
    fi
    " | sudo tee -a /etc/bash.bashrc
    sudo rm -fv /etc/skel/.bashrc
    sudo rm -fv /home/*/.bashrc
    sudo rm -fv /root/.bashrc

Disable Terminus font on console
--------------------------------

I personally find Linux's built-in console font more appealing than
the one Debian substitutes it for. The package in charge is
*console-setup*, you may remove it:

.. code:: bash

    sudo apt-get purge console-setup

Or if preferred, substitute it's config with a dummy one:

.. code:: bash

    sudo mv /etc/default/console-setup /etc/default/console-setup.backup
    echo "" | sudo tee /etc/default/console-setup


Fix video tearing
-----------------

Wheezy ships with 2.19 version of Intel video card drivers which
still has issues on Sandy Bridge chipsets. You may try backporting a
package from *testing/jessie*, pinning packages from *testing* is not
reccommended since it can blow up your whole package management.
I have backported 2.21 from *jessie* and it seems to be working fine,
if you're interested in just that package you may download it:

.. code:: bash

    wget http://packages.koodur.com/dists/wheezy/main/binary-amd64/xserver-xorg-video-intel_2.21.15-2~koodur0_amd64.deb
    sudo dpkg -i xserver-xorg-video-intel_2.21.15-2.99koodur0_amd64.deb

You probably have to explicitly tell the Xorg driver to
enable TearFreea and SwapbuffersWait flags in */etc/X11/xorg.conf*.
Using SNA acceleration method might be a good idea aswell:

.. code:: bash

    Section "Device"
        Identifier  "Intel Graphics"
        Driver "intel"
        Option "TearFree" "true"
        Option "SwapbuffersWait" "true"
        Option "AccelMethod" "sna"
    EndSection

The *TearFree* experimental flag was added in 2.20 version of Intel driver,
and as far as I know it only works with SNA acceleration and
with *SwapbuffersWait* enabled.
It should work with both - with and without 3D compositing.
You can see if *TearFree* was enabled with:

.. code::

    lauri@localhost ~ $ grep TearFree /var/log/Xorg.0.log
    [     5.202] (**) intel(0): Option "TearFree" "true"

If you're adventurous you might want to try to enable PCI Express powersave,
framebuffer compression, LVDS downclocking and RC6 powersave mode for GPUs.
If you experience hangs try disabling  RC6.
If you see garbage on the screen you might want to disable framebuffer compression.

.. code:: bash

    sudo sed -i /etc/default/grub -e \
        's/^GRUB_CMDLINE_LINUX_DEFAULT=.*$/GRUB_CMDLINE_LINUX_DEFAULT="pcie_aspm=force i915.lvds_downclock=1 i915.i915_enable_rc6=1"/g'
    sudo update-grub2

When you enable 3D compositing in MATE desktop (System -> Preferences -> Windows) the
whole desktop environment switches from traditional bitmap based rendering to
OpenGL based rendering. There are couple ways to render OpenGL stuff on Xorg based systems,
when you don't have proper video card drivers installed a software renderer is used which
is of course slow. The video card driver works properly if direct rendering is enabled:

.. code::

    lauri@localhost ~ $ glxinfo | grep direct
    direct rendering: Yes

