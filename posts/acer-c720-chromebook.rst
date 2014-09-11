.. title: Acer Chromebook C720
.. date: 2013-12-14
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: Chromebook, Ubuntu, Haswell

Acer Chromebook C720
====================

Sissejuhatus
------------

Jõuluhulluses krabatakse poeriiulitelt igasugu mõttetu kraami.
Ei saa minagi selle kokkujooksva majanduskorralduse toetamist vahele jätta
ja seoses sellega sai tutvust tehtud Google Chromebookidega.
Acer C720 on üks kõige odavamaid Chromebooke, mida hetkel Berliinis saab
250€ eest.

Näitajad
--------

Selle hinna eest saab päris pädevate näitajatega pilli [#archlinux]_:

* 1366x768 lahutusvõimega LED-taustvalgustusega matt-ekraan.
* 16GB välkmälu kõvaketta asemel
* Kahetuumaline Haswell mikroarhitektuuril põhinev Intel Celeron 2955U 1.4GHz 64-bitine protsessor
* 2GB madala voolutarbega operatiivmälu
* Atheros AR9462 2.4/5GHz 802.11abgn + Bluetooth 4.0 võrguliides
* 1x USB2.0 ning 1x USB3.0 pesad
* HDMI liides
* Ethernet pesa puudub

ChromeOS
--------

Masin tuleb vaikimisi koos ChromeOS operatsioonisüsteemiga, mis on tegelikult
kõige tavalisem Linux käitab ainult ühte rakendust - Google Chrome'i.
Algaja ja tavakasutaja jaoks on see üpris okei asjatundja jaoks mõne koha pealt suht valuline kogemus.

Sisemine SSD on analoogselt Androidile jupitatud mitmeks:
kolm alglaaduri kettajagu, ChromeOS kettajagu, kasutaja failide kettajaod jne.
Huvitav tähelepanek oli see et kasutaja failid paiknevad AES krüpteeringuga
kettajaos, mida haldab arvatavasti arvuti protsessorisse ehitatud TPM kiip.

Mis on selle tagajärjed? Esiteks kui arvuti emaplaat maha peaks põlema,
ei saa kettalt faile kätte. Teiseks ma pakun et NSA-l on TPM-i äris käpp sees
ja saab vajalikud AES võtmed kätte ja ketta dekrüptida kui "vajadus" peaks tulema.
Teisalt ilmselt paljud kasutajad kasutavad Chromebooki nõnda et kõik
andmed on Google pilves naguinii varundatud. Selle masina soetamisega saab
Google Drive jaoks lisaks 100GB ruumi.

ChromeOS-is hetkeseisuga ID-kaarti kasutada ei saa. Teoorias peaks olema
võimalik käima saada Eesti ID-kaardi tarkvara ChromeOS all kuna
ChromeOS istub kõige tavalisema X-i otsas, küll aga peab omajagu pusima
et kompileerida vajalikud paketid ning ilmselt seda Google äppipoodi 
nii lihtsalt veel ei ilmu.


Ubuntu paigaldus
----------------

Vanematel Chromebookidel on üsna valus teist operatsioonisüsteemi paigaldada.
Käesoleval masinal saab arendaja režiimis (*developer* *mode*) sisse lülitada
*legacy* *BIOS*-e, mis tähendab et masinat käivitades vajutades Ctrl-L
siseneb masin SeaBIOS alglaadimisahelasse.
Sealt edasi saab käivitada USB pulgalt Debiani, Ubuntut või teha alglaadimine sisemisel kettal
asuva GRUB-i abil.

Arendaja režiimis saab ka nii mõndagi muud teha, näiteks *root* kasutaja õigustes
ChromeOS failisüsteemi lehitseda.
Ubuntu paigalduseks leiab ka skripti [#chrubuntu]_,
mille puhul pole paigldamiseks mälupulka üldsegi vaja.
Ubuntu all sai üsna hõlpsalt paigaldada ID-kaardi tarkvara Sertifitseerimiskeskuse
skriptide abil.

lspci, lsusb
------------

PCI Express seadmed (*lspci*):

.. code::

    00:00.0 Host bridge: Intel Corporation Haswell-ULT DRAM Controller (rev 09)
    00:02.0 VGA compatible controller: Intel Corporation Haswell-ULT Integrated Graphics Controller (rev 09)
    00:03.0 Audio device: Intel Corporation Device 0a0c (rev 09)
    00:14.0 USB controller: Intel Corporation Lynx Point-LP USB xHCI HC (rev 04)
    00:15.0 DMA controller: Intel Corporation Lynx Point-LP Low Power Sub-System DMA (rev 04)
    00:15.1 Serial bus controller [0c80]: Intel Corporation Lynx Point-LP I2C Controller #0 (rev 04)
    00:15.2 Serial bus controller [0c80]: Intel Corporation Lynx Point-LP I2C Controller #1 (rev 04)
    00:1b.0 Audio device: Intel Corporation Lynx Point-LP HD Audio Controller (rev 04)
    00:1c.0 PCI bridge: Intel Corporation Lynx Point-LP PCI Express Root Port 1 (rev e4)
    00:1d.0 USB controller: Intel Corporation Lynx Point-LP USB EHCI #1 (rev 04)
    00:1f.0 ISA bridge: Intel Corporation Lynx Point-LP LPC Controller (rev 04)
    00:1f.2 SATA controller: Intel Corporation Lynx Point-LP SATA Controller 1 [AHCI mode] (rev 04)
    00:1f.3 SMBus: Intel Corporation Lynx Point-LP SMBus Controller (rev 04)
    00:1f.6 Signal processing controller: Intel Corporation Lynx Point-LP Thermal (rev 04)
    01:00.0 Network controller: Qualcomm Atheros AR9462 Wireless Network Adapter (rev 01)

USB seadmed (*lsusb*):

.. code::

    Bus 001 Device 002: ID 8087:8000 Intel Corp. 
    Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
    Bus 003 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
    Bus 002 Device 003: ID 0489:e056 Foxconn / Hon Hai 
    Bus 002 Device 002: ID 1bcf:2c67 Sunplus Innovation Technology Inc. 
    Bus 002 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
    
Esimese tuuma */proc/cpuinfo* väljavõte:

.. code::

    processor	: 0
    vendor_id	: GenuineIntel
    cpu family	: 6
    model		: 69
    model name	: Intel(R) Celeron(R) 2955U @ 1.40GHz
    stepping	: 1
    microcode	: 0x15
    cpu MHz		: 800.000
    cache size	: 2048 KB
    physical id	: 0
    siblings	: 2
    core id		: 0
    cpu cores	: 2
    apicid		: 0
    initial apicid	: 0
    fpu		: yes
    fpu_exception	: yes
    cpuid level	: 13
    wp		: yes
    flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 cx16 xtpr pdcm pcid sse4_1 sse4_2 movbe popcnt tsc_deadline_timer xsave rdrand lahf_lm abm arat epb xsaveopt pln pts dtherm tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust erms invpcid
    bogomips	: 2793.61
    clflush size	: 64
    cache_alignment	: 64
    address sizes	: 39 bits physical, 48 bits virtual
    power management:

.. [#chrubuntu] http://chromeos-cr48.blogspot.de/
.. [#archlinux] https://wiki.archlinux.org/index.php/Acer_C720_Chromebook
