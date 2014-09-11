.. title: Resetting OpenSSH server keys
.. date: 2014-04-12
.. tags: OpenSSH, Heartbleed, OpenSSL, security, privacy

Resetting OpenSSH server keys
=============================

Introduction
------------

The `Heartbleed <https://xkcd.com/1354/>`_ vulnerability that was published couple of days ago
has knocked off feet many sysadmins.
There is still a lot of fuss around what are the implications of this vulnerability issue.
The major issue is that it allows reading memory of the server process.
In case of web servers this means attacker could steal your SSL private key.
Most probaly there have been efforts to pull web server private keys of random machines so
replacing the keys might be a good idea.

This bug however should NOT affect OpenSSH servers because SSH is pretty much protocol of it's own.
But if you're paranoid or you think your keys have been compromised by some other means then you might find this howto useful.
Resetting OpenSSH server keys is pretty simple if you know how public/private key cryptography works.

OpenSSH server
--------------

You may start off by deleting the keys you have on your SSH server:

.. code:: bash

    rm /etc/ssh/sshd_host_*

You might want to disable DSA and RSA key based authentication and use ECDSA instead.
Altough this requires your SSH client to be up to date, since old OpenSSH clients do
not have ECDSA support. Note that ECDSA is significantly slower than RSA, 
so if 2-3 second login bothers you, you still might want to stick to RSA.
I have disabled RSA and DSA in /etc/ssh/sshd_config:

.. code::

    #HostKey /etc/ssh/ssh_host_rsa_key
    #HostKey /etc/ssh/ssh_host_dsa_key
    HostKey /etc/ssh/ssh_host_ecdsa_key

If you're on Debian you may regenerate SSH keys simply by:

.. code:: bash

    sudo dpkg-reconfigure openssh-server

You can get the certificate fingerprint with *ssh-keygen* utility,
so everyone who wants to connect to this particular SSH server can verify
whether the remote endpoint is actually who it claims to be:
         
.. code::
         
    nas.koodur.com lauri # ssh-keygen -l -f /etc/ssh/ssh_host_ecdsa_key
    256 bd:08:1e:e1:cf:78:3d:89:81:21:ae:4c:90:09:50:e3  root@nas (ECDSA)
    
OpenSSH client
--------------
    
Now if you try to log into your SSH server you'll be greeted with
the well known man-in-the-middle attack warning saying that SSH server
certificate has changed and it is not the one used to log in last time:

.. code::

    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    @    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
    Someone could be eavesdropping on you right now (man-in-the-middle attack)!
    It is also possible that a host key has just been changed.
    The fingerprint for the ECDSA key sent by the remote host is
    bd:08:1e:e1:cf:78:3d:89:81:21:ae:4c:90:09:50:e3.
    Please contact your system administrator.
    Add correct host key in /home/lauri/.ssh/known_hosts to get rid of this message.
    Offending ECDSA key in /home/lauri/.ssh/known_hosts:2
      remove with: ssh-keygen -f "/home/lauri/.ssh/known_hosts" -R nas.koodur.com
    ECDSA host key for nas.koodur.com has changed and you have requested strict checking.
    Host key verification failed.

You can purge the fingerprint from your SSH client's *known_hosts* file by:

.. code::

    lauri@hypercubie ~ $ ssh-keygen -f ~/.ssh/known_hosts -R nas.koodur.com
    # Host nas.koodur.com found: line 2 type ECDSA
    /home/lauri/.ssh/known_hosts updated.
    Original contents retained as /home/lauri/.ssh/known_hosts.old

OpenSSH also stores certififcate for the IP address, so you might have to purge that aswell:

.. code::

    lauri@hypercubie ~ $ ssh-keygen -f ~/.ssh/known_hosts -R 213.168.13.40
    # Host 213.168.13.40 found: line 21 type ECDSA
    /home/lauri/.ssh/known_hosts updated.
    Original contents retained as /home/lauri/.ssh/known_hosts.old
    
Now once you try to connect to the SSH server again make sure the fingerprint is the one presented previously:

.. code::

    lauri@hypercubie ~ $ ssh nas.koodur.com
    The authenticity of host 'nas.koodur.com (213.168.13.40)' can't be established.
    ECDSA key fingerprint is bd:08:1e:e1:cf:78:3d:89:81:21:ae:4c:90:09:50:e3.
    Are you sure you want to continue connecting (yes/no)? yes

