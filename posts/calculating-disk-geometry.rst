.. title: Calculating disk geometry
.. date: 2010-09-09 07:26:31
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: failbox, rant

Calculating disk geometry
=========================

.. image: http://www.promise-data-recovery.com/images/harddisk.jpg
When you come across various disk partitioning tools you might wonder what's up with cylinders, heads and whatnot. Well this goes back to the old days when they actually meant something, 4 heads meant 2 platters and so on. Nowadays it's just like an appendix that should have been cut out long time ago. This means that the disks are using maximum value those bits could use anyways like 255 for heads and 63 for sectors per track although there is no real disk with 127.5 platters!

So you have a disk which insist that it has 24321 cylinders, 255 heads, 63 sectors per track and 512 bytes per sector. Now to calculate the size of such disk you just multiply all those figures:

**24 321 cylinders * 255 heads * 63 sectors per track * 512 bytes per sector = 200 047 034 880 bytes or 200 gigabytes**

Now to create partitions, lets say with fdisk you need to have the number of sectors. So sector count for 64MB partition goes like this:

**64 mebibytes * 1 048 576 bytes per mebibyte / 512 bytes per sector = 131 072 sectors**

`Note that 1 megabyte is 1 000 000 bytes and 1 mebibyte is 1 048 576 bytes! <http://en.wikipedia.org/wiki/Mebibyte>`_ 
