.. title: Firefly Media Server and Banshee
.. date: 2011-10-30 21:18:32
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: DAAP, DLNA, uPNP

Firefly Media Server and Banshee
================================

If you have more than 10k audio tracks on your NAS box, reading all the metadata is rather slow via Samba or NFS. There are various ways to access multimedia over LAN, DLNA/UPnP is good enough for videos, `Digital Audio Access Protocol <http://wikipedia.org/wiki/Digital_Audio_Access_Protocol>`_  is better for audio. DAAP originates from Apple's iTunes, it is based on HTTP and most of the Free Software implementations are actually reverse engineered, because Apple hasn't exactly provided proper documentation if I am not mistaken.

There are various DAAP servers besides iTunes itself, the most used one seems to be mt-daapd. The author of mt-daapd has abandoned the project and there's a bunch of forks on the web: `Firefly Media Server <http://wikipedia.org/wiki/Firefly_Media_Server>`_ , the more up-to-date `forked-daapd <https://github.com/jasonmc/forked-daapd>`_  and probably others.

DD-WRT's Optware repository contains mt-daapd and mt-daapd-svn packages, first one seems to be pretty much obsolete version, the second one seems to carry Firefly Media Server branding. That's also the package I got working on my router. The configuration for those of you who are interested sits in at /opt/etc/mt-daapd/mt-daapd.conf:

.. code:: bash

    [general]
    web_root = /opt/share/mt-daapd/admin-root
    port = 3689
    admin_pw = mt-daapd
    db_type = sqlite3
    db_parms = /mnt/disc0-part1/.mt-daapd
    mp3_dir = /mnt/disc0-part1/Muusika
    servername = Firefly on rt-n16
    runas = nobody
    extensions = .mp3,.m4a,.m4p,.flac,.ogg
    logfile = /mnt/disc0-part1/.mt-daapd/mt-daapd.log
    rescan_interval = 0
    always_scan = 0
    scan_type = 0
    compress = 0
    
    [plugins]
    # Banshee fails to play transcoded FLAC stream so I disabled
    # ssc-ffmpeg.so and ssc-script.so plugins by deleting them
    plugin_dir = /opt/lib/mt-daapd/plugins
    
    [scanning]
    process_playlists = 0
    process_itunes = 0
    process_m3u = 0
 
Once started Firefly Media Server scans the music directory for audio files, stores meta-information and afterwards starts listening on port 3689, that's also the standard port for DAAP. You can fire up a browser and see how it's doing, the login in this case is admin and mt-daapd. The web interface seems to be the "right" place to shut down the media server because the process is not properly handling SIGTERM or SIGKILL, you can also reinitiate the scan from the web interface.

Now once Firefly is up and running, you can connect to it using iTunes, but being an open-source zealot, I don't have much Apple gear lying around! On Ubuntu you can try out Rhythmbox, and it's buggy bro Banshee. Banshee is written in C# and those guys have written some funky code that exposes it's local cache and what not on http://localhost:8089. Note that Firefly by default transcodes FLAC and OGG to uncompressed WAV, but Banshee doesn't play with that well.

For all the hackers out there: having a HTML5 based player interface in Firefly would be a bliss!
