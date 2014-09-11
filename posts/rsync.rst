.. title: Backing up files with rsync
.. date: 2010-06-27 10:08:43
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: rsync, backup, DD-WRT

Backing up files with rsync
===========================

I wanted to keep a backup of my NAS contents. It's a router running DD-WRT with USB harddisk attached to it, serving files via SAMBA. After digging around on the internet, I figured out that I should use rsync to do the job. It provides way to transfer differential data so I don't need to wait for 50 gigabytes of photos to get copied during every backup session. By default it uses SSH to transfer data, but it also has it's own rsync:// protocol which isn't encrypting the data. Since router isn't very powerful, it makes sense to disable encryption and compression.

Source machine
--------------


On the DD-WRT box I already had set up `optware <http://www.dd-wrt.com/wiki/index.php/Optware>`_ , so only thing I had to do was:

.. code:: bash

    ipkg-opt install rsync

And to create configuration file for rsync in /opt/etc/rsyncd.conf:

.. code:: bash

    uid = nobody
    gid = nobody
    use chroot = yes
    max connections = 5
    syslog facility = local3
    pid file = /var/run/rsyncd.pid
    secrets file = /opt/etc/rsyncd.secrets
    socket options = SO_SNDBUF=65536,SO_RCVBUF=65536
    
    [photos]
    path = /mnt/Photos
    comment = Photos
    read only = yes
    hosts allow = 192.168.1.2

This configuration serves files from /mnt/Photos under share name "photos", allows only connections from IP 192.168.1.2 that's my desktop. For improved security the process switches to user and group "nobody" and chroots into the target folder. To start the daemon I just issued:

.. code:: bash

    rsync --daemon

Target machine
--------------

On the Ubuntu desktop machine I just downloaded rsync via APT:

.. code:: bash

    sudo apt-get install rsync

Finally I ran following command to download changes from the router and keep /mnt/backup/Photos synchronized with the contents on the router:

.. code:: bash

    rsync --verbose  --progress --stats \
        --size-only --times --recursive --perms \
        --links --delete --exclude "*~" \
        192.168.1.1::photos mnt/backup/Photos

Alternatively you can use gtkrsync or grsync to do the same job with GUI application
