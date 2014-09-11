.. title: Convert Apple Lossless files to FLACs
.. date: 2013-05-03 16:32:02
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. tags: m4a, Apple Lossless, FLAC, avconv, FFMPEG

Convert Apple Lossless files to FLACs
=====================================

Quick shell snippet to convert those Apple Lossless files to FLACs:

.. code:: bash

    for filename in *.m4a; do
        avconv \
            -i "$filename" \
            -acodec flac \
            -compression_level 12 \
            "$(basename "$filename" ".m4a").flac";
    done


