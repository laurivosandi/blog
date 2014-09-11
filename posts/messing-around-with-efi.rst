.. title: Messing around with EFI
.. date: 2014-03-02
.. tags: EFI, PC-BIOS, GRUB, Debian

Messing around with EFI
=======================

Introduction
------------

UEFI is a new way to boot PC-s.
Most UEFI enabled computers also allow so called *Legacy mode*
which emulates PC BIOS behaviour.
Windows 7 recommended UEFI and
Windows 8 requires that computers come with UEFI firmware.

Making distinction between UEFI and traditional PC BIOS is not that easy
because the manufacturers have seriously messed up presenting that information.

Partition table
---------------

First of all the partition table differs.
Traditional PC-s have DOS partition tables:

.. code::

    localhost ~ $ fdisk /dev/sda

    Command (m for help): p

    Disk /dev/sda: 128.0 GB, 128035676160 bytes
    255 heads, 63 sectors/track, 15566 cylinders, total 250069680 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk identifier: 0x000d5238

       Device Boot      Start         End      Blocks   Id  System
    /dev/sda1   *        2048    29296639    14647296   83  Linux
    /dev/sda2        29296640   250068991   110386176   83  Linux

    Command (m for help):
    
One of the requirements of EFI is that instead DOS partition table a GPT
partition table is used. 
Attempting to edit GPT partition table with *fdisk* will result in a warning.
Also all the disk space is allocated to protective partition:

.. code::

    localhost ~ $ fdisk /dev/sda

    WARNING: GPT (GUID Partition Table) detected on '/dev/sda'! The util fdisk doesn't support GPT. Use GNU Parted.


    Command (m for help): p

    Disk /dev/sda: 256.1 GB, 256060514304 bytes
    255 heads, 63 sectors/track, 31130 cylinders, total 500118192 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk identifier: 0x00000000

       Device Boot      Start         End      Blocks   Id  System
    /dev/sda1               1   500118191   250059095+  ee  GPT

    Command (m for help): 

To edit a GPT partition table you need *gdisk*:

.. code::

    localhost ~ $ gdisk /dev/sda
    GPT fdisk (gdisk) version 0.8.5

    Partition table scan:
      MBR: protective
      BSD: not present
      APM: not present
      GPT: present

    Found valid GPT with protective MBR; using GPT.

    Command (? for help): p
    Disk /dev/sda: 500118192 sectors, 238.5 GiB
    Logical sector size: 512 bytes
    Disk identifier (GUID): 878637F3-2209-4C79-94EE-6C8DDB145D61
    Partition table holds up to 128 entries
    First usable sector is 34, last usable sector is 500118158
    Partitions will be aligned on 2048-sector boundaries
    Total free space is 2669 sectors (1.3 MiB)

    Number  Start (sector)    End (sector)  Size       Code  Name
       1            2048          249855   121.0 MiB   EF00  
       2          249856        29546495   14.0 GiB    0700  
       3       441524224       470820863   14.0 GiB    0700  
       4       470820864       500117503   14.0 GiB    0700  
       5        29546496       441524223   196.4 GiB   0700  

    Command (? for help): 
    
EFI partition
-------------

As can be seen from the partition listing above there is a partition with code EF00.
This is a FAT32 formatted partition that contains the bootloaders of operating systems.
It is usually mounted at */boot/efi*:

.. code::

    localhost ~ $ mount | grep boot
    /dev/sda1 on /boot/efi type vfat (rw,relatime,fmask=0022,dmask=0022,codepage=437,iocharset=utf8,shortname=mixed,errors=remount-ro)
    
If you would run it on a cleanly installed Debian Wheezy box it would look something like this:

.. code::

    localhost ~ $ find /boot/efi
    /boot/efi
    /boot/efi/EFI
    /boot/efi/EFI/debian
    /boot/efi/EFI/debian/grubx64.efi
    
Secure Boot feature of UEFI firmware checks the signature of those bootloader binaries
and refuses to boot Debian because Debian's GRUB is not signed.
On my Thinkpad T420 I could not locate Secure Boot toggle in the BIOS,
appearently it's disabled by default.

EFI boot entries
----------------

You can list EFI entries using *efibootmgr* if you have booted your machine in EFI mode,
that is - you have NOT enabled legacy mode in the BIOS:

.. code::

    lauri-t420 lauri $ efibootmgr 
    BootCurrent: 0019
    Timeout: 0 seconds
    BootOrder: 0019,000D,000B,000A,0008,0007,0006,000C,0013,0009,0011,0010,000F,000E,0012
    Boot0000  Setup
    Boot0001  Boot Menu
    Boot0002  Diagnostic Splash Screen
    Boot0003  Startup Interrupt Menu
    Boot0004  ME Configuration Menu
    Boot0005  Rescue and Recovery
    Boot0006* USB CD
    Boot0007* USB FDD
    Boot0008* ATAPI CD0
    Boot0009* ATA HDD2
    Boot000A* ATA HDD0
    Boot000B* ATA HDD1
    Boot000C* USB HDD
    Boot000D  PCI LAN
    Boot000E* ATAPI CD1
    Boot000F* ATAPI CD2
    Boot0010* Other CD
    Boot0011* ATA HDD3
    Boot0012* ATA HDD4
    Boot0013* Other HDD
    Boot0014* IDER BOOT CDROM
    Boot0015* IDER BOOT Floppy
    Boot0016* ATA HDD
    Boot0017* ATAPI CD:
    Boot0018* PCI LAN
    Boot0019* debian

This of course assumes that *efivars* module has been loaded and the kernel has detected the presence of UEFI:

.. code::

    modprobe efivars

If you have loaded the module but *efibootmgr* still fails to probe the EFI entries
this means that your EFI firmware is not detected by the kernel:

.. code::

    Fatal:  Couldn't open either sysfs or procfs directories for accessing EFI variables.
    Try 'modprobe efivars' as root.


Restoring EFI entries
---------------------

On my Thinkpad T420 I happened to restore BIOS defaults which appearently also
deletes all EFI entries (dafuq?!).
Get a hold of a USB stick that boots with UEFI enabled BIOS, you may notice
Debian Wheezy LiveCDs, Gentoo LiveCD and many others fail to boot if you have
put the ISO on the usb key 1:1 with *dd* or *cat*.
Sabayon Linux luckily has ISO which boots properly off USB memory stick.
Note that I haven't used *unetbootin* to place ISO on a memory stick in a long
time and I would not recommend it to anyone anyway.

I have to remind this again - *efibootmgr* complains that sysfs entries are missing if
you attempt to boot in legacy mode.

Once Sabayon is up and running:

.. code:: bash

    sudo mkdir /wheezy                      # Create mountpoint for my already installed Debian Wheezy
    sudo mount /dev/sda2 /wheezy            # Mount root filesystem of Debian
    sudo mount /dev/sda1 /wheezy/boot/efi   # Mount EFI partition
    sudo mount --bind /dev /wheezy/dev
    sudo mount --boot /dev/pts /wheezy/dev/pts
    sudo mount --boot /sys /wheezy/sys
    sudo mount --boot /proc /wheezy/proc
    sudo chroot /wheezy apt-get install --reinstall grub-efi-amd64
    sudo umount /wheezy/dev/pts
    sudo umount /wheezy/dev/
    sudo umount /wheezy/proc
    sudo umount /wheezy/sys
    sudo umount /wheezy/boot/efi
    sudo umount /wheezy/
    sudo reboot

This method also works if let's say you tried to install Ubuntu and it failed
to detect that it is running on a UEFI enabled machine and the machine refuses
to boot into GRUB.   
