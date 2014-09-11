.. title: Ubuntu minimal install with memory stick
.. date: 2010-07-29 21:25:24
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: Ubuntu, wget, zcat

Ubuntu minimal install with memory stick
========================================

The really hassle-free method for installing Ubuntu is this. Get bootable 15 meg image here:

.. code:: bash

    wget -c http://archive.ubuntu.com/ubuntu/dists/lucid/main/installer-amd64/current/images/netboot/boot.img.gz

Write the image to your memory stick device, remember to replace sdz with the correct one!:

.. code:: bash

    zcat boot.img.gz > /dev/sdz


