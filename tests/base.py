from unittest2 import TestCase


class BaseEncoderTestBase(TestCase):

    def test_base_encoder(self):
        """
        Basic tests for the BaseEncoder and getting the output file name.
        """

        from html5video.encoders.base import BaseEncoder

        encoder = BaseEncoder('fake_file.mov')

        self.assertEqual('fake_file.avi', encoder.get_output_path('avi'))

    def test_path_calculations(self):

        from html5video.encoders.base import BaseEncoder

        test_cases = (
            # No output specified
            ('/my/video2.mov', None, '/my/video2.mp4'),
            # Output is a directory
            ('/my/video1.mov', '/tmp/', '/tmp/video1.mp4'),
            # Output is a specific file path
            ('/my/video3.mov', '/tmp/out3', '/tmp/out3.mp4'),
        )

        for source, in_path, out_path in test_cases:

            e = BaseEncoder(source, in_path)
            self.assertEquals(e.get_output_path('mp4'), out_path)

    def test_dimensions(self):

        from html5video.encoders.base import BaseEncoder

        e = BaseEncoder('fake_file.mov')

        self.assertEqual(e.dimensions, None)

        e.dimensions = "100x200"

        self.assertEqual(e.width, "100")
        self.assertEqual(e.height, "200")
        self.assertEqual(e.dimensions, "100x200")

        with self.assertRaises(AttributeError):
            e.dimensions = None

    def test_group(self):

        from html5video.encoders.base import BaseEncoder

        class MyEncoder(BaseEncoder):
            binary = "my_encoder"
            quality_flag = '-q'
            group_flag = '--group'
            dimensions_flag = '-xy'

        e = MyEncoder('some_video.avi')

        e.group = 90
        e.dimensions = "10x10"

        self.assertEqual(['my_encoder', '--group', 90, '-xy', '10x10'], e.build_args())
