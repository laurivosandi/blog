.. title: Configuring Evolution for Gmail
.. date: 2011-10-30 18:55:59
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: IMAP, SMTP

Configuring Evolution for Gmail
===============================

There's many different guides for setting up Evolution for Gmail, but I haven't found a perfect one. So here goes yet another one.

Receiving mail with Evolution:

* Server type: IMAP+
* Server: imap.gmail.com
* Port: 993
* Username: first.last@gmail.com
* Use secure connection: SSL encryption
* Authentication type: Password

Sending mail:

* Server type: SMTP
* Server: smtp.gmail.com
* Port: 587
* Server requires authentication: yes
* Use secure connection: SSL encryption
* Authentication type: Login
* User Name: first.last@gmail.com
