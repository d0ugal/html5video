Usage
====================

Command Line
--------------------

The following example shows the simplest usage of html5video::

    html5video /path/to/source/file -o /output/directory

This will convert the input file into the different formats required to
reliably serve HTML5 video. These are MPEG 4, Ogg (Theora video and Vorbis audio
in an Ogg container) and WebM.

Calling the API
--------------------

The simplest usage of the API is as follows::

    from html5video import Encoder
    video_encoder = Encoder('path/to/source/file', '/output/directory')

    files_list = video_encoder.all_html5()

This will create, save and return handles for each of the formats required for
HTML5 video. If you need to be more specific or only need a specific format
these can be achived like so::

    mp4_file = video_encoder.to_mp4()
    webm_file = video_encoder.to_webm()
    ogg_file = video_encoder.to_ogg()


Video Markup
----------

Once you have saved these files, the following markup can be used to display
the videos on a web page with a flash fallback for older browsers.::

    <video id="movie" width="320" height="240" preload controls>
      <source src="pr6.webm" type='video/webm; codecs="vp8, vorbis"' />
      <source src="pr6.ogv" type='video/ogg; codecs="theora, vorbis"' />
      <source src="pr6.mp4" />
      <object width="320" height="240" type="application/x-shockwave-flash"
        data="flowplayer-3.2.1.swf">
        <param name="movie" value="flowplayer-3.2.1.swf" />
        <param name="allowfullscreen" value="true" />
        <param name="flashvars" value='config={"clip": {"url": "http://wearehugh.com/dih5/pr6.mp4", "autoPlay":false, "autoBuffering":true}}' />
        <p>Download video as <a href="pr6.mp4">MP4</a>, <a href="pr6.webm">WebM</a>, or <a href="pr6.ogv">Ogg</a>.</p>
      </object>
    </video>
    <script>
      var v = document.getElementById("movie");
      v.onclick = function() {
        if (v.paused) {
          v.play();
        } else {
          v.pause();
        }
      };
    </script>