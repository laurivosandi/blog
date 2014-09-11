.. title: Estobuntu Lucid Lynx LTSP
.. date: 2010-05-19 18:57:40
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: Estobuntu, Ubuntu, LTSP, ID-card

Estobuntu Lucid Lynx LTSP
=========================

Currently Estobuntu team is working hard to get ready with next release based on Kubuntu Lucid Lynx (10.04). My part is to make LTSP work with this release. Biggest issue with Estobuntu LTSP is ID-card, because it needs some hackish changes to make ID-card work in terminal-server environment.

I have prepared APT repository, so adding "deb http://v6sa.itcollege.ee estobuntu-ltsp lucid" to your server's /etc/apt/sources.list will suffice. Here's what we did: Patch LDM to allow passing extra parameters to the SSH session started from terminal; Patch OpenSSH so it would be possible to redirect UNIX domain sockets; Patch PCSCLite 1.5.6 so it would be possible to relocate it's communication socket.

If you're into this whole SmartCard business then you know that PCSCLite is pretty much server-client architecture based software so multiple applications could use one SmartCard at the same time. Current implementation limits server-client possibilities to one computer tough. We tweaked it a bit so now this communications socket gets redirected from terminal to user's home directory at LTSP server via SSH tunneling.

Currently National  Library of Estonia is already using the packages I prepared for previous  Long-Term Support version of Ubuntu codenamed Hardy Heron (8.04). They  are running around 50 terminals connected to one powerful server. Thanks  to us it is possible to use ID-cards on terminals to log in to e-banks  and so forth.

Right now only i386 architecture is supported. I encountered some really weird issues with amd64 port. PCSCLite segfaults with getenv() calls in SHMClientSetupSession (src/winscard_msg.c). If anyone could ellaborate on this I would be very thankful. Until then I'll try out PCSCLite 1.6.0 which was just released two weeks ago.

UPDATE: PCSCLite 1.6.0 seems to suffer the same issue
