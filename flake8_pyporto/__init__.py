import ast
from dataclasses import dataclass
import os


@dataclass
class MapOfErrors:
    code: str
    condition: str
    desc: str


@dataclass
class TailsOfClassName:
    task = MapOfErrors('PYP001', 'Task', 'A task class name must have suffix "Task"')


class PyPorto:
    name = __name__
    version = '1.0'

    def get_filename_wrapper(self, filename):
        """It needs to mock for testing."""
        return filename

    def validate_task(self, tree):
        for i in tree.body:
            if isinstance(i, ast.ClassDef):
                suffix_len = len(TailsOfClassName.task.condition)

                if i.name[-suffix_len:] != TailsOfClassName.task.condition:
                    self.errors.append(
                        (
                            i.lineno,
                            i.col_offset,
                            f'{TailsOfClassName.task.code} {TailsOfClassName.task.desc}',
                        ),
                    )

                # for i_bases in i.bases:
                #     ...

    def __init__(self, tree, filename='(none)', file_tokens=None):
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
            if file_name_splited[-1] == 'task.py':
                # print(ast.dump(tree, indent=4))  # noqa: E800

                self.validate_task(tree)

    def run(self):
        for line_number, offset, text in self.errors:
            yield (
                line_number,
                offset,
                text,
                type(self),
            )
