Installation
====================

The easiest way to install html5video is with pip_:

    pip install html5video

``easy_install html5video`` can also be used or the code can be downloaded from
GitHub_. After installing you will need to install FFMPEG or make sure you have
a recent version. Currently only FFMPEG version ``0.8.0`` and above are
supported.

Installing FFMPEG
-----------------

Unfortunately most repository versions of FFMPEG are not recent enough and don't
support all the formats and codecs required for HTML5 video. FFMPEG offers a
good set of instructions to compile your own in the _website. However, following
is a summary of a few different platforms.

Ubuntu
~~~~~~~~~

The easiest way to install FFMPEG on ubuntu is to use an existing PPA.
`This PPA` provided by a community member provides ffmpeg version greater than
``0.8.0``. If you want to use it, follow these steps:

1. Run ``sudo add-apt-repository ppa:jon-severinsson/ffmpeg``

2. Add the following lines to your /etc/apt/sources.list::

    deb http://ppa.launchpad.net/jon-severinsson/ffmpeg/ubuntu YOUR_UBUNTU_VERSION_HERE main
    deb-src http://ppa.launchpad.net/jon-severinsson/ffmpeg/ubuntu YOUR_UBUNTU_VERSION_HERE main

3. Finally ``sudo apt-get update`` and ``sudo apt-get install ffmpeg``

OS X
~~~~~~~~~

At the time of writing, homebrew has a formula for version 0.8.5 that after
installing homebrew can be installed with:

    brew install ffmpeg

Compile Your own
~~~~~~~~~~~~~~~~

Compiling your own version of FFMPEG is straight forward. After downloading a
tar ball from the `ffmpeg website`_. Extract it and follow the steps included in
the ``INSTALL`` file.

.. _pip: http://pip.openplans.org/
.. _GitHub: https://github.com/d0ugal/html5video
.. _ffmpeg website: http://ffmpeg.org/download.html
.. _This PPA: https://launchpad.net/~jon-severinsson/+archive/ffmpeg