.. title: Colourful command prompt
.. date: 2010-09-29 19:12:01
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: Gentoo, shell

Colourful command prompt
========================

Remember Gentoo and it's nice colourful command prompt? Append this to your users' ~/.bashrc. The locaton to put this code varies from distro to distribution tough.:

.. code:: bash

    if [[ ${EUID} == 0 ]] ; then
        PS1='[\033[01;31m]h [\033[01;34m]W $ [\033[00m]' 
    else
        PS1='[\033[01;32m]u@h [\033[01;34m]W $ [\033[00m]' 
    fi


