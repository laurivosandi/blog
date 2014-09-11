.. title: Bricking Samsung Galaxy S2
.. date: 2011-10-27 08:11:05
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: Android
.. flags: outdated

Bricking Samsung Galaxy S2
==========================

Hey everyone, it has been a long time since my last post.
There's much fuss around installing custom firmware on Samsung Galaxy S2,
so I wanted to figure out how it exactly works.

First of all most Android customized ROM's, eg. CyanogenMod, VillainROM,
DarkyROM aren't exactly ROM images, they're zipped filesystem
overlays of the original stock firmware root filesystem.
This means that in order for the customization to work,
you first need to have properly booting stock firmware [#tips]_.

To install these customizations you need to have a rooted phone.
Rooted phone basically meanss that you can run the classic
UNIX command "su" to become the root user.
There are hacked kernel [#kernels]_ images available on the XDA developers for various versions of Galaxy S2.

Utilities called Odin and Heimdall are available for directly manipulating the
built-in flash storage of Samsung Galaxy phones.
Odin seems to be available only for Windows so it's out of the scope of this blogpost.
Heimdall is a cross-platform command-line utility with similar purpose [#heimdall]_ .

Rooting Samsung Galaxy S2 [#rooting]_ is easy as booting it into the download mode,
this means turning the phone off and holding Volume **down** and Home buttons
while powering up the phone and uploading the hacked kernel using Heimdall:

.. code:: bash

    # This kernel should work with stock Android 2.3.4 firmware of Galaxy S2 sold in Europe
    http://attachments.xda-developers.com/attachment.php?attachmentid=651559&d=1310388033 \
        -O CF-Root-SGS2_XX_OXA_KG1-v4.1-CWM4.zip
    unzip CF-Root-SGS2_XX_OXA_KG1-v4.1-CWM4.zip
    tar xvf CF-Root-SGS2_XX_OXA_KG1-v4.1-CWM4.tar
    echo "3a70ced0c96d947b4cb1983dcebd1584  zImage" | md5sum -c -
    sudo heimdall flash --kernel zImage

The yellow warning sign is shown while booting with the hacked kernel - it's okay.
The hacked kernel image also installs two apps: ROM Manager and Superuser.
First one allows the user to (re)boot into ClockworkMod Recovery. 
It is also possible to directly boot into ClockworkMod Recovery,
just hold Volume **up** and Home while powering up the phone.
It is always good idea to back up the current system [#pit]_.
Move around in the ClockworkMod Recovery menus with volume up/down buttons.

The phone's internal flash storage is called "SD Card" in the
ClockworkMod Recovery although it's not an actual SD card plugged into the
SD card socket, so this means that **you don't need an SD card to install custom ROM**. 
While running ClockworkMod, it is possible to mount the internal flash storage to your PC,
this way you can upload the ROM zip to your phone.
Once having the right zip file in your phone just select
"Install zip from sdcard" while running ClockworkMod Recovery.

There are many custom ROM's for Galaxy S2, the most popular CyanogenMod seems
to be built from scratch and does not have the optimizations enabled for S2,
it's also rumored that is does not have support for hardware accelerated video decoding.
I haven't tried out VillainROM [#villainrom]_ yet,
but DarkyROM [#darkyrom]_ that is based on the original Samsung firmware seems to be running just fine.

**OH AND OF COURSE YOU VOID ANY WARRANTY IF YOU FLASH ANY FUNKY STUFF ON YOUR PHONE**

.. [#tips]        http://wiki.cyanogenmod.com/wiki/Samsung_Galaxy_S_II:_Full_Update_Guide
.. [#kernels]    `Hacked kernels with CWM and SU on XDA developers <http://forum.xda-developers.com/showthread.php?t=1103399>`_ 
.. [#heimdall]    http://www.glassechidna.com.au/products/heimdall/
.. [#rooting]     http://winterland.no-ip.org/2011/09/root-galaxy-s2-with-heimdall-on-linux/
.. [#pit]        `Default PIT (Partition Information Table) <http://pastebin.com/SAQVbx3L>`_
.. [#villainrom]  http://www.villainrom.co.uk/forum/
.. [#darkyrom]    http://www.darkyrom.com/community/index.php?threads/rom-cwm-sgs2-2-3-5-darkyrom2-xxki3-base.5710/

