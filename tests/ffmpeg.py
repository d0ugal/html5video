from mock import patch
from unittest2 import TestCase


class FfmpegTestCase(TestCase):

    def _get_fixture_path(self, name):
        from unipath import Path
        d = Path(__file__).parent
        return d.child("fixtures", name)

    def _load_output(self, name):
        f = open(self._get_fixture_path(name))
        return '\n'.join(f.readlines())

    def test_ffmpeg_installed(self):

        from html5video import Encoder, ImproperlyConfigured

        with self.assertRaises(ImproperlyConfigured):
            Encoder("", binary="fake_binary_path")

    def test_version(self):

        from html5video import Encoder, ImproperlyConfigured

        ffmpeg = Encoder("fake_file.something")

        self.assertEquals(ffmpeg.version(), (0, 8, 4), )

        with patch.object(Encoder, 'version', lambda s: (0, 7, 3)):

            with self.assertRaises(ImproperlyConfigured):
                ffmpeg = Encoder("fake_file.something")

    def test_missing_source(self):

        from html5video import Encoder, ImproperlyConfigured

        ffmpeg = Encoder("my_video.something")
        with self.assertRaises(ImproperlyConfigured):
            ffmpeg.all_html5()

        ffmpeg = Encoder("my_video.something", "my_output")

    def test_full_encode(self):

        from html5video import Encoder

        video_path = self._get_fixture_path('test_video.mov')
        ffmpeg = Encoder(video_path)
        ffmpeg.all_html5()

    def test_mp4_encode(self):

        from html5video import Encoder

        video_path = self._get_fixture_path('test_video.mov')
        expected_path = video_path.replace('.mov', '.mp4')
        ffmpeg = Encoder(video_path)
        result_path = ffmpeg.as_mp4()
        self.assertEquals(expected_path, result_path)

    def test_webm_encode(self):

        from html5video import Encoder

        video_path = self._get_fixture_path('test_video.mov')
        expected_path = video_path.replace('.mov', '.webm')
        ffmpeg = Encoder(video_path)
        result_path = ffmpeg.as_webm()
        self.assertEquals(expected_path, result_path)

    def test_ogv_encode(self):

        from html5video import Encoder

        video_path = self._get_fixture_path('test_video.mov')
        expected_path = video_path.replace('.mov', '.ogv')
        ffmpeg = Encoder(video_path)
        result_path = ffmpeg.as_ogv()
        self.assertEquals(expected_path, result_path)

    def test_unable_to_detect_version(self):

        from html5video import Encoder, ImproperlyConfigured

        with patch.object(Encoder, 'call', lambda a, b: ("", "")):
            with self.assertRaises(ImproperlyConfigured):
                Encoder("dummy_file")

    def test_feature_detection_failed(self):

        bad_output = self._load_output('bad_ffmpeg_version_info.txt')

        expected = ['avfilter', 'avfilter-lavf', 'vdpau', 'bzlib', 'libgsm',
        'libschroedinger', 'libspeex', 'libtheora', 'libvorbis', 'pthreads',
        'zlib', 'runtime-cpudetect', 'gpl', 'postproc', 'swscale', 'x11grab',
        'libdc1394', 'shared', ]

        from html5video import Encoder, ImproperlyConfigured

        with patch.object(Encoder, 'call', lambda a, b: (bad_output, bad_output)):
            with patch.object(Encoder, 'version', lambda a: (0, 8, 0)):

                e = Encoder('dummy_file')
                features = e.enabled_features()
                self.assertEquals(features, expected)
                with self.assertRaises(ImproperlyConfigured):
                    e.validate_configuration()

    def test_feature_detection_passed(self):

        from html5video import Encoder

        good_output = self._load_output('good_ffmpeg_version_info.txt')

        with patch.object(Encoder, 'call', lambda a, b: (good_output, good_output)):
            with patch.object(Encoder, 'version', lambda a: (0, 8, 0)):
                e = Encoder('dummy_file')
                e.enabled_features()
                self.assertTrue(e.validate_configuration())

        e = Encoder('dummy_file')
        e.enabled_features()
        self.assertTrue(e.validate_configuration())


class FfmpegArguementsTestCase(TestCase):

    def test_invalid_args(self):

        from html5video import Encoder
        from html5video.encoders.ffmpeg import FfmpegException

        ffmpeg = Encoder('dummy_file')

        with self.assertRaises(FfmpegException):
            ffmpeg.call(['ffmpeg', '-this-is-not-a-recognised-arguement'])

    def test_build_args(self):

        from html5video import Encoder

        ffmpeg = Encoder("v.something")
        expected = "ffmpeg -b 1500k -y -i v.something v.tmp"
        actual = ' '.join(ffmpeg.build_args([], 'v.tmp'))
        self.assertEqual(expected, actual)

    def test_mp4_args(self):

        from html5video import Encoder

        ffmpeg = Encoder("v.something")
        expected = "ffmpeg -b 1500k -y -i v.something v.mp4"
        actual = ' '.join(ffmpeg.mp4_args())
        self.assertEqual(expected, actual)

    def test_webm_args(self):

        from html5video import Encoder

        ffmpeg = Encoder("v.something")
        expected = "ffmpeg -b 1500k -y -i v.something -vcodec libvpx -f webm -acodec libvorbis -ab 160000 v.webm"
        actual = ' '.join(ffmpeg.webm_args())
        self.assertEqual(expected, actual)

    def test_ogv_args(self):

        from html5video import Encoder

        ffmpeg = Encoder("v.something")
        expected = "ffmpeg -b 1500k -y -i v.something -vcodec libtheora -acodec libvorbis -ab 160000 v.ogv"
        actual = ' '.join(ffmpeg.ogv_args())
        self.assertEqual(expected, actual)
