.. title: Caching web traffic with Squid
.. date: 2010-06-27 16:40:37
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: caching, Squid, HTTP

Caching web traffic with Squid
==============================

While developing stuff on my PC, I noticed that some scripts download the same files multiple times. Same applies for my Estobuntu boxes which I want to keep up-to-date and at the moment software packages from APT repositories are downloaded at least twice. I figured out that I need caching proxy server for my LAN. Obvious place to install it was to my DD-WRT router with USB harddisk attached to it.

I tried several packages available in DD-WRT's optware:

* polipo - Worked great but the developer has no intentions to add support for intercepting/transparent proxy
* tinyproxy - Had some weird issues, couldn't get it even running

I ended up installing Squid:

.. code:: bash

    ipkg-opt install squid

Next I edited Squid's configuration file in /opt/etc/squid/squid.conf. The sample configuration file was HUGE, so I here are the most important lines:

.. code:: bash

    # Listen to requests from these IP addresses
    acl our_networks src 192.168.1.0/24
    http_access allow our_networks
     
    # Listen on this IP address/port and allow transparent proxying
    http_port 192.168.1.1:3128 transparent
    
    # Maximum file size, allow caching bigger files
    maximum_object_size 2048 MB
    
    # Run Squid process as this user
    cache_effective_user nobody
    
    # Run Squid process as this group
    cache_effective_group nobody
    
    # Set hostname, otherwise Squid refuses to start
    visible_hostname dd-wrt
    
    # Path where to store cache data (max 32768 megabytes)
    cache_dir ufs /opt/var/squid/cache 32768 16 256
    coredump_dir /opt/var/squid/cache

Next initialize cache in /opt/var/squid/cache:

.. code:: bash

    squid -z
    chown -R 65534:65534 /opt/var/squid/cache

I also created customized startup script in /opt/etc/init.d/squid:

.. code:: bash

    killall squid
    echo "Press Ctrl-C..."
    sleep 2
    
    if grep -q nobody /etc/passwd; then
        echo "User 'nobody' exists"
    else
        echo "Created user 'nobody'"
        echo "nobody:*:65534:65534:nobody:/var:/bin/false" >>
            /etc/passwd
    fi
    
    if grep -q nobody /etc/group; then
        echo "Group 'nobody' exists"
    else
        echo "Created group 'nobody'"
        echo "nobody:x:65534:" >>
            /etc/group
    fi
    
    # Start Squid
    /opt/etc/init.d/squid

Create custom firewall script for DD-WRT in /opt/etc/rc.firewall:

.. code:: bash

    iptables -t nat -A PREROUTING -p tcp 
        --dport 80 -j REDIRECT --to-port 3128

Enable execute bit and set nvram variable to point to this script:

.. code:: bash

    nvram set rc_firewall=/opt/etc/rc.firewall
    nvram commit
    chmod 755 /opt/etc/rc.firewall
    /opt/etc/rc.firewall

That's it, you can test it by either killing squid process, in this case none of the HTTP requests should go through or try downloading a file and then downloading it again. For example Linux source tarball was downloaded at 300-400kB/s the first time, any of the subsequential downloads were about 3-4MB/s.
