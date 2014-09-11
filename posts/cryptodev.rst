.. title: Accelerating crypto
.. date: 2014-07-09
.. tags: Cryptodev, OpenSSL, Crypto API
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>

Crypto API
----------

Crypto API is generic cryptography library API introduced in Linux kernel.
Kernel already contains software implementations for major symmetric
ciphers.
The API allows plugging in implementations which take advantage of hardware
components such as
Geode AES engine [#geode-aes-engine]_,
Kirkwood CESA engine [#cesa-engine]_
that can accelerate encryption.

OpenSSL acceleration
--------------------

Crypto API backend modules transparently accelerate kernelspace crypto such as IPsec.
Accelerating userspace applications Apache, OpenSSH, OpenVPN and others using OpenSSL
is currently possible via two methods.
Note that crypto hardware that has been implemented as instructions
such as VIA Padlock [#via-padlock]_ and Intel AES-NI [#aesni]_ does not need
any special mechanism to be used from userspace.

OpenSSL can take of advantage of Padlock if the respective engines are present.
AES-NI support seems to have been fully integrated [#openssl-aesni]_:

.. code:: bash

    openssl speed -elapsed -evp aes-128-cbc
    
Resulting following on Thinkpad T420's i5:

.. code::

    aes-128-cbc     501615.36k   539707.75k   549787.56k   554413.40k   554825.05k

Compared to a run where AES-NI capability was turned off explicitly:  
    
.. code:: bash

    OPENSSL_ia32cap="~0x200000200000000" openssl speed -elapsed -evp aes-128-cbc 
    
Resulting in roughly twice less throughput:

.. code::

    aes-128-cbc     249055.09k   282151.70k   287307.43k   292073.13k   292874.92k

.. [#openssl-aesni] http://openssl.6102.n7.nabble.com/How-can-I-enable-aes-ni-in-openssl-on-Linux-td47582.html


Userspace access via Cryptodev
------------------------------

Cryptodev-linux module [#cryptodev-linux]_ has to be compiled.
It's compatible with OpenBSD's cryptodev userspace API (*/dev/crypto*) and
it's GPLv2 licensed which means that one day it could be included in the upstream kernel.
It enables userspace application access to Crypto API backend modules already
present in the kernel.

Since such API is not available by default on Linux distributions,
the OpenSSL has to be recompiled with additional flags:

.. code:: bash

    ./configure -DHAVE_CRYPTODEV -DUSE_CRYPTDEV_DIGESTS
    make
    sudo make install
    
Note that for Ubuntu/Debian machines it is preferred to download source package,
modify debian/rules and recompile the package:

.. code:: bash

    apt-get source openssl
    cd openssl-*/
    sed -i -e "s/CONFARGS  =/CONFARGS = -DHAVE_CRYPTODEV -DUSE_CRYPTDEV_DIGESTS/" debian/rules
    dch -i "Enabled cryptodev support"
    debuild
    sudo dpkg -i ../openssl*.deb
  
You can test the performance by:

.. code:: bash
  
    openssl speed -evp aes-128-cbc -engine cryptodev -elapsed

.. [#geode-aes-engine] `Using Geode's AES engine on ALIX.3D3 
   <http://www.twam.info/hardware/alix/using-geodes-aes-engine-on-alix3d3>`_
.. [#cesa-engine] `Hardware Accelerated SSL on SheevaPlug <http://www.altechnative.net/2011/05/22/hardware-accelerated-ssl-on-marvell-kirkwood-arm-using-openssl-on-fedora/>`_
.. [#via-padlock] `VIA PadLock Security Engine <http://www.via.com.tw/en/initiatives/padlock/hardware.jsp>`_
.. [#aesni] `Intel® Advanced Encryption Standard Instructions (AES-NI) <https://software.intel.com/en-us/articles/intel-advanced-encryption-standard-instructions-aes-ni>`_
.. [#cryptodev-linux] `Cryptodev-linux module <http://cryptodev-linux.org/>`_

Userspace access via AF_ALG
---------------------------

AF_ALG plugin for OpenSSL [#openssl-af_alg]_ takes advantage of the new AF_ALG
interface present in kernels since 2.6.38.
It is very much like cryptodev method *sans* compiling special kernel module.
Isnstalling the plugin is pretty easy, note that you might need to adjust
engine lookup path:

.. code:: bash

    git clone http://src.carnivore.it/users/common/af_alg/
    cd af_alg/
    make
    sudo cp libaf_alg.so /usr/lib/arm-linux-gnueabi/openssl-1.0.0/engines/
    sudo chmod 644 /usr/lib/arm-linux-gnueabi/openssl-1.0.0/engines/libaf_alg.so

Make sure modules are loaded:

.. code:: bash

    echo af_alg >> /etc/modules
    echo algif_hash >> /etc/modules
    echo algif_skcipher >> /etc/modules
    modprobe af_alg algif_hash algif_skcipher

You can test the performance by:

.. code:: bash

    openssl speed -evp aes-128-cbc -engine af_alg -elapsed

.. [#openssl-af_alg] `OpenSSL AF_ALG plugin <http://carnivore.it/2011/04/23/openssl_-_af_alg>`_



