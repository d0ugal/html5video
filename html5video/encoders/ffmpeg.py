from subprocess import Popen, PIPE
from re import findall, search
from unipath import Path

from html5video.encoders.base import (BaseEncoder, EncoderException,
                                    ImproperlyConfigured)


class FfmpegException(EncoderException):
    pass


class Encoder(BaseEncoder):

    quality_flag = '-b'
    group_flag = '-g'
    dimensions_flag = '-s'

    def __init__(self, input_file, output_file=None, binary='ffmpeg'):
        super(Encoder, self).__init__(input_file, output_file, binary)
        self.quality = '1500k'

        version = self.version()
        if version < (0, 8, 0):
            version_string = '.'.join(str(s) for s in version)
            msg = "The binary '{binary}' is version {version}. FFMPEG version 0.8 \
or above is required. Run the command 'ffmpeg -version' for more detals\
".format(binary=binary, version=version_string)
            raise ImproperlyConfigured(msg)

    def call(self, command):
        r = Popen(command, stdout=PIPE, stderr=PIPE)
        exc_stdout, exc_stderr = stdout, stderr = r.communicate()

        if exc_stdout:
            try:
                exc_stdout = exc_stdout.split('\n\n')[1]
            except IndexError:
                exc_stdout = exc_stdout

        if exc_stderr:
            try:
                exc_stderr = exc_stderr.split('\n\n')[1]
            except IndexError:
                exc_stderr = exc_stderr

        if r.returncode != 0:
            msg = """FFMPEG returned a non-zero return code of {returncode}
    COMMAND
{command}

    STDOUT:
{exc_stdout}

    STDERR:
{exc_stderr}
""".format(command=' '.join(command), returncode=r.returncode,
            exc_stdout=exc_stdout, exc_stderr=exc_stderr)
            raise FfmpegException(msg)

        return stdout, stderr

    def version(self):
        try:
            stdout, stderr = self.call([self.binary, '-version'])
        except OSError as e:
            raise ImproperlyConfigured("Uable to call FFMPEG. %s" % e)

        patterns = (
            'ffmpeg\sversion\s([\d\.]+)',
            'FFmpeg\sversion\sSVN-r([\d\.]+)'
        )

        for pattern in patterns:
            result = search(pattern, stderr)
            if result:
                version = result.group(1)
                return tuple([int(part) for part in version.split('.')])

        raise ImproperlyConfigured("Unable to get FFMPEG version string.")

    def version_info(self):
        command = [self.binary, '-version', '-formats', '-codecs']
        return self.call(command)

    def enabled_features(self):

        if hasattr(self, '_enabled_features'):
            return self._enabled_features

        r = self.version_info()
        print r, r.__class__
        stdout, stderr = r
        self._enabled_features = findall('--enable-([\w-]+)', stderr)

        return self._enabled_features

    def validate_configuration(self):

        webm_requirements = ['libvorbis', 'libvpx']

        for i in webm_requirements:
            if i not in self.enabled_features():
                config_msg = "ffmpeg version 0.6 or later is required for WebM"\
                    "support. Run ffmpeg with no parameters and look for "\
                    "'--enable-{feature}'".format(feature=i)

                raise ImproperlyConfigured(config_msg)

        return True

    def get_mp4_output_path(self):
        return self.get_output_path('mp4')

    def get_ogv_output_path(self):
        return self.get_output_path('ogv')

    def get_webm_output_path(self):
        return self.get_output_path('webm')

    @property
    def vorbis(self):
        return ['-acodec', 'libvorbis', '-ab', '160000']

    def mp4_args(self, output_path=None):
        if not output_path:
            output_path = self.get_mp4_output_path()
        mp4_args = []
        return self.build_args(mp4_args, output_path)

    def webm_args(self, output_path=None):
        if not output_path:
            output_path = self.get_webm_output_path()
        webm_args = ['-vcodec', 'libvpx',  '-f', 'webm'] + self.vorbis
        return self.build_args(webm_args, output_path)

    def ogv_args(self, output_path=None):
        if not output_path:
            output_path = self.get_ogv_output_path()
        ogv_args = ['-vcodec', 'libtheora', ] + self.vorbis
        return self.build_args(ogv_args, output_path)

    def build_args(self, format_specific, output_path):
        base_args = super(Encoder, self).build_args()
        general_args = base_args + ['-y', '-i', self.input_file]
        return general_args + format_specific + [output_path, ]

    def as_mp4(self):
        output_path = self.get_mp4_output_path()
        self.call(self.mp4_args(output_path))
        return output_path

    def as_ogv(self):
        output_path = self.get_ogv_output_path()
        self.call(self.ogv_args(output_path))
        return output_path

    def as_webm(self):
        output_path = self.get_webm_output_path()
        self.call(self.webm_args(output_path))
        return output_path

    def all_html5(self, mp4=True, webm=True, ogv=True):

        if not Path(self.input_file).exists():
            raise ImproperlyConfigured("Input file '%s' does not exist" % self.input_file)

        command_list = []
        if mp4:
            command_list.append(self.mp4_args())
        if webm:
            command_list.append(self.webm_args())
        if ogv:
            command_list.append(self.ogv_args())

        return [self.call(command) for command in command_list]
