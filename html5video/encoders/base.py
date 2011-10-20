from unipath import Path


class ImproperlyConfigured(Exception):
    pass


class EncoderException(Exception):
    pass


class BaseEncoder(object):

    def __init__(self, input_file, output_file=None, binary=None):

        self.width = None
        self.height = None
        self.quality = None
        self.group = None

        if binary:
            self.binary = binary

        self.input_file = Path(input_file)

        input_name = self.input_file.name.rsplit('.', 1)[0]

        if output_file:
            output_file = Path(output_file)
            if output_file.isdir():
                self.output_file = output_file.child(input_name)
            else:
                self.output_file = output_file
        else:
            self.output_file = self.input_file.parent.child(self.input_file.stem)

    def get_output_path(self, format):
        return "{path}.{format}".format(path=self.output_file, format=format)

    @property
    def dimensions(self):
        if self.width or self.height:
            return "{w}x{h}".format(w=self.width, h=self.height)

    @dimensions.setter
    def dimensions(self, value):
        self.width, self.height = value.split('x')

    def build_args(self):

        base_args = [self.binary, ]

        if self.quality:
            base_args.extend([self.quality_flag, self.quality])

        if self.group:
            base_args.extend([self.group_flag, self.group])

        if self.dimensions:
            base_args.extend([self.dimensions_flag, self.dimensions])

        return base_args
