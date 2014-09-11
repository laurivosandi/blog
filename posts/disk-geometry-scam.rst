.. title: Reedeõhtune virin ketaste teemal
.. date: 2011-04-29 21:51:19
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: rant, failbox

Reedeõhtune virin ketaste teemal
================================

Alustaks siis seekord tavalistest kõvaketastest. Arvutimaailma tundvad inimesed
teavad et 1 kilobait = 1024 baiti, 1 megabait = 1024 * 1024 = 1 048 576 baiti
ning 1 gigabait = 1024 * 1024 * 1024 = 1 073 741 824 baiti. Kui nüüd tähti
närida siis õigem oleks kasutada 1024 astmete jaoks termineid kibibyte,
mebibyte, gibibyte aga IT-inimeste seas pole see vedu võtnud. Küll aga
kõvakettatootjad on aga otsustanud kõvaketaste mahtuvust mõõta "õigetes"
SI-ühikutes. Praktikas tähendab see seda, et 1000GB ketas ongi ligilähedal
miljardile baidile:

.. code:: bash

    lauri@localhost:~$ fdisk /dev/sdb
    Command (m for help): p
    Disk /dev/sdb: 1000.2 GB, 1000204886016 bytes

Tehes siit nüüd kiire arvutuse ja eeldades, et failide suurusi mõõdan ma ikka
1024 kordsetena nagu normaalne arvutikasutaja, tuleb välja et oma arust makstud
1000GB asemel saan ma kettale kirjutada 931GB andmeid ning 69GB jagu on mulle
tünga tehtud! Protsentides oleks see umbkaudu 7% jagu.

Minnes edasi nüüd SSD ehk pooljuhtketaste juurde, siis asi on veel absurdsem.
Ketastele peale märgitud suurused nt. 128GB väljendavad füüsiliselt kasutatavat
andmemahtu, tegelikkuses on pooljuhtketaste omapäraks see, et osad plokid
hapnevad kirjutustsüklite ammendumisel. Selle raviks on tarbija makstud ruumist
eraldatud mingi hulk plokke, nt 8GB *remap*-imise jaoks. Kasutaja jaoks on
seetõttu partitsioneeritav ainult 120GB:

.. code:: bash

    lauri@localhost:~$ smartctl -i /dev/sda
    smartctl 5.40 2010-10-16 r3189 [x86_64-redhat-linux-gnu] (local build)
    Copyright (C) 2002-10 by Bruce Allen, http://smartmontools.sourceforge.net
    
    === START OF INFORMATION SECTION ===
    Device Model:     ADATA SSD S599 128GB
    Serial Number:    00000000000000000082
    Firmware Version: 3.1.0
    User Capacity:    120,034,123,776 bytes
    Device is:        Not in smartctl database [for details use: -P showall]
    ATA Version is:   8
    ATA Standard is:  ATA-8-ACS revision 6
    Local Time is:    Sat Apr 30 00:29:14 2011 EEST
    SMART support is: Available - device has SMART capability.
    SMART support is: Enabled
    
    lauri@localhost:~$ fdisk /dev/sda
    Command (m for help): p
    Disk /dev/sda: 120.0 GB, 120034123776 bytes

Maakeeli tähendab see seda et makstud 128GB asemel saan ma kasutada vähem kui
112GB. Protsentides tähendab see umbkaudu 13% tünga. *Remap* ala suurus sõltub
tootjast, ADATA omadel rohkem, OCZ omadel vähem. OCZ pooljuhtketaste jaoks
leidus ka *püsivara* uuendamise tarkvara Linux jaoks erinevalt ADATA-st.

Kokkuvõttes üsna ebameeldiv kuidas tarbijaid lollitatakse numbritega ...




