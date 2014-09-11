.. title: Cooling DELL laptops with dellfand
.. date: 2010-07-09 12:32:29
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>

Cooling DELL laptops with dellfand
==================================

For long time I had my laptop running rather hot. The problem was that BIOS was
handling the cooling and not so well. First I tried loading *i8kfan* module but
it crashed the whole machine. Finally I found *dellfand* utility which allows
the user to control fan speed. Altough my DELL Studio 1535 wasn't listed in the
supported models list it still worked.

First I downloaded dependencies on my Ubuntu install:

.. code:: bash

    sudo apt-get install build-essential

Then compiled the program since it wasn't available in the APT repositories:

.. code:: bash

    wget -c http://dellfand.dinglisch.net/dellfand-0.9.tar.bz2
    tar xvf dellfand-0.9.tar.bz2
    cd dellfand-0.9
    make
    sudo cp dellfand /usr/local/bin

Finally started it up with following parameters:

.. code:: bash

    sudo dellfand 1 10 25 30 35

The cooling has three modes - turned off, low speed, max speed. In this case the
fan is turned off 25-30C, in low mode 30-35C and at max speed when the
temperature raises over 35C. More information `here <http://dellfand.dinglisch.net/>`_ .
