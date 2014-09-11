This is yet another blog generator
==================================

It's inspired by Sphinx, Nikola and Pelican.

Dependencies:

.. code:: bash

    sudo apt-get install python3-jinja2 python3-pip
    sudo pip-3.2 install langid jinja2 docutils urllib2 pygal

I am not sure whether OCR A font used by Fritzing schematics is redistributable.
Directly linking CSS from Fritzing website often lags so you probably want to download those.
I think it is in Fritzing's best interests aswell if their schematics look the same everywhere.

.. code:: bash

    wget http://fritzing.org/static/fonts/ocr-a-tribute/ocr-a-tribute-bold.eot     -O fonts/ocr-a-tribute-bold.eot
    wget http://fritzing.org/static/fonts/ocr-a-tribute/ocr-a-tribute-bold.ttf     -O fonts/ocr-a-tribute-bold.ttf
    wget http://fritzing.org/static/fonts/ocr-a-tribute/ocr-a-tribute-bold.woff    -O fonts/ocr-a-tribute-bold.woff
    wget http://fritzing.org/static/fonts/ocr-a-tribute/ocr-a-tribute-light.eot    -O fonts/ocr-a-tribute-light.eot
    wget http://fritzing.org/static/fonts/ocr-a-tribute/ocr-a-tribute-light.ttf    -O fonts/ocr-a-tribute-light.ttf
    wget http://fritzing.org/static/fonts/ocr-a-tribute/ocr-a-tribute-light.woff   -O fonts/ocr-a-tribute-light.woff
    wget http://fritzing.org/static/fonts/ocr-a-tribute/ocr-a-tribute-regular.eot  -O fonts/ocr-a-tribute-regular.eot
    wget http://fritzing.org/static/fonts/ocr-a-tribute/ocr-a-tribute-regular.ttf  -O fonts/ocr-a-tribute-regular.ttf
    wget http://fritzing.org/static/fonts/ocr-a-tribute/ocr-a-tribute-regular.woff -O fonts/ocr-a-tribute-regular.woff

To serve on the spot:

.. code:: bash

    python3 blog.py -s

To build to output/:

.. code:: bash

    python3 blog.py
    
Features
========

* No more broken links!
* Keyword extraction and in-browser search
* Related posts via tags
* Referred content caching
* Broken URL checking
* Optimize and inline SVG images
* LaTeX formula in-browser rendering using MathJax
* Disqus commenting system
* Tag cloud generation
* Flexible templating system via Jinja2
* Fast serving mode
* Comprehensive build mode: detect broken links, cache embedded objects
* Fritzing schematic rendering

Directory structure
===================

css/ contains stylesheets
js/ contains JavaScript
templates/ contain .html files which are used as templates for posts/pages/etc
posts/ contain .rst files which are transformed into dated urls 
pages/ contain .rst files which maintain their filesystem hierarchy

