import ast
import os
from dataclasses import dataclass

DEFAULT_CONFIG_HANDLER = 'handler'
FILE_SUFFIX_HANDLER = 'handler.py'
DEFAULT_HANDLER_DESC = 'A task/handler class name must have suffix "{}"'


def capitalize_title(value):
    return value[0].upper() + value[1:]


@dataclass
class MapOfErrors:
    code: str
    condition: str
    desc: str


@dataclass
class TailsOfClassName:
    handler = MapOfErrors(
        code='PYP001',
        condition=capitalize_title(DEFAULT_CONFIG_HANDLER),
        desc=DEFAULT_HANDLER_DESC.format(capitalize_title(DEFAULT_CONFIG_HANDLER)),
    )


class PyPorto:
    name = __name__
    version = '1.0'

    def get_filename_wrapper(self, filename):
        """It needs to mock for testing."""
        return filename

    def validate_handler(self, tree):
        for i in tree.body:
            if isinstance(i, ast.ClassDef):
                suffix_len = len(TailsOfClassName.handler.condition)
                if i.name[-suffix_len:] != TailsOfClassName.handler.condition:
                    self.errors.append(
                        (
                            i.lineno,
                            i.col_offset,
                            f'{TailsOfClassName.handler.code} {TailsOfClassName.handler.desc}',
                        ),
                    )

                # for i_bases in i.bases:
                #     ...

    def __init__(self, tree, filename='(none)', file_tokens=None):
        self.tree = tree
        self.filename = filename
        self.file_tokens = file_tokens

    def _run(self):
        tree = self.tree
        filename = self.filename
        file_tokens = self.file_tokens
        filename = self.get_filename_wrapper(filename)

        fn = 'stdin' if filename in ('stdin', '-', None) else filename
        self.filename = fn
        self.tokens = file_tokens

        self.errors = []

        path_splited = os.path.split(self.filename)

        file_name = path_splited[-1]

        file_name_splited = file_name.split('_')

        if len(file_name_splited) >= 2:
            # Case validate *task.py
            if file_name_splited[-1] == FILE_SUFFIX_HANDLER:
                # print(ast.dump(tree, indent=4))  # noqa: E800

                self.validate_handler(tree)

    def run(self):
        self._run()

        for line_number, offset, text in self.errors:
            yield (
                line_number,
                offset,
                text,
                type(self),
            )

    @classmethod
    def add_options(cls, parser):
        parser.add_option(
            '--handler-suffix',
            default=DEFAULT_CONFIG_HANDLER,
            parse_from_config=True,
            type=str,
            help='Suffix for handler files and classes.',
        )

    @classmethod
    def parse_options(cls, options) -> None:
        cls.config = {}
        if hasattr(options, 'handler_suffix') and options.handler_suffix is not None:
            cls.config.update({'handler_suffix': options.handler_suffix})
            TailsOfClassName.handler.condition = options.handler_suffix
            TailsOfClassName.handler.desc = DEFAULT_HANDLER_DESC.format(
                capitalize_title(options.handler_suffix),
            )
