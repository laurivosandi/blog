.. title: Ubuntu 10.04, LTSP ja ID-kaart
.. date: 2011-11-12 10:45:13
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: LTSP, Ubuntu, ID-card, PCSC-Lite, pcscd, OpenSC, SmartCard, PKCS#11

Ubuntu 10.04, LTSP ja ID-kaart
==============================

Vahepeal on mitu uut Ubuntu väljalaset olnud ning viimased ID-kaardi
terminal-serveri paketid Ubuntule sai treitud 8.04 jaoks.
Seekord siis Estobuntu 10.09 ehk Ubuntu 10.04 jaoks,
seni olengi ainult Ubuntu Long Term Support väljalasetele neid teinud ning
tihedamini vist ei hakkagi punnitama.

Serveri tarkvara paigaldus
--------------------------

Juhend eeldab Ubuntu Server 10.04 paigaldust. Kõigepealt paigalda LTSP paketid:

.. code:: bash

    apt-get install ltsp-server-standalone python-software-properties ubuntu-desktop

Paigalda soovitud töölaud:

.. code:: bash

    apt-get install ubuntu-desktop

Luba repositooriumid:

.. code:: bash

    add-apt-repository ppa:lauri-vosandi/ppa
    add-apt-repository ppa:esteid/ppa
    apt-get update

Paigalda paketid:

.. code:: bash

    apt-get install openssh-server libpcsclite1 \
        qdigidoc qesteidutil mozilla-esteid thunderbird-esteid

Lisa Xsession skript mis näitab uut PCSC-lite sokkli asukohta:

.. code:: bash

    echo "export PCSCLITE_CSOCK_NAME=$HOME/.pcscd.comm" > /etc/X11/Xsession.d/80-pcsclite


Terminali tarkvara paigaldus
----------------------------


Paigalda terminali tarkvara serveri /opt/ltsp/i386 alla:

.. code:: bash

    MIRROR="http://ee.archive.ubuntu.com/ubuntu/" \
    EARLY_PACKAGES="ltsp-client" \
    LANG=C \
    ltsp-build-client --arch i386

Sisene terminali juurikasse:

.. code:: bash

    chroot /opt/ltsp/i386

Uuenda pakettide nimekirju:

.. code:: bash

    apt-get install python-software-properties
    add-apt-repository ppa:lauri-vosandi/ppa
    add-apt-repository ppa:esteid/ppa
    apt-get update

Paigalda modifitseeritud paketid:

.. code:: bash

    apt-get install openssh-client pcscd libccid

Lisa SSH kliendi seadistused, asenda 192.168.0.21 oma serveri IP-ga:

.. code:: bash

    echo "Host 192.168.0.10
        RemoteForward [~/.pcscd.comm] :[/var/run/pcscd/pcscd.comm]" >> /etc/ssh/ssh_config

Välju terminali juurikast:

.. code:: bash

    exit

Uuenda võrgust laetavaid tõmmiseid:

.. code:: bash

    ltsp-update-image --arch i386


