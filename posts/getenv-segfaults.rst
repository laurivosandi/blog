.. title: Segmentation faults with getenv under amd64
.. date: 2010-06-05 16:07:45
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: C, PCSC-Lite, pcscd

Segmentation faults with getenv under amd64
===========================================

This is a follow up to `my previous <http://v6sa.wordpress.com/2010/05/19/estobuntu-lucid-lynx-ltsp/>`_  post.

So the thing is that we needed to adjust PCSC-Lite source tree so it would be
possible to specify it's IPC socket path manually. It usually resides at
/var/run/pcscd/pcscd.comm, but in LTSP system it gets redirected to ~/.pcscd.comm at server.

I used getenv("PCSCLITE_CSOCK_NAME") to read customised IPC socket path.
The weird thing was that everything worked perfectly under i386.
Once I ran the same code on amd64 I got segfaults. I digged for many hours and
finally I figured out that #include <stdlib.h> was missing.
I was rather surprised that on amd64 it failed like this.
Anyways hint for any amateur C programmers - check your includes twice!
