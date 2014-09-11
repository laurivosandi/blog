.. title: Elioni hüperkiire internet
.. date: 2010-07-16 21:26:54
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: IPTV, Elion

Elioni hüperkiire internet
==========================

Siit ka minu esimene eestikeelne postitus. Sain mõned päevad tagasi "õnnelikuks"
Elioni hüperkiire interneti kliendiks. Teoorias lubavad läbilaskevõimet 100Mbps
alla ja 20Mbps üles ning paistab, et praktikas ka nii on. Enne ühenduse
hankimist tekkis mul terve tosin küsimust, millele klienditeeninduse tädid ei
osanud vastata ja küll mulle lubati 2-3 korda et "päris" tehnik võtab kontakti
aga ei tuhkagi.

Hüperkiire interneti infrastruktuur paistab olevat ehitatud Tallinnas välja nii
mõneski korterelamus ning korterelamu all ma mõtlen just nõukogudeaegseid 5- ja
9-korruselisi hooneid. Majasse tuleb sisse fiiber, keldris on switch ning iga
korruse peale on tõmmatud CAT5 kaablid ja 2  pistikut. Tehniku töö seisneski
õige juhtme ühendamises switchi.

Elioni kolmiklahendus selle ühenduse baasil on täiesti IP põhine. Kaabli
ühendamisel arvutisse saab sealt kohe DHCPga avaliku IP, millel on mul soovi
kohaselt kõik pordid lahti. Elioni DigiTV paketid liiguvad eraldi VLANis ning
nad on märgistatud identifikaatornumbriga 4, tegu on siinkohal IEEE 802.1Q
standardiga. Linuxis on üpris lihtne luua virtuaalvõrguliides, mis sorteerib
välja need märgistatud paketid võimaldades arvutist ka vaadata televisiooni.:

.. code:: bash

    ip link add link eth0 name iptv0 type vlan id 4

Peale virtuaalliidese loomist saab sealt ka küsida oma "telekale" IP aadressi.
Kontrolli mõttes võib pingida aadressi 10.0.16.12 või domeeninime web.dtv.
Kui VLAN on korrektselt seadistatud siis need mõlemad peaksid vastama.:

.. code:: bash

    dhclient iptv0

Paraku arvuti puhul DHCP keerab ruutimistabeli sassi ja tekitab segadust ka DNS
kirjete lahendamisel. Kõige lihtsam lahendus oli kasutada DHCPga antud IPd
staatiliselt. Nii või naa jääb veel puudu ruutimiskirje digitelevisiooni
multicasti edastamiseks:

.. code:: bash

    route add -net 224.0.0.0 netmask 240.0.0.0 dev iptv0

Nii palju kui ma Elioni pakutava Digiboksi kohta kaevanud ja kuulnud olen, siis
tegu on embedded Linuxil põhineva seadmega. Vanemates variantides olevat olnud
32MB ROMi, uuemates 64MB ning protsessoriks PowerPC. Krüpteeritud kanaleid
mängib Widevine multiplatvormne DRM rakendus. Krüpteerimata on vaid ETV,
Kanal 2 ning TV3. Tähele võiks panna seda et Digiboksi MACi aadressi
spoofimine POLE vajalik, seda ka mitte vanema ADSL põhise ühenduse puhul!
Küll aga võtab omajagu aega multicasti gruppi ühinemise päring, st peale
võrguseadete rakendamist võib oodata rahulikult 20-60 sekundit enne kui VLC
nõustub üleüldse midagi mängima.

Pika uurimustöö lõpptulemuseks sai minu sülearvuti /etc/network/interfaces fail,
mis võimaldab otse Elioni DigiTV-d vaadata:

.. code:: bash

    auto lo
    iface lo inet loopback
     
    # Primaarne võrguliides
    auto eth0
    iface eth0 inet dhcp
      
    # DHCP toimiks ka aga DHCP kirjutab üle default route ja DNS kirjed
    auto iptv0
    iface iptv0 inet static
        # Sama mis DHCPga saades
        address 10.253.145.203
        netmask 255.255.192.0
        # Lisame Q VLAN virtuaalliidese iptv0, ühendatuna eth0 külge
        pre-up ip link add link eth0 name iptv0 type vlan id 4
        # Lisame multicasti route
        post-up route add -net 224.0.0.0 netmask 240.0.0.0 dev iptv0
        # Seame lüüsi 10.0.0.0/8 võrgu jaoks, kuna me ei taha vaikimisi lüüsi üle kirjutada
        post-up route add -net 10.0.0.0 netmask 255.0.0.0 gw 10.253.128.1 dev iptv0
        # Lisame multicast grupi liikmelisuse vastamiseks route-i
        post-up route add -net 84.50.255.0 netmask 255.255.255.0 dev iptv0
        # Kustutame virtuaalliidese
        post-down ip link del link eth0 dev iptv0

Peale selle tuli tuuma seadeid natuke muuta failis /etc/sysctl.conf:

.. code:: bash

    net.ipv4.conf.iptv0.rp_filter=0
    net.ipv4.conf.iptv0.force_igmp_version=2

Ning nende uuesti laadimiseks:

.. code:: bash

    sysctl -p

Üks trikk veel mis muidu kahe silma vahele võib jääda - VLC tahab saada
miskipärast @ märki aadressis, st ETV vaatamiseks tuleb täpselt, märk-märgilt kasutada sellist käsku:

.. code:: bash

    vlc udp://@239.3.1.1:1234

Järgmisel korral VoIP ning DD-WRT seadistamisest!
