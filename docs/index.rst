Welcome to html5video!
====================

Converts a source video file into the multiple video container and codecs
required to support HTML5's ``<video>`` tag.

.. toctree::
   :maxdepth: 2

   installation
   usage


Quick Start
==================

1. Install FFMPEG version 0.8 or above.
2. ``pip install html5video`` or ``easy_install html5video``.
3. Run the command ``html5video /path/to/source_video``


Justification
=============
Why another wrapper around a video encoder? Reading and digesting all the
different requirements for HTML5 video is a tedious task. With html5video you
can rely on a sensible set of defaults that can be tweaks and are kept up to
date over time.


Requirements
============

html5video requires the following modules. If you use pip_, you can install
the necessary packages via the included ``requirements.txt``. If you installed
html5video with pip_ you will already have the required packages.

Required
--------

* Unipath 0.2.1

Development Requirements
-------------------------

To work on html5video itself, the following requirements are recommended for
running the full test suite and building the documentation.

* coverage
* mock
* nose
* sphinx
* unittest2
* versiontools


Planned/Requested Features
================

* Support for Django/Jinja2 template langugaes to output the <video> tag.
* Support for more versions of FFMPEG
* Support for further customisation and control over the video output


Contributions
==============

Bug reports, patches and pull requests are welcome. The code and management of
the project is happening on GitHub_



.. _pip: http://pip.openplans.org/
.. _GitHub: https://github.com/d0ugal/html5video