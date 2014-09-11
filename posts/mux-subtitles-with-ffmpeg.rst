.. title: Merge subtitles
.. date: 2013-06-02
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: FFMPEG, avconv

Merge subtitles
===============

Quick snippet for muxing subtitles into Matroska container:

.. code:: bash

    avconv \
        -i path-to-video-file.mp4 \
        -f srt -i path-to-subtitles.srt \
        -map 0:0 \
        -map 0:1 \
        -map 1:0 \
        -acodec copy \
        -vcodec copy \
        -scodec copy \
        merged-output-file.mkv
