.. date: 2010-08-11 11:52:50
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: Huawei, TELE2, DELL, Broadcom
.. flags: outdated

DELL D620 ja TELE2 netipulk Huawei E1752
========================================

Teisipäevasele `Vaba Tarkvara klubi <http://www.google.com/calendar/embed?src=kgqbmrqri8l175ontecafi4nds%40group.calendar.google.com&amp;ctz=Europe/Tallinn>`_  kogunemisele toodi üks DELLi sülearvuti ning TELE2 netipulk, täpsemini Huawei E1752.
Peale oli lastud eelmine Estobuntu versioon (Ubuntu 9.10 põhine) ning netipulk mängis trikke.
Kuna masin oli dokumentidest tühi siis peale mõningast näppimist tundus mõistlik värske Estobuntu 10.05 peale lasta.
Hiljem selgus et üks USB port oli rikkis, mistõttu netipulk ei töötanud aga mis sest.

.. figure:: http://farm5.staticflickr.com/4116/4919372039_b1dd6a1714_o_d.jpg
    :width: 60%

    Huawei E1752 ehk TELE2 pakutav 3G modem


Esiteks panin paika DELLi jahutuse:

.. code:: bash

    sudo apt-get install i8kutils
    cat /usr/share/doc/i8kutils/examples/i8kmon.conf | sudo tee /etc/i8kmon

Sülearvuti sees oli ka Broadcomi bcm4311 võrgukaart, seega panin peale võrgukaardi firmware:

.. code:: bash

    wget http://lauri.vosandi.com/dists/estobuntu/karmic/binary-i386/b43-firmware-1.0_estobuntu1.deb
    sudo dpkg -i b43-firmware-1.0_estobuntu1.deb

Netipulgaga oli nii, et mõnikord ta tegi modeswitchi ise, mõnikord mitte.
Mälupulgana oli ta lsusb all indekseeritud tootja identifikaatoriga 0x12d1 ning
toote identifikaatoriga 0x1446. Peale modeswitchi lülitus toote id 0x1001 peale.
Selleks et olla kindel et lülitus toimuks paigaldasin ka usb-modeswitch paketi:

.. code:: bash

    sudo apt-get install usb-modeswitch usb-modeswitchd-data

Teadmiseks teistele häkkeritele siis Udev reeglite tegemine või usb-modeswitchi
seadistamine EI ole enam vajalik. Udev reeglid mis kõik automatiseerimise ära
teevad on failis /lib/udev/rules.d/40-usb_modeswitch.rules

Lõpuks tegin masinale restardi ning seadistasin võrguhalduris TELE2 ühenduse ning kõik toimis nagu kulda.
