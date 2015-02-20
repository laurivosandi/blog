.. title: ID-kaardi paketid Ubuntu 14.04, Linux Mint 17 ja Debian jaoks
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. date: 2014-04-18
.. tags: tallinx

ID-kaardi paketid Ubuntu 14.04, Linux Mint 17 ja Debian jaoks
=============================================================

.. important:: Käesolev juhend on aegunud. Ubuntu 14.04 ja Mint 17 jaoks soovitan 2014 septembri seisuga paigaldada RIA ametlikud tarkvarapaketid kuhu sisse sai ka minu Google Chrome/Chromium automaagia. Tähelepanu peaks pöörama sellele, et Chrome/Chromium 34 oli viimane versioon mis toetas ID-kaardiga allkirjastamist Firefox pistikprogrammi abil. RIA varamus on PPAPI liidesega pistikprogramm uuemate väljalasete jaoks, kuid see eeldab ka teenusepakkujate tuge mida ilmselt **2014 aasta sees ei tule**. LHV on lõpuks ka oma sertifikaadi korda teinud ning pole vaja keemiat teha et Chromium LHV-sse sisse logiks. Debiani pakettide jaoks võib minu varamut ikka proovida - wheezy amd64/i386 ning jessie armhf pakid peaks olema kasutuskõlblikud.

Sissejuhatus
------------

Aprillikuus lasti välja uus Ubuntu 14.04, kuid Sertifitseerimiskeskus pole jõudnud veel 
tarkvarapakette välja lasta.
`Tallinna koolide Linuxile ülemineku <http://bitbucket.org/lauri.vosandi/lauri-edu>`_ jaoks oli vaja
ID-kaardi pakette Ubuntu 14.04 jaoks ning seetõttu sai end kokku võetud ja pbuilder abil tarkvarapaketid
Ubuntu 14.04 jaoks kompileeritud.
Debian Wheezy ja Jessie jaoks olid minu tehtud paketid juba mõnda aega olemas.

Olemasolevate pakketide eemaldamine
-----------------------------------

Kui oled proovinud muid juhendeid siis võib juhtuda et neist on üleliigset kraami
jäänud peale ja seega enne kui jätkad on soe soovitus maha võtta muu kama:

.. code:: bash

    sudo rm /etc/apt/sources.list.d/ria-repository.list
    sudo apt-get purge esteidcerts esteidcerts-dev esteidcerts-fin \
        esteidfirefoxplugin esteidpkcs11loader \
        libdigidoc-common libdigidocpp-common \
        qesteidutil qdigidoc opensc

Paigaldus
---------

Tarkvarapaketid on kättesaadavad minu isiklikust tarkvarahoidlast mille saab lisada järgnevalt:

.. code:: bash

    echo "deb http://packages.koodur.com $(lsb_release -c -s) main" | \
        sudo tee /etc/apt/sources.list.d/koodur.list
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B8A6153D

Tarkvarapakettide paigaldamiseks:

.. code:: bash

    sudo apt-get update
    sudo apt-get install estonianidcard
    
Nimetatud käsud töötavad järgnevate distributsioonide ja arhitektuuride peal:

* Ubuntu Trusty Tahr 14.04 (amd64/i386)
* Linux Mint 17 (amd64/i386)
* Debian Wheezy 7.4 (amd64/i386/armel/armhf) 
* Debian Jessie (amd64/i386/armel/armhf)

Eelduseks on lsb_release käsu olemasolu, kui see mingil põhjusel puudu on siis:

.. code:: bash

    sudo apt-get install lsb-release
    
Sanity check
------------
    
Nimetatud sammude tulemusena peavad olema paigaldatud järgnevad pakettide versioonid
Ubuntu 14.04 ning Linux Mint 17 peal:

.. code::

    ii  opensc                                                0.13.0-3ubuntu4.1ria1koodur0                        amd64        Smart card utilities with support for PKCS#15 compatible cards
    ii  libdigidoc-common                                     3.8.0.1133-99koodur2                                all          DigiDoc library common files
    ii  libdigidoc-tools                                      3.8.0.1133-99koodur2                                amd64        DigiDoc library tools
    ii  libdigidoc2:amd64                                     3.8.0.1133-99koodur2                                amd64        DigiDoc library
    ii  libdigidocpp-common                                   3.8.0.1208-99koodur2                                all          DigiDocPP common files
    ii  libdigidocpp-tools                                    3.8.0.1208-99koodur2                                amd64        DigiDocPP tools
    ii  libdigidocpp0:amd64                                   3.8.0.1208-99koodur2                                amd64        DigiDocPP library
    ii  qdigidoc                                              3.8.1.1250-99koodur1                                amd64        DigiDoc UI applications
    ii  esteidcerts                                           3.8.0.9128-99koodur3                                all          Estonian ID card certificates
    ii  esteidfirefoxplugin                                   3.8.0.1115-99koodur2                                amd64        Firefox ID card plugin
    ii  esteidpkcs11loader                                    3.8.0.1052-99koodur2                                all          esteid PKCS#11 module loader
    ii  qesteidutil                                           3.8.0.1106-99koodur3                                amd64        Smart card manager UI application

Seda saab kontrollida järgnevate käskudega:

.. code:: bash

    dpkg -l | grep opensc
    dpkg -l | grep digidoc
    dpkg -l | grep esteid
    
Kui mõni veider versiooninumber on paigaldatud siis ma oleks sellisest situatsioonist
ka huvitatud ning võid järgneva käsu väljundi mulle saada:

.. code:: bash

    apt-cache policy paketinimi-mis-on-piiksus


Firefox
-------

Debian Wheezys on OpenSC 0.12.2 mis tähendab et onepin teek on olemas ning
Firefoxiga probleeme olla ei tohiks.
Ubuntu 14.04 jaoks on minu pakettide varamus SK modifitseeritud OpenSC 0.13 mis 
toob tagasi onepin teegi, see tähendab et Firefoxis autentimine ning allkirjastamine
peaks toimima.

Debian Jessie peal on OpenSC 0.13.0, mis tähendab et Firefoxis autentimine ei toimi õigesti.
Debian Jessie kasutajad võivad torkida, kui huvi on
siis võin OpenSC pätsid üle tuua.
Hetkel on mu Debian Jessie masinaks Cubietruck ja Firefoxi jaoks on see masin naguinii liiga aeglane.

Firefoxis on LHV-sse sisselogimine ikka katki aga tegelikult on see LHV enda probleem, et nad ID-kaardiga
sisselogimiseks vajalikke sertifikaate oma veebiserverist välja ei jaga nii nagu Swedbank ja SEB seda teevad.

Google Chrome ja Chromium
-------------------------

Lisasin *esteid-update-nssdb* skripti mis tõmmatakse sisselogimisel Xsession.d kaudu käima.
See skript lisab Google Chrome ja Chromium jaoks ID-kaardi toe ning parandab samas ka LHV-sse sisselogimise nendes veebilehitsejates.

Ubuntu 14.04 peal tehti midagi Google Chrome ja Chromiumiga, mis tähendab et
Ubuntu peal satub Chrome segadusse kumba PIN-i küsida autentimisel samamoodi nagu Firefox veebilehitsejaski.
Kui seal PIN2 dialoog ette peaks hüppama tuleb pressida Escape nuppu seni
kuni küsitakse ikkagi PIN1 koodi.

Ubuntu 14.04 puhul on komistasin ka mingi säärase vea otsa et Chromium mingis asendis
ei reageeri klaviatuuri nupuvajutustele, eeldan et see on äsjase väljalaske
tooruse viga lihtsalt ning mõne aja möödudes kaovad säärased anomaaliad.
Selle ravimiseks pidi eemaldama *ibus* nimelise paketi.

Google plaanib
`2014 aasta jooksul eemaldada ebaturvalise NPAPI toe <https://developer.chrome.com/extensions/npapi>`_
Chrome/Chromium veebilehitsejatest mis tähendab, et ID-kaardiga allkirjastamine **lakkab töötamast**
kuna seni on Chrome/Chromium kasutanud Firefoxi NPAPI allkirjastamise pistikprogrammi.
Uue Pepper Plugin API jaoks aga allkirjastamise pistikprogrammi hetkel pole kirjutatud,
see peaks välja tulema uue ID-kaardi tarkvara versiooniga 3.9.

Kokkuvõte
---------

Debian Wheezy peal peaks töötama kõik õigesti nii Firefoxi, Iceweaseli, Google Chrome kui Chromiumiga.
Debian Jessie peal peaks töötama kõik õigesti Google Chrome ja Chromiumiga.
Ubuntu 14.04 peal peaks kõik töötama õigesti Firefoxiga ning nagu öeldud
täisväärtuslik Chromium/Chrome tuge võib oodata juunikuus.
Vanemate Ubuntuliste jaoks soovitan tarbida ametlikke pakette.
Kui midagi (muud) ei tööta siis võite ikka julgelt mulle e-kirjakese teele saata.
Annetused on ikka teretulnud, ega open-source aktivistid ainult õhust ja armastusest ela ;)

