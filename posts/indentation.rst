.. title: Treppimine
.. tags: indentation, best practices, C, Java, coding conventions
.. date: 2014-03-03

Treppimine
==========

Sissejuhatus
------------

Treppimine (*indentation*) tähendab üldjuhul programmeerimiskeele
juhtimisstruktuuride nihutamist paremale teatud sammu võrra.

Treppimine programmeerimiskeeles C
----------------------------------

Võtame näiteks C-s kirjutatud funktsiooni *abs*, süntaktiliselt on korrektne
see ühele reale kirjutada:

.. code:: c

    int abs(a) { if (a < 0) { return -a; } else { return a; } };
    
Isegi kogenud programmeerijal on seda valus lugeda kuna pole täpselt aru
saada missugune koodijupp käima läheb kui *if* lause tõeseks osutub ja 
missugune siis kui see on väär.

`Java koodimistavad <http://www.oracle.com/technetwork/java/javase/documentation/codeconvtoc-136057.html>`_
näevad ette et trepitakse nelja tühiku kaupa:

.. code:: c

    int abs(a) {
        if (a < 0) {
            return -a;
        } else {
            return a;
        }
    }

Treppimine tekstiredaktorites
-----------------------------

Paljudes tekstiredaktorites saab ↹ ehk Tab ehk tabulaatori
nuppu kasutada koodi sisse treppimiseks, see tähendab paremale nihutamiseks.
Enamikes on ka seadistatud Shift-Tab mis trepib koodi väljapoole ehk nihutab vasakule.
Paljudes saab hiire või Shift-←	↑→↓ nuppude abil valida mitu rida ning
neid samaagselt Tab või Shift-Tab abil sisse-välja treppida.

Mõned tekstiredaktorid trepivad tabulaatori sümboli kaupa,
see tähdendab et nelja tühiku (' ') asemel on üks tabulaatori
sümbol ('\\t') mis lihtsalt võtab nelja sümboli jagu ruumi.

.. code::

    lauri@localhost ~ $ echo -en "\t1. tab\n" > spaghetti
    lauri@localhost ~ $ echo -en "    2. spaces\n" >> spaghetti
    
Tabulaatori laius ei ole defineeritud, käsureal on tabulaatori
laiuseks tavaliselt 8 sümbolit (*tab width 8*):

.. code::

    lauri@localhost ~ $ cat spaghetti
            1. tab
        2. spaces
    

Käsurea tööriistaga *expand* saab tabulaatorid asendada tühikutega:

.. code::

    lauri@localhost ~ $ expand -t 4 < spaghetti 
        1. tab
        2. spaces
