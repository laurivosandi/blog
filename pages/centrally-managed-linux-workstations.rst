.. title: Keskselt hallatud Linux baasil tööjaamad
.. flags: hidden
.. date: 2014-05-31

Üline loogika
-------------

Terminali sisemise mälu tõmmis luuakse Debian, Ubuntu vms populaarse
distributsiooni baasil mille pakihalduses on hulgim pakette mille seast
saab valida juba binaarkujul olevat tarkvara.
Deploymentis me ei sõltu distributsiooni paketihaldusest kuna sellega
võib ikka tihtipeale jalga tulistada.
Selle asemel me loome `universaalse vahendi
<http://www.igorpecovnik.com/2013/12/24/cubietruck-debian-wheezy-sd-card-image/>`_
millega sisemise mälu tõmmist hõlpsalt luua saab.
Terminalide tarkvarauuendus seisneb uue testitud tõmmise
alla laadimises ning alglaaduri ümberlülitamises uuele tõmmisele.
Niiviisi on välistatud sisemise mälu korruptsioon, paketihalduse õhkulendamine vms
problemaatilised stsenaariumid.

Terminali seadistamiseks pakume välja teksti-režiimi rakenduse mille
ligi pääsemiseks tuleb a'la vajutada Ctrl-Alt-F2 ning sisse logida
konkreetse terminali admin kontoga.
Sellest `menüüpõhisest rakendusest <https://github.com/v6sa/socle/>`_ saab seadistada
terminali masinanime, võrguseadeid, lähtestada kaughalduse ja/või VPN võtmeid jne:

.. image:: http://lauri.vosandi.com/shared/soc-config/mainmenu-cubietruck.png
    :align: center

Terminal teeb alglaadimise vaikimisi sisselogimishaldurisse kust siis
saab sisse logida terminal-serverisse kas rdesktop abil või tuleviku
mõttes algatada kohalik töölauasessioon kus saab ainult Chromium veebilehitsejat tarbida.

Taustal jookseb kaughaldussüsteem mille kaudu seadistame terminali,
uuendame terminali juurfailisüsteemi
tõmmist ning näiteks korjame kokku terminali virtuaalprivaatvõrgu avalikke RSA võtmeid.
Kui kaughaldussüsteemi poolt on terminal heaks kiidetud
võetakse üles virtuaalprivaatvõrgu tunnel, misjärel on võimalik hakata
kasutama teenuseid tunneli kaudu.

Terminalide haldamiseks pakume välja modernse veebiliidese
mis kasutab `Flaskis <http://flask.pocoo.org/>`_ kirjutatud API-keskse
veebiserveriga suhtlemiseks RESTful lähenemist.
Andmebaasiks on MySQL kuhu logitakse kogu VPN-i tegevus.

Printimiseks/skänneerimiseks pakume välja `kohandatud seadme (?) <https://www.indiegogo.com/projects/vocore-a-coin-sized-linux-computer-with-wifi/>`_ millel
puuduvad ekraan, klaviatuur ning hiir. Selle asemel on sinna
ühendatud pinpadiga kaardilugeja ning peale autentimist 
lähevad printimisse kõik PDF (?) dokumendid mis on terminalserveri kodukataloogis
a'la ~/Ootel all.
Skänneerimisega analoogselt kasutaja vajutab skänneril nuppu ning
kui skänneerimine on valmis siis see fail laaditakse üles
kodukataloogi ~/Skänneeritud vms alla.
Kuna printeri/skänneritega on Linuxis alati hädad tuleb võtta ette mõni
kombain mis reklaamib Debiani tuge (nt Lexmark) ning ära testida funktsionaalsus:
kas skännimise nupud töötavad ning kas printimine on lollikindel.

Tehtavad tööd
-------------

* Universaalne terminali juurfailisüsteemi generaator x86 ja armhf jaoks, Lauril on juba nii mõndagi töös.
* Terminali `seadistamisvahend <https://github.com/v6sa/socle/>`_, Lauril on juba midagi olemas.
* VPN lüüsi ja terminalide tulemüüri seadistused, Lauri teha.
* SaltStack/Puppet konfiguratsioon VPN lüüsi masinale, terminalidele ning print/skännboksile, Lauri teha
* Terminalide tõmmise uuendamise mehhanism mis võiks olla väga elegantne 
  `kasutades kaughaldust ning differentsiaaltihendamist
  <http://stackoverflow.com/questions/23279147/git-like-versioning-system-based-on-squashfs-and-aufs>`_.
  Kas panna tõmmised ext4 sisse või a'la lüüa 8GB flash kaheks 4GB partitsiooniks?
  Read-only juurfailisüsteem vajab veidikene uurimist sest nii mõnigi 
  teenus eeldab kirjutatavat juurfailisüsteemi. See selgub Rahvusraamatukogu
  Cubietruckide piloodis augustikuu algul.
  Võibolla tuleb kombineerida aufs abil midagi? A'la read-only Squashfs baas,
  read-only Squashfs diffid ning selle peale read-write kiht mis on ajutine.
* Kaughalduse ja VPN-i võtmete haldamise, IP whitelist (?), juurfailisüsteemi tõmmiste haldamise veebiliides,
  Priit (?)
* Print/scan lahendus. Kui on ekraaniga kaardilugeja kuidas ja kas saame
  mingit teksti ekraanile ka näidata? Ehk saame lahendada scp abil üsna hõlpsalt,
  kaart sisse, PIN1 sisestamine, print ja failide kustutamine serverist.
  Skännimisega analoogselt, dokument saab skännitud, sisestad PIN-i ning
  scp-ga lükatakse serverisse. ssh-agent abil saame vast PIN-i meelde ka jätta
  et senikaua kuni kaart sees on ei pea iga dokumendi jaoks PIN-i sisse tokisma.
  Kui tulevikus terminal-server asendub veebiserveriga siis võibolla on asjalikum
  teha muidugi HTTPS ühendusega midagi. Priit (?)
  
Kõigi kohta jääb õhku rippuma intellektuaalomandi küsimus. Juurfailisüsteemi generaator
ja seadistamisvahend on juba praegu avalikud ja mida rohkem kasutajaid sellel
on seda parem meile.
Kaughalduse ja VPN-i võtmehaldus samamoodi kuluks ära teistele ning seeläbi
parandaks ka meie koodi kvaliteeti.
Kõige kriitilisem teave on muidugi kaughalduse konfiguratsioonis ning
kaughalduse konfiguratsiooni nagu ka suvalisi shelliskripti juppe muidugi avalikuks ei tee.

Kaughaldus
----------

Puppet on üks vanimaid kaughaldussüsteeme ning tal on ka kaasaegne veebiliides
Foreman millega saab võtmeid signeerida ning saada ülevaade toimuvast.
Puppeti klientrakendus on võrdlemisi uimane ning
igasuguste muudatuste rakendamisel on märgatav latentsus (30min) kuna klient
ei hoia ühendust lahti serveriga kogu aeg.
Puppet majandab võtmetega traditsioonilselt CA abil.
Puppeti abil haldame praegu `150 masinat 5 koolis <https://bitbucket.org/lauri.vosandi/lauri-edu>`_.

SaltStack on pisut modernsem lahendus mis võimaldab rakendada muudatusi praktiliselt
reaalajas. Saltil hetkel kasutuskõlblik veebiliides puudub.
Salt ei kasutada CA-d, selle asemel on tal nimekiri lubatud avalikest RSA võtmetest,
nii nagu OpenSSH puhulgi.


VPN tunnel
----------

Suurema koguse terminalide haldamiseks on mitu varianti:

* OpenVPN TAP režiimis, CA signeeritud sertifikaatidega, CSR-id saab kaughalduse abil kokku korjata
* StrongSwan, CA signeeritud sertifikaatidega
* StrongSwan, PSK võtmega mida saab jagada kaughalduse vahendusel
* OpenSSH koos -w argumendiga võimaldab IP forwardit teha, autentimine RSA võtmetega
* OpenSSH koos -R võtmega saab port forwardit teha, autentimine sama

Plussid-miinused: Heartbleed puudutas OpenVPN-i aga mitte StrongSwani ega OpenSSH-d.
OpenSSH puhul on liiklus kapseldatud TCP ühendusse mis võib probleeme tekitada
halva ühendusega kohtades.
StrongSwani üles seadmine on mahukas aga tehtav.
OpenVPN-i kohta olen mitmeid `koolitusi teinud <http://www.itcollege.ee/taiendusope/koolitused/koolituskalender/?event_id=69>`_ ja ütleks et tunnen teda
läbilõhki.

Ubuntu terminal-serveriks
-------------------------

Üleüldsiselt loeksin ma terminal-serverid surnud tehnoloogiaks ning
ainus reaalselt tulevikukindel tehnoloogia on HTML5 kus videovoogude edastamine
on optimaalselt lahendatud. Chromiumi FFMPEG plugina saab näiteks juba praegu
panna kasutama riistvaralist videodekoordit VDPAU kaudu.

Kui aga peaks olema suur tahtmine Ubuntut kasutada serveri poolel siis
variante on väga palju igaühel plussid ja miinused.
Käesolev peatükk käib eelkõige selle pihta et kuidas Linux (ja Windows) terminalist
teha Linuxi serverisse kaugtöölauda:

1. `X11rdp <http://scarygliders.net/x11rdp-o-matic-information/>`_ on pätsitud
   Xorg 7.1 mis kompileerib kokku X serveri RDP serveriga.
   Peaks teoorias olema üsna optimaalne kui on õigesti realiseeritud.
   Autentimist, sessioonihaldust ning X11rdp käivitamist viib läbi
   `xrdp <https://github.com/neutrinolabs/xrdp/>`_ ning
   xrdp oskab üle tuua heli, kiipkaarte ning USB mälupulki.
   Windowsi remote desktop klient on ühilduv xrdp-ga.
   xrdp-l on ka hulgim autentimisvahendeid.
   Kui serveri poolel käitatakse Linuxilist siis tuleb kasutada `kohandatud PCSC-Lite
   teeki <http://sourceforge.net/p/xrdp/mailman/message/32249390/>`_ selleks
   et serveris käitatavad rakendused saaks ligipääsu terminali külge ühendatud kiipkaardile.
   Ubuntu 14.04 baasil terminal-serveri panime käima rdp.povi.ee masinas.
   Plussid: sama protokoll mis Windowsi terminal-serveril,
   terminal-serveris saab sessiooni käima jätta ning hiljem uuesti ühenduda.
   Miinused: keerukas üles seada Linuxi baasil serverit aga tehtav,
   võimalik et vaja teha ootamatuid arendustöid selleks et värskemate
   opsüsteemidega/teekidega käima saada toimib kooslus.
   
2. Tihendatud/kiirendatud X11
   (`NX <https://www.nomachine.com/download>`_,
   `LBX <http://en.wikipedia.org/wiki/Lbxproxy>`_,
   `dxpc <http://en.wikipedia.org/wiki/Dxpc>`_, 
   `FreeNX <http://freenx.berlios.de/>`_,
   `Neatx <https://code.google.com/p/neatx/source/browse/#svn%2Ftrunk%2Fneatx%2Flib>`_).
   Sisuliselt tegu LTSP5 + tihendusega, NoMachine pakkus klientrakendust ka Windowsi jaoks.
   Arendust enam eriti ei toimu nimetatud (vabamates) projektides.
   Plussid: iseenesest hea tehnoloogia, toimib üsna hästi üle interneti kui omal ajal proovitud sai.
   Miinused: NoMachine vahendid on osaliselt kinnise lähtekoodiga ning avatud lähtekoodiga analoogide
   puhul on vaja palju pusida.
   
3. LTSP5 - Tunneldab X11 protokolli, PulseAudio läbi OpenSSH tunneli.
   ltspfs on FUSE moodul mis võimaldab serverisse tuua kohalikult haagitud failisüsteeme
   (USB mälupulki ja kõvakettaid).
   Selleks et serveris käitatav rakendus saaks ligipääsu terminali ühendatud 
   kiipkaardile tuleb paigaldada
   `minu kohandatud OpenSSH server </posts/ubuntu-precise-pangolin-ltsp-ja-id-kaart.html>`_ mis
   võimaldab üle tuua UNIX sokkleid mida PCSC-Lite kasutab.
   Plussid: võrdlemisi lihtne üles seada lightdm abil
   Miinused: Vajab märgatavalt rohkem arvutusvõimsust terminalidest krüpteerimise jaoks,
   latentsus on samamoodi probleemiks nagu LTSP4 puhulgi,
   video vaatamine koormab võrku kuna videovoog liigub küll pakitud OpenSSH tunnelis,
   kuid mitte optimaalsel kujul.

4. LTSP4 - Ajaloolise väärtusega projekt, tööjaamades käitati X11 serverit,
   rakendusi käitati keskses serveris ning videoväljund suunati tööjaama (DISPLAY=12.34.56.78:0.0).
   Heli jaoks kasutati Enlightened sound daemonit ning analoogselt X11-le suunati
   see ümber terminalidesse.
   Plussid: võrdlemisi lihtne üles seada kuna tugi olemas distributsioonides.
   Miinused: turvalisus, X11 on krüpteerimata ning võrku pealt kuulates
   saab kätte kõik mida kasutaja trükib töömasinas ning mida kasutajale kuvatakse.
   Eeldab ka kiiret võrku kuna X11 protokoll ei olnud disainintud kõrge latentsusega ühenduste jaoks,
   video vaatamine koormab võrku kuna videovoog liigub võrgus pakkimata kujul.

5. VNC - Kõige vanem tehnoloogia, sisuliselt ainult pildi edastamine.
   Kood xrdp-ga tarbides saab ehitada ilmselt toimiva süsteemi nii et xrdp
   teeb heli, smartcard ja USB pulkade edastamist. Sobib kõrge latentsusega linkide jaoks.

6. `FreeRDS <https://github.com/FreeRDS/>`_ on xrdp fork mis peaks linkima
   X11rdp süsteemsete X11 teekide vastu ja üleüldisemalt korrastama seisu.
   #freerdp@Freenode tegelaste sõnul toores ja vajab aega.

7. GTK3 teegi kooseisu kuuluval komponendil GDK on Broadway backendi tugi mis
   võimaldab GDK-l baseeruvaid rakendusi
   `kuvada veebibrauserisse <http://worldofgnome.org/running-gtk-apps-on-web-with-node-broadway/>`_.
   Isegi kui GTK3 rakendused sellega töötaks siis Qt rakenduseld oleks ikkagi
   problemaatilised ning jätkuvalt on kasutuses palju GTK2 rakendusi mis
   oleksid samamoodi problemaatilised.
   Igal juhul see variant vajab palju lisatööd autentimismehhanismi ehitamiseks.

8. `GateOne <https://github.com/liftoff/GateOne/>`_ on HTML5 SSH klient mis
   pakub erinevaid autentimismeetodeid: GSSAPI (Kerberos), PAM.
   Demolehel on näha SMPlayerit mängimas FullHD videot aga
   aga koodibaasis pole kippu ega kõppu lubatud X11 kohta.

9. `Guacamole <http://guac-dev.org/>`_ on remote desktopi lüüs mis võimaldab
   veebibrauseriga ligipääsu VNC, RDP, SSH ja telnet teenustele.
   Guacamole tõlgib nimetatud protokollid ümber JavaScripti jaoks söödavasse formaati.
   ID-kaardi autentimise realiseerimine ilmselt vajab tööd.
   ID-kaardi ületoomine serverisse ilmselt raske kui mitte võimatu.


   
ID-kaart vs terminal-serverid
-----------------------------

ID-kaardi juures tuleks tähele panna seda et terminal-serveri juures on kolm
aspekti:

1. Kas kaugtöölaua ühenduse autentimiseks saab terminalis ID-kaarti kasutada?
2. Kas kaugtöölauaprotokoll/lahendus toob üle ligipääsu kaardilugejale?
3. Kas serveris käitatav tarkvara oskab liidestada ennast kaugtöölauaserveri/lahendusega?

Rahvusraamatukogu praeguses LTSP5 installatsioonis lõin ma lahenduse 2 ja 3 jaoks.

Serveri ja terminali vahelise side turvamine
--------------------------------------------

* Veebipõhiste rakenduste juures saab kasutada HTTPS-i
* LTSP5 baseerus OpenSSH peal mis juba krüpteerib ühendusi
* RDP 5.2 protokoll toetab samuti krüpteerimist aga selle tugi xrdp-s ega
  rdesktop-is pole kindel
  
  
Terminalide riistvara
---------------------

Terminalide riistvara valikuks pakuksin välja mitu varianti.
Kõige tavalisema x86 kasuks räägivad paindlikkus ja universaalsus aga jätkuvalt
on probleemiks energiatarve.
Igal juhul tuleks vältida liikuvaid osi (ventilaator, kõvaketas).
Tihtipeale on probleemiks ka toiteplokkide kondensaatorid mis kipuvad lekkima
mille tagajärjel riknevad ka emaplaadi komponendid.
ARM plaatide hulgas on viimasel ajal ilma teinud Hiina brändid
Allwinner ja Rockchip, nende mõlemi kasuks räägib hind kuna mängust 
on välja lõigatud lääne bränd kes oma kasu vahelt lõikab
ning võib spekuleerida et ka oma tagauksed sisse paneb.
Muidugi on alust arvata, et
`Hiina luureagentuurid tegelevad analoogse tegevusega <http://www.zdnet.com/former-pentagon-analyst-china-has-backdoors-to-80-of-telecoms-7000000908/>`_.
Peale lahti kirjutatud ARM plaatide on palju teisigi:

`CuBox-i4-Pro <http://imx.solid-run.com/product/cubox-i4-pro/>`_,
`Minix NEO X8 <http://www.minix.com.hk/Products/MINIX-NEO-X8.html>`_,
`M8 Amlogic S802 <http://www.amazon.com/M8-Bluetooth-Streaming-Tronsmart-Ethernet/dp/B00JDCO22I/ref=sr_1_fkmr1_1?ie=UTF8&qid=1403526644&sr=8-1-fkmr1&keywords=m805+amlogic>`_,
`Arndaleboard <http://www.arndaleboard.org/>`_,
`Origenboard <http://www.origenboard.org/>`_
`Utilite Trim-Slice <http://utilite-computer.com/web/models>`_,
`Cubietruck 8 <http://cubieboard.org/2014/05/04/cubietech-will-promote-a80-high-performance-mini-pc/>`_,
`VIA VAB-1000 <http://www.viaembedded.com/en/products/boards/2190/1/VAB-1000_(Pico-ITX).html>`_.
ARM on praktiliselt kasutuskõlblikuks muutunud viimase paari aasta jooksul
tänu tootjatele kes reaalselt jagavad dokumentatsiooni ja lähtekoodi.
Situatsioon läheb veel märgatavalt paremaks kui `Wayland jõuab massidesse
<http://www.raspberrypi.org/tag/maynard/>`_.


Cubietruck
----------

`Cubietruck </posts/debian-jessie-sunxi-packages.html>`_ on Allwinner A20 SoC baasil toodetud
energiasäästlik (max 10W) ARM protsessoril põhinev plaat:

.. image:: http://www.seeedstudio.com/depot/images/product/Cubietruck_03.jpg
    :align: center

Cubietrucki spetsifikatsioon:

* Kahetuumaline ARM Cortex-A7 @ 1GHz
* 2GB DDR2 @ 528MHz
* 8GB NAND välkmälu
* Mali400 MP2 videokaart
* CedarX 2160p video dekooder
* HDMI digitaalvideo väljund
* VGA analoogvideo väljund
* SPDIF digitaalaudio väljund
* 1Gbps Realtek RTL8211E juhtmega võrk
* Broadcom BCM4329 802.11bgn juhtmeta võrgukaart
* Broadcom BCM40181 Bluetooth 4.0 liides
* 2x USB2.0 host
* 1x USB OTG
* 1x microSD pesa
* 1x SATA 2.0 pesa

Debian, Ubuntu tugi olemas ning
Fedora on valinud Cubietrucki oma ARM SoC toe testimiseks.
Võimalik kasutada VGA ja SATA porte mida praktiliselt ühelgi teisel ARM plaadil ei eksisteeri.
Lauri on Cubietrucki kasutanud üle poole aasta töölaua asendusena ning
Lauri poolt on olemas toimiv Chromium ja ID-kaardi tarkvara.
Augustikuus tuleb Rahvusraamatukokku 30 masinaga setup
kus kõik masinad teevad alglaadimist võrgust NFS abil.
    
Radxa Rock
----------

Radxa Rock on Cubietruckile analoogne Rockchip SoC baasil toodetud ARM plaat:

.. image:: http://www.seeedstudio.com/depot/images/product/radxa.jpg
    :align: center
    
Rockchip RK3188 SoC:

* Neljatuumaline ARM Cortex-A9, 2GB RAM
* 8GB NAND Flash mälu
* MicroSD mälukaardi pesa
* Mali400 video
* HDMI pesa
* 100Mbps LAN
* 150Mbps 802.11bgn
* Bluetooth 4.0
* S/PDIF heliväljund
* 2x USB2.0 host pesa
* 1x USB OTG pesa

Plaat on samamoodi energiasäästlik (max 10W) aga
VGA ja SATA porte pole, integreeritud on mikrofon (?!).
Rockchip SoC-ide Linuxi tugi on pisut kehvem kui Allwinneri omadel.




