.. title: Asus WL500G Premium + Huawei E1750 + Elisa Mint
.. tags: OpenWrt, Asus WL500G Premium, 3G, Broadcom, Elisa
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. date: 2012-07-15

Asus WL500G Premium + Huawei E1750 + Elisa Mint
===============================================

Häkkimistuhinas tuli mõte et tahaks proovida mõne ruuteri küljes USB 3G pulga käima saada.
Katsetuseks sattusid parajasti Asus WL500G Premium ruuter ning EMT levitatav 3G pulk,
täpsema mudeliga Huawei E1750. SIM kaart oli Elisa pakutav MINT maks allalaadimiskiirusega 2MBit.

Esmalt ajasin ruuterile selga OpenWRT tarkvara.
Sellel ruuteril on pikka aega olnud võimalik jooksutada ainult 2.4 kernelil baseeruvat tarkvara,
seda enamjaolt Broadcomi WiFi kaardi tõttu.
See kivi on jalus olnud juba üle 8 aasta aga lõpuks on asjalikud mehed
reverse engineerinud b43 nimelise avatud lähtekoodiga tüüreli Broadcomi binaari baasil.

Ajaga kaasas käimine pole ainus põhjus kerneli 2.6 seeria kasutamiseks,
kiired HSDPA USB 3G modemid aga tahavad saada "optional" nimelist kerneli moodulit
mis hetkel töötab ainult 2.6 kerneli all.
Ilma "option" moodulita ei saanud ma 3G kaarti õigesti käima,
allalaadimiskiirus jäi 50 kilobaiti/sekundis piiresse ning ping oli kohutav.
OpenWRT pakub mõlema kerneli baasil tarkvara, 2.6 oma paigaldamiseks tuleks
sisse logida ruuterisse ning eeldusel et seal juba mingi Linuxi baasil OS toimib teha midagi sellist:

.. code:: bash

    cd /tmp/
    wget http://downloads.openwrt.org/backfire/10.03/brcm47xx/openwrt-brcm47xx-squashfs.trx
    mtd -r write openwrt-brcm47xx-squashfs.trx linux

Lootes et see tegevus ruuterist tellist ei tee, peaks ta taaskäivitama end ning
võimaldama telneti kaudu sisselogimist IP aadressil 192.168.1.1.
Järgmine samm on uuendada pakettide nimekirja ning paigaldada vajalikud paketid:

.. code:: bash

    opkg update
    opkg install kmod-usb-uhci kmod-usb-serial kmod-usb2 kmod-usb-serial-option comgt usb-modeswitch nano htop usbutils

Peale seda muutsin WAN seadistused failis /etc/config/network umbestäpselt selliseks.
See fail on osa OpenWRT standardsest võrguseadistusfailist ning OpenWRT kasutab
proto=3g puhul ühenduse käivitamiseks ülal märgitud comgt või vanema nimega gcom paketti.:

.. code:: bash

    config interface	wan
        option 'ifname' 'ppp0'
        option 'proto' '3g'
        option 'device' '/dev/ttyUSB0'
        #option 'apn' 'internet' # EMT
        #option 'apn' 'internet.tele2.ee' # TELE2
        #option 'apn' 'wap' # Elion (?)
        option 'pincode' '5101'
        option 'service' 'umts_only'
        option 'keepalive' ''
        option 'ppp_redial' 'persist' # Ühenduse katkemisel ühenda uuesti
        option 'pppd_options' 'noipdefault' # TELE2 häkk
        #option 'pppd_options' 'debug' # Vajadusel luba silumine logread kaudu
        #option 'username' '*' # Kasutajanimi kui operaator nõuab
        #option 'password' '*' # Salasõna

Käesolev E1750 pulk identifitseerib end esialgu kui virtuaalne USB-CDROM (vendid=0x12d1; prodid=1446).
Säärased 3G pulgad vajavad usb-modeswitch programmi mis käsib CDROMil end ümber lülitada modemiks.
OpenWRTs ei ole kaasa pandud udev reegleid modeswitchi täielikuks automatiseerimiseks nii nagu ta on lahendatud nt Ubuntus,
kus ports udev reegleid koos modeswitchi reeglitega on /usr all.
Selle modemi jaoks tuleb luua järgnev fail /etc/usb-modeswitch.conf sisse:

.. code:: bash

    DefaultVendor= 0x12d1
    DefaultProduct=0x1446
    TargetVendor=  0x12d1
    TargetProductList="1001,1406,140c,14ac"
    CheckSuccess=20
    MessageContent="55534243123456780000000000000011060000000000000000000000000000"

Kui pulk on ruuteris algkäivitamise ajal siis OpenWRT kutsub usb-modeswitch
programmi ise mingil hetkel välja aga kui seda ei juhtu siis tuleb seda käsitsi teha.
Ümberlülitumise õnnestumisel konkreetne modem tuvastab end kui Huawei E620 (vendid=0x12d1; prodid=0x1001).:

.. code:: bash

    usb_modeswitch

Kui modemi plokkseade (/dev/ttyUSB0) on nähtav, võib proovida ühenduse loomist.
Võrguseadistuste uuesti laadimiseks on kaks varianti:

.. code:: bash

    ifup wan # Liidese järgi
    /etc/init.d/network restart & # Kõik liidesed

Vigade tuvastamiseks on OpenWRTs järgnev käsk:

.. code:: bash

    logread

Modemi oleku informatsiooni lugemiseks on omaette plokkseade:

.. code:: bash

    root@OpenWrt:~# gcom -d /dev/ttyUSB2
    SIM ready
    Waiting for Registration..(120 sec max)
    Registered on Home network: "EE elisa",2
    Signal Quality::21

Viimane huvitav tähelepanek oli see et modem näitab
sinist tuld siis kui tal on 3-3.5G ühendus ning
rohelist siis kui on kättesaadav kõigest 2-2.5G leviala.
Sinise korral oli allalaadimiskiirus 2.2Mbit ringis ja ping 80-150ms.
Rohelise korral kukkus ta kuskil poole megabiti ja 500-600ms peale.

Kiiruseprobleemide korral võib veel mängida "usbserial" mooduli maxSize
parameetriga failis /etc/modules.d/60-usb-serial.
See peaks mõjuma ka "optional" moodulile:

.. code:: bash

    usbserial maxSize=4096

Juhul kui ruuterile pole võimalik tarkvara paigalduse ajal Internetti anda
võrgupesale, peab vajalikud failid eelnevalt alla sikutama ning
näiteks *scp* abil kopeerima:

.. code:: bash

    ROOT="http://downloads.openwrt.org/backfire/10.03.1/brcm47xx/packages"
    wget -c $ROOT/usb-modeswitch_1.1.8-1_brcm47xx.ipk
    wget -c $ROOT/usb-modeswitch-data_20110705-1_brcm47xx.ipk
    wget -c $ROOT/kmod-usb-core_2.6.32.27-1_brcm47xx.ipk
    wget -c $ROOT/kmod-usb-serial_2.6.32.27-1_brcm47xx.ipk 
    wget -c $ROOT/kmod-usb-serial-option_2.6.32.27-1_brcm47xx.ipk
    wget -c $ROOT/kmod-usb-uhci_2.6.32.27-1_brcm47xx.ipk
    wget -c $ROOT/kmod-usb2_2.6.32.27-1_brcm47xx.ipk
    wget -c $ROOT/comgt_0.32-9_brcm47xx.ipk
    wget -c $ROOT/usbutils_003-1_brcm47xx.ipk
    wget -c $ROOT/libusb_0.1.12-2_brcm47xx.ipk
    wget -c $ROOT/libusb-1.0_1.0.8-1_brcm47xx.ipk
    wget -c $ROOT/zlib_1.2.3-5_brcm47xx.ipk
    wget -c $ROOT/chat_2.4.4-16.1_brcm47xx.ipk
    wget -c $ROOT/kmod-nls-base_2.6.32.27-1_brcm47xx.ipk
    wget -c $ROOT/librt_0.9.30.1-43.32_brcm47xx.ipk  
    wget -c $ROOT/libpthread_0.9.30.1-43.32_brcm47xx.ipk
