.. title: GNU/Linux based terminal-servers with SmartCard support
.. date: 2010-12-01 20:37:40
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: ID-card, PCSC-Lite, pcscd, opensc-tool, OpenSC, SmartCard, PKCS#11, LTSP

GNU/Linux based terminal-servers with SmartCard support
=======================================================

.. image: http://www.id.ee/public/idlugeja.jpg

`Our company <http://www.povi.ee>`_  has been dealing with GNU/Linux based terminal-servers for a while and in Estonia you run into issues with ID-card at some point. Estonian ID-card is a SmartCard which is used to authenticate person online and to give **legally valid signature**. With terminal-server systems issues arose immediately because PCSC-lite originally didn't support any network transparency. With few hacks it is possible to do this and that's what this post is about.

PCSC-lite is a SmartCard framework which allows multiple applications to use multiple cards. Applications use a UNIX domain socket to talk to the process which handles the cards. There also used to be a public shared memory file which was a complete showstopper for LTSP, but after poking the core developer Ludovic `it was finally removed <http://archives.neohapsis.com/archives/dev/muscle/2009-q4/0016.html>`_ . In `revision 5373 <http://lists.alioth.debian.org/pipermail/pcsclite-cvs-commit/2010-November/004926.html>`_  another important feature for LTSP was implemented, the user can also specify the path to the forementioned UNIX domain socket.

So obviously what you need to do is to run the daemon in the terminal, redirect the UNIX domain socket to the server and tell the application to use that custom path. With version 5 LTSP switched from unencrypted connections to OpenSSH which encapsulates X11 traffic and any other connections between server and terminal. OpenSSH does support redirecting TCP/IP sockets but not UNIX domain sockets altough required code changes are minor.

There was a project called `streamlocal <http://www.25thandclement.com/~william/projects/streamlocal.html>`_ , which was basically a bunch of patches for OpenSSH 4.4p1 to allow UNIX domain socket redirecting, I updated the patch and made it available for OpenSSH 4.7p1. After that there were some major rewrites in the OpenSSH core so I didn't bother porting and I started from scratch to have the bare minimum to make ID-card work. This resulted in hackish `rewrites for OpenSSH 5.3p1 and 5.5p1 <http://lauri.vosandi.eu/hg/ltsp-esteid/openssh/>`_ .

LTSP5 uses LDM in the terminal to authenticate SSH connection after which it passes X11 session to the desktop session application on the remote machine. To enable the socket redirection I also needed to modify LDM to inject parameters to SSH client process. This patch is obsolete since LDM now officially reads environment variable LDM_SSHOPTIONS for exactly the same purpose.

There are packages available for Ubuntu 8.04 and Ubuntu 10.04. National Library of Estonia is using them to power their server and 50 VxL terminals. There's a `manual written in Estonian <http://lauri.povi.ee/wiki/?page=lucid-ltsp-esteid>`_ , you can try your `luck with Google Translate <http://translate.google.com/translate?js=n&amp;prev=_t&amp;hl=et&amp;ie=UTF-8&amp;layout=2&amp;eotf=1&amp;sl=et&amp;tl=en&amp;u=http%3A%2F%2Flauri.povi.ee%2Fwiki%2F%3Fpage%3Dlucid-ltsp-esteid>`_ . There was an `article about our solution <http://www.am.ee/node/1748>`_  in Arvutimaailm, again you can try your `luck with Google Translate <http://translate.google.com/translate?hl=et&amp;sl=et&amp;tl=en&amp;u=http%3A%2F%2Fwww.am.ee%2Fnode%2F1748>`_ .

PS: OpenSSH is reference implementation of the SSH protocol so incorporation of UNIX domain patches needs protocol standard change first. This could be pushed through Internet Task Engineering Force, so if anyone is willing to lobby them please let me know :)
