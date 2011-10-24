# following PEP 386, versiontools will pick it up
__version__ = (0, 1, 1, "final", 0)


from html5video.encoders.ffmpeg import Encoder
from html5video.encoders.base import EncoderException, ImproperlyConfigured