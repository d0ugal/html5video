Welcome to html5video!
====================

Converts a source video file into the multiple video container and codecs
required to support HTML5's ``<video>`` tag


Usage Example
==============

From the command line::

    html5video /path/to/source/file -o /output/directory

In your code::

    from html5video import Encoder
    video_encoder = Encoder('path/to/source/file', '/output/directory')

    files_list = video_encoder.all_html5()


`Read more on Read The Docs <http://html5video.readthedocs.org/>`
