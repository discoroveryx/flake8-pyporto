import ast
import os
import unittest
from unittest import mock

from flake8_pyporto import PyPorto

from .constants import BASE_DIR, GET_FILENAME_WRAPPER_METHOD_NAME, TESTS_FOLDER


class ClassNameTestingTest(unittest.TestCase):
    def _join_path(self, path: tuple) -> str:
        return os.path.join(BASE_DIR, TESTS_FOLDER, *path)

    def _parse_content_from_file(self, path: str):
        content = open(path).read()
        tree = ast.parse(content)
        return tree

    def _run_plugin(self, tree):
        plugin = PyPorto(tree)
        return {f'{line}:{col} {msg}' for line, col, msg, _ in plugin.run()}

    @mock.patch.object(PyPorto, GET_FILENAME_WRAPPER_METHOD_NAME)
    def test_unary_not_equality(self, mocked_filename):
        path = ('app', 'container_1', 'tasks', 'get_product_list_task.py')
        path_joined = self._join_path(path)

        mocked_filename.return_value = path[-1]

        tree = self._parse_content_from_file(path_joined)
        result = self._run_plugin(tree)

        self.assertEqual(result, {'1:0 PYP001 A task class name must have suffix "Task"'})


if __name__ == '__main__':
    unittest.main()
