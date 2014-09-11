.. title: QNAP TS-412 võrguketas
.. date: 2013-09-02
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: NAS, QNAP, ARM

QNAP TS-412 võrguketas
======================

asdkfjfjlksajflksajflkdsajfdsajfsajdfljdsaflkjsaflkjsalkfjasfjksajfsajflkjsaf

Käesolev artikkel räägib kuidas QNAP TS-412 võrgukettale
paigaldada Debian tarkvarakogumik.

.. image:: http://d2bktxdiepbdhz.cloudfront.net/images/products/full/4TS-412-2.jpg
    :width: 80%
    :align: center

QNAP TS-412 on üks väga ütlematagi pädevate näitajatega võrguketas:

* 1.2GHz Marvell Kirkwood 88F6281 ARMv6-ühilduv protsessor
* 256MB DDR2 mälu
* 16MB püsimälu 
* 4x 3.5" SATA kettapesa
* 2x 1Gbps võrguliidesed
* 2x eSATA pesad
* 4x USB pesad
* Toiteplokk 120W, kuid reaalselt võiks arvestada max 10W + 10W ketta kohta

Ühenda ülemise võrgupesa kaudu kettaboks võrku.
Marsruuterist tuvasta mis IP-aadressiga võrguketas külge tuli,
kui kasutate näiteks *dnsmasq* tarkvara DHCP serverina:

.. code::

    localhost ~ # cat /var/lib/misc/dnsmasq.leases | grep "01:00:08"
    1378178319 00:08:9b:d1:79:4b 192.168.3.229 NASD1794B 01:00:08:9b:d1:79:4b

Logi sisse *ssh* abil, parool peaks olema *admin*:

.. code:: bash

    ssh admin@192.168.3.229 # Parool on "admin"

Järgnevalt laadi alla alglaadimisjuurfailisüsteem (*initial* *root* *disk*),
tuum (*kernel*) ning skriptid nende paigaldamiseks:

.. code:: bash

    cd /tmp
    busybox wget ftp://ftp.debian.org/debian/dists/stable/main/installer-armel/current/images/kirkwood/network-console/qnap/ts-41x/initrd.gz
    busybox wget ftp://ftp.debian.org/debian/dists/stable/main/installer-armel/current/images/kirkwood/network-console/qnap/ts-41x/kernel
    busybox wget http://people.debian.org/~tbm/qnap/flash-debian
    busybox wget ftp://ftp.debian.org/debian/dists/stable/main/installer-armel/current/images/kirkwood/network-console/qnap/ts-41x/model
    sh flash-debian

Nüüd oota marurahulikult, et need skriptid võrguketta püsimälu uuendaks.
Vastasel korral võid võrguketta telliseks lasta ning 
pead ikka eriti hea muinasjutu garantii poistele välja mõtlema:

.. code::

    Updating MAC address...
    Your MAC address is 00:08:9B:8C:xx:xx
    Writing debian-installer to flash... done.
    Please reboot your QNAP device.

Järgnevalt taaskäivita võrguketas:

.. code:: bash

    reboot
    exit

Läheb pisut aega ja Debiani paigaldus käivitub võrgukettas.
Kui hästi läheb, korjab võrguketas üles DHCP ning kasutab sama IP-aadressi mis ennegi.
Mõnel juhul võivad võrguliidesed vahetusse minna ning DHCP-klient käivitub automaastelt
hoopis alumisel võrgupesal. Käesoleva katsetuse puhul oli näiteks nii:

* *eth0* alumine pesa
* *eth1* ülemine pesa

Viimane variant on see, et võrguketas läheb käima staatilise IP-aadressiga.
Sel juhul peab käisitsi ühenduma 192.168.1.100 IP-aadressile ning
sülearvuti vms masina kust ühendutakse tõstma samasse 192.168.1.0/24 alamvõrku.
Arvesta, et Debiani paigaldaja OpenSSH server genereerib igal käivitamisel
uued võtmed mistõttu võib tulla ette, et peab *known_hosts* failist mõned 
read eemaldada. Debiani paigaldaja parool on igal juhul *install*:

.. code:: bash

    ssh installer@192.168.3.229 # Parool on "install"

Kui võrguketas on käima läinud staatilise IP-ga vali Debiani
paigaldaja menüüst *start* *shell* ning küsi mõnele võrguliidesele
IP-aadress. Siinkohal muidugi kukub võrguühendus maha kui see on see sama 
ühendus mille kaudu ühenduti.

.. code:: bash

    dhclient eth1

Kui internetiühendus on olemas võib edasi liikuda Debiani paigaldamise juurde.
Logi sisse võrgukettasse ning vali menüüst *Start* *installer*:

.. code:: bash

    ssh installer@192.168.3.229

Edasine peaks olema üsna iseenesestmõistetav kui on vähegi tuttav Debiani
paigaldamine.

Kasutatud materjalid:

* `Installing Debian on the QNAP TS-41x <http://www.cyrius.com/debian/kirkwood/qnap/ts-41x/install/>`_

Eestis tarnivad QNAP võrgukettaid:

* `Arvuti Traumapunkt <http://www.atrauma.ee/>`_
* `Arvutitark <http://arvutitark.ee/est/TOOTEKATALOOG/qnap/NAP-4-Bay-TurboNAS-SATA-3G-12G-256M-RAM-2x-GbE-LAN-69456>`_
* `www.ox.ee <http://www.ox.ee/est/product/324558>`_
* ... ja kindlasti paljud teised. Ordi, Klick ega Euronics hinnakirjadest
  praeguse seisuga QNAP tooteid küll aga **EI** leia
