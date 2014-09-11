.. title: Arduino workshop ja avatud lähtekoodi tähtsusest hariduses
.. date: 2014-01-03
.. tags: Arduino, education, open-source

Arduino workshop ja avatud lähtekoodi tähtsusest hariduses
==========================================================

Eelsõna
-------

Käesolev postitus sai kiirelt kokku visatud
3. jaanuari hommikul erinevate koolide IT juhtidele ning õpetajatele
orienteeritud `Vaba Tarkvara seminaril <https://docs.google.com/file/d/0B1O3ZyIuaTKiWjdOMmZ1RVlEOHM/edit?pli=1>`_.

Tähelepanu keskpunktis oli eelkõige asjaolu, et koolides kasutatav Microsofti
tarkvara litsenseerimise hind oleks pidanud tõusma pea 10 korda 2014 aastal, sest
Microsofti näitajate järgi pole Eesti enam arenguriik. Haridusministeerium
sai Microsoftiga
`kokkuleppele <http://www.postimees.ee/2636832/ministeerium-voitles-haridusasutustele-valja-windowsi-soodushinnad>`_,
et 2014-2014 aastatel saaks kasutada
Microsofti tooteid hinnatõusule eelneva hinnaga.
Jätkusuutlikkuse huvides tuleb töötada selle nimel, et Eesti saavutaks
ka IT taristu poolest iseseisvuse.

.. youtube:: myryz4wnx70#t=2h44m48

Nüüd saab Youtube vahendusel ka nimetatud ürituse videot vaadata,
selleks et paremini edasi anda postituses mainitud mõttenupukesi.

Sissejuhatus
------------

Tänapäevane tarbimiskeskne arvutimaailm surub kogu IKT tööstust ning ka haridust
teatud suunas.

* `Miks lapsed ei oska arvuteid kasutada ja miks see peaks muret valmistama?
  <http://coding2learn.org/blog/2013/07/29/kids-cant-use-computers/>`_
* `Kaks erinevat kultuuri arvutimaailmas
  <http://pgbovine.net/two-cultures-of-computing.htm>`_
  
Peamisteks probleemideks on teadmatus ja õpitud abitus ning kõige suurem jõud
mis edasi ei lase liikuda on mugavustsoon.
Mida ette võtta ning missugune peaks välja nägema haridus 5, 10 või 20 aasta pärast?


Vaba tarkvara
-------------

Selleks et vältida tootjalukku on tuleks tootjatelt nõuda valikuvabadust.
Windows 8 nõuab
`SecureBoot <http://en.wikipedia.org/wiki/Unified_Extensible_Firmware_Interface#Secure_boot>`_
võimekust sülearvutitelt, mis teeb veelgi keerulisemaks alternatiivse operatsioonisüsteemi paigalduse,
võttes seega ära valikuvabaduse.

Operatsioonisüsteeme töölauale ning sülearvutile:

* `Ubuntu <http://www.ubuntu.com/>`_ - Kõige modernsem Linux põhine operatsioonisüsteem sülearvutile.
* `Debian <http://www.debian.org/>`_ - Pika ajalooga Linuxi põhine vaba tarkvara kogumik lauaarvutile ning sülearvutile.
* `Gentoo <http://www.gentoo.org/>`_ - Linux põhine operatsioonisüsteem töölaua
  masinale, selleks et õppida kuidas üks modernne operatsioonisüsteem toimib.

Telefonidele ning muudele "purkidele":

* `CyanogenMod <http://www.cyanogenmod.org/>`_ - Tarkvara Anrdoid telefonide järelturule.
* `OpenWRT <https://openwrt.org/>`_ - Avatud lähtekoodiga tarkvara marsruuteritele.
* `Rockbox <http://www.rockbox.org/>`_ - Avatud lähtekoodiga tarkvara muusikapleieritele.

Kui laps soovib proovida näiteks Ubuntut, siis peaks looma soodsa pinnase
selle kontakti tekkeks.


Vaba raudvara
-------------

Tehnoloogia läheb iga päevaga odavamaks ning energiasäästlikumaks.
Tänapäeval on kättesaadavad väga odavad krediitkaardisuurused arvutid,
mis teeb võimalikuks väga odavalt õppida elektroonika, programmeerimise ning
arvutite aluseid:

* `Arduino </bootcamp/arduino/>`_
* Raspberry Pi
* `BeagleBoard ja BeagleBone <http://beagleboard.org/>`_
* `Cubieboard, Cubieboard2 ja Cubietruck </blog/cubieboard2.html>`_
* `LEGO Mindstorms <http://www.lego.com/en-us/mindstorms/>`_

Praegu elame huvitaval ajastul kuna 3D printimine läheb aina odavamaks aga
praegune õigussüsteem ei ole ühilduv nende võimalustega.

* `RepRap <http://reprap.org/>`_ - kodustes tingimustes 3D printimine ning CNC töötlus
* `Open Source Ecology <http://opensourceecology.org/>`_ - kõik eluks vajalik


Õppimine veebis
---------------

Veebis saab õppida programmeerimist ja nii mõndagi muud:

* `Codeacademy <http://www.codecademy.com/>`_ - erinevad programmeerimiskeeled
* `Code <http://code.org/>`_ - programmeerimine algajale, Python ning JavaScript
* `Khanakademy <https://www.khanacademy.org/>`_ - matemaatika, teadus, programmeerimine

Vaba tarkvara, selle dokumentatsioon ning lähtekood võimaldab
õppida kuidas erinevates tarkvaraprojektides probleeme lahendatakse.
Programmeerimise õpetamine aitab aru saada matemaatikast, füüsikast,
interneti ülesehitusest.
Üks oluline aspekt mis kahe silma vahele jääb on ka see, et programeerimine
õpetab ennast väljendama üheselt mõistetavalt.

Veebiarendusest
---------------

Veebistandardid võimaldavad inimese moel tarkvara arendada. Paljude
programmeerimiskeeltega saab üsna lihtsalt kokku visata veebirakenduse
mis asendab tüüpiliselt kontoritarkvara paketiga koostatavat vormi.

* `Django <https://www.djangoproject.com/>`_ - Pythoni fanaatikutele
* `Ruby on Rails <http://rubyonrails.org/>`_ - Ruby hipsteritele
* `nodejs <http://nodejs.org/>`_ - JavaScripti fännidele

Mis kõige olulisem, andmed sellisel kujul on töödeldavamad.
Näiteks Pythonis kokku visatud skript ei erine kuigi Excelis valemite sisse toksimisest.

 
Küljendamine
------------

Matemaatika valemite ja muude keerukate dokumentide koostamiseks on ainus reaalselt
kasutatav vahend LaTeX:

* `LaTeX <http://latex-project.org/guides/>`_

Pisut pehmem variant on reStructuredText või Markdown:

* `reStructuredText <http://docutils.sourceforge.net/rst.html>`_
* `Markdown <http://daringfireball.net/projects/markdown/>`_

Informatsioon on oluliselt käideldavam kui seda saab mõne programeerimiskeele
abil töödelda. Väljundiks võib olla HTML, PDF või mis iganes.

Privaatpilve tarkvara
---------------------

Google on muutumas uueks Microsoftiks mistõttu tõstataksin siinkohal
privaatpilve teema. Suvalisest Raspberry Pi-st või Cubieboard-ist saab teha
privaatpilve majutava purgi:

* `OwnCloud <http://owncloud.org/>`_
* Olemasolevatest juppidest midagi kokku visata


Turvalisusest
-------------

Kinnine lähtekood on kogu riigi julgeolekurisk:

* `Turvaaukudest Microsofti toodetes
  <http://www.techdirt.com/articles/20130614/02110223467/microsoft-said-to-give-zero-day-exploits-to-us-government-before-it-patches-them.shtml>`_
* `Turvaaukudest 3G ja 4G modemites
  <http://www.osnews.com/story/27416/The_second_operating_system_hiding_in_every_mobile_phone>`_
* `Turvaaukudest D-Link marsruuterites
  <http://www.infoworld.com/d/security/backdoor-found-in-d-link-router-firmware-code-228725>`_
* `Turvaaukudest paljudes Netgear, Cisco ning Linksys marsruuterites
  <http://arstechnica.com/security/2014/01/backdoor-in-wireless-dsl-routers-lets-attacker-reset-router-get-admin/>`_
* `SIM kaartide turvalisusest 
  <http://www.forbes.com/sites/parmyolson/2013/07/21/sim-cards-have-finally-been-hacked-and-the-flaw-could-affect-millions-of-phones/>`_

