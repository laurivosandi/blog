.. title: Audio codecs
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags:  MP3, sampling rate, bitrate
.. flags: hidden
.. date: 2013-07-15

Introduction
--------------

I bet everybody's familiar with MP3, but how does it work?
First let's start off with sounds in general.
A human being is capable of hearing frequencies between approximately 30Hz and 20000Hz.
Any sound is actually composed of different *frequencies* of varying *amplitude* and duration.

For a computer this information needs to be *quantified*,
that means making the information measurable and countable.
The most common way to do that is to *sample* audio, that roughly means
measuring the speaker cone displacement several thousand times per second.
The speaker cone offset and time when it was measured form the basic unit
of *audio* *sample*. The concept is somewhat similar to pixel, the basic unit
of digital image consists of pixel location on the screen and the color of it.

Sampling rate
-------------

The speed of taking those samples is called *sampling* *rate*.
Samples per second is usually noted with the frequency unit Hertz (Hz).
A `fancy theorem <http://en.wikipedia.org/wiki/Nyquist%E2%80%93Shannon_sampling_theorem>`_
says that sampling frequency is supposed to be at least twice the frequency 
it wishes to reproduce, that is twice the 20000Hz human is able to hear.
Sony and Philips, the creators of the now-obsolete Audio CD agreed that
frequency should be 44100Hz.

Sampling precision
------------------

The second metric of *sampling* is the precision of the samples,
that means how accurately the speaker cone displacement is measured.
Audio CD-s use 16-bit numbers to describe the position of each speaker.
A 16-bit integer means that there are two to the power of 16 possible
values for such number. That means 65536 different positions for the 
speaker cone.
Usually audio CD-s are in stereo, which means that there are two channels,
one for left speaker and one for right.

Bitrate
-------

One of the most important metrics of audio data is the bitrate, 
how many bits is required to represent one second of audio.
Knowing that audio is sampled 44100 times per second for both channels
with 16-bit precision, we can calculate the it easily:

.. math::

    44100 \frac{samples}{sec} \times 2ch \times 16 \frac{bits}{ch} = 1411200\ bps \approx 1378 kbps
    
That is roughly 172 kilobytes per second. So for a regular 3 minute track
this yields:

.. math::

    3 \times 60 \frac{sec}{min} \times 1411200 = 254016000 bits \approx 30MB
    
The capacity of an audio CD
---------------------------

The goal of engineers who designed audio CD was to make it possible for an
audio CD to contain Beethoven's Ninth Symphony performed by
London Philharmonic Orchestra.
That means rougly 80 minutes of audio data.
Following the points presented above, we can easily calculate the 
minimum data capacity for such disc:

.. math::

    80 min \times 60 \frac{sec}{min} \times 44100 \frac{samples}{sec} \times 2ch \times 16 \frac{bits}{ch}
    
That results in:

.. math::

    6773760000\ bits = 846720000\ bytes \approx 800MB
    
Which is incidently the size of an average user writable CD-R disc.

MP3
---

MP3 (MPEG-1 or MPEG-2 Audio Layer III) is one of the most commonly used algorithms to
decrease disk usage. The format is encumbered by various patents and many companies
claim that in order to sell products incorporating MP3 technology one needs to license
the technology from them, although in countries except US the patents have already
expired and the algoritm is in public domain.


    
* `Sampling <http://en.wikipedia.org/wiki/Sampling_(signal_processing)>`_
* `Compact disc <http://en.wikipedia.org/wiki/Compact_Disc>`_
* `Audio bit depth <http://en.wikipedia.org/wiki/Audio_bit_depth>`_
* `MP3 <http://en.wikipedia.org/wiki/MP3>`_

