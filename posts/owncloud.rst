.. title: Owncloud
.. date: 2014-03-15
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags:  cloud, PHP, Ubuntu

Owncloud
========

Sissejuhatus
------------

OwnCloud on veebipõhine privaatpilve lahendus asendades osaliselt Google Drive'i.


Paigaldus
---------

Ubuntu puhul saab kõige värskema OwnCloudi versiooni OpenSUSE tarkvarapakettide varamust:

.. code:: bash

    echo "deb http://download.opensuse.org/repositories/isv:/ownCloud:/community/xUbuntu_12.04/ /" | \
        sudo tee /etc/apt/sources.list.d/owncloud.list
    wget -q -O - http://download.opensuse.org/repositories/isv:ownCloud:community/xUbuntu_13.10/Release.key | \
        sudo apt-key add -
    apt-get update
    apt-get install owncloud

Debian Wheezy varamutes hetkeseisuga OwnCloudi pole:

.. code:: bash

    echo "deb http://download.opensuse.org/repositories/isv:/ownCloud:/community/Debian_7.0/ /" | \
        sudo tee /etc/apt/sources.list.d/owncloud.list 
    wget -q -O - http://download.opensuse.org/repositories/isv:ownCloud:community/Debian_7.0/Release.key | \
        sudo apt-key add -
    apt-get update
    apt-get install owncloud

Peale paigaldust ava /owncloud oma serveri aadressilt,
näiteks http://owncloud.povi.ee/owncloud/ ning loo administraator-kasutaja OwnCloud jaoks.
Selle kasutajakontoga saab seda OwnCloud paigaldust seadistada.

Sidumine LDAP-iga
-----------------

Vasakult alt nurgast vali *+ Rakendused*, seejärel nimekirjast
*LDAP user and group backend* ning klõpsa nupul *Lülita sisse*.
Seejärel paremal üleval kasutajanimel klõpsates vali menüüst *Admin*,
rulli alla ning seal peaks vastu vaatama LDAP sektsioon.
*Server* kaardil sisesta LDAP serveri masinanimi (näiteks ldap.povi.ee),
port on vaikimisi port (389),
kasutaja DN ning parool jäta tühjaks.
Viimasesse lahtrisse sisesta baas DN (dc=ldap,dc=povi,dc=ee).
Vajuta *Jätka* ning veendu et seadistus oleks korras (roheline mammu).
*User Filter* all vali *posixAccount* objektiklassid nii et moodustuks filter:

.. code::

    (|(objectclass=posixAccount))

*Login Filter* all eemalda LDAP kasutajanimi ning LDAP e-posti aadress.
Muude attribuutide alla lisa ainult *uid*, moodustuma peaks järgnev filter:

.. code::

    (&(|(objectclass=posixAccount))(|(uid=%uid)))

*Group Filter* all lisa ainult *posixGroup* objektiklass nii et filter oleks:

.. code::

    (&(|(objectclass=posixGroup)))

*Advanced* kaardi all veendu, et *Kausta seaded* all, *Kasutaja näidatava nime väli* oleks *uid*, mitte *displayname*.

Silumine
--------

Owncloud hoiab oma logi tavaliselt */var/www/owncloud/data/owncloud.log* all, kui on probleeme siis aitab logi vaatamine:

.. code:: bash

    tail -f /var/www/owncloud/data/owncloud.log 

Klientrakendus
--------------

Graafiline klientrakendus võimaldab kasutajanime ning parooliga OwnCloud
serverist kohalikku masinasse sünkroniseerida faile.

.. code:: bash

    sudo apt-get install owncloud-client
