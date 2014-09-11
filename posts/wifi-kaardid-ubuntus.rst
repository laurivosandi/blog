.. title: WiFi kaardid Ubuntus
.. date: 2010-08-11 10:52:28
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: Ubuntu, lucid, Broadcom, Intel, Atheros, Ralink
.. flags: hidden

WiFi kaardid Ubuntus
====================

Siin siis väike kokkuvõte situatsioonist võrgukaartidega Ubuntu all. Ehk säästab kellelegi aega! Selleks et kontrollida mis võrgukaart sul arvutis on, sisesta terminalis:

.. code:: bash

    lspci | grep -i net

Tulemuseks on midagi sellist:

.. code:: bash

    0c:00.0 Network controller: Broadcom Corporation BCM4311 802.11b/g WLAN (rev 01)

Broadcom
--------


Kui tegu on Broadcom kaardiga, on situatsioon üsna paha. Broadcom pole avaldanud eriti palju dokumentatsiooni oma kaartide kohta mistõttu draiverite kvaliteet jätab soovida. Ubuntu 10.04 sees on b43 moodul mis on reverse-engineeritud Linksys ruuteri tüürelite baasil. Kuigi tüürel on olemas, siis sellest siiski ei piisa, vajalik on ka firmware mis võrgukaardis endas jookseb. Debiani pakett mis kõik raske töö ära teeb on olemas `siin <http://lauri.vosandi.eu/dists/estobuntu/karmic/binary-i386/b43-firmware-1.0_estobuntu1.deb>`_ . Selle paketiga olen ma käima saanud võrgukaardid järgnevate kiibistikega: BCM4311, BCM4312. Varem on b43 tüürel põhjustanud arvuti kokkujoosmisi olles ühendatud krüpteeritud võrku, kuid praegu peaks situatsioon olema paranenud. Kui on probleeme siis võib mulle kirjutada-joonistada!

Intel
-----


Intelil on oma open-source osakond kes Linuxi tüürelitega tegeleb seega Inteli võrgukaartidega eriti probleeme ei tohiks tekkida. Paraku võrgukaartide firmware on kinnise lähtekoodiga, samas Intel lubab neid binaare levitada. Ubuntus on Inteli võrgukaartide firmware juba kaasas.

Atheros
-------


Atherose võrgukaardid on popid netbookides. Minu teada on nende võrgukaartide moodulid (ath3k, ath5k, ath9k) ja ka firmware avatud lähtekoodiga. Atheros ise tüürelite arendust vist palju ei toeta kuid on avaldanud piisavalt dokumentatsiooni, et Vaba Tarkvara kogukonnal oleks võimalik tüüreleid ise arendada. Probleemide esinemisel tasub paigaldada wireless backports pakett:

.. code:: bash

    sudo apt-get install linux-backports-modules-wireless-lucid-generic

Ralink
------

Ralink on üks vähestest firmadest kes paneb rõhku avatud lähtekoodiga moodulitele (rt2500, rt73). Ralink võrgukaartide tugi on üldiselt väga hea. Probleemide korral kehtib sama soovitus mis Atheros puhulgi - paigaldada wireless backports pakett.
