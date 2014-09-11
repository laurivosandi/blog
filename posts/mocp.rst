.. title: Music On Console
.. date: 2010-12-28 20:44:57
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: shell, FFMPEG, MP3, FLAC, OGG Vorbis

Music On Console
================

Music On Console Player or mocp for short is awesome piece of software for command line geeks. It is somewhat similar to Midnight Commander - on the left panel you can browse through your filesystem and on the right there is your current playlist.

To install on a Debian or Ubuntu box:

.. code:: bash

    apt-get install moc moc-ffmpeg-plugin

Start it up with mocp command. Note that some Qt guys had another program called moc!:

.. code:: bash

    mocp

Now the most important part - key bindings! Let's start with the global ones.

* q - Exit the user interface but keep player running in the background
* Q - Exit the whole program and stop any playing audio tracks
* R - Toggle repeating the playlist
* S - Toggle shuffling
* tab - Switch between panels

Now the keys you can use on the left panel for browsing the files:

* a - Add files/directories to the playlist
* A - Add playlist to current playlist
* Enter - Enter directory or add file

And finally the keys you can use on the playlist

* d - Remove track from playlist
* C - Clear the whole playlist
* Enter - Start playing a track
* Control-f - Toggle track format visibility
* Control-t - Toggle track duration visibility

Note that shortcuts in capital letters mean the button pressed with Shift. Happy hacking :)
