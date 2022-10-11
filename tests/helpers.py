import ast
import os
from argparse import Namespace

from flake8_pyporto import PyPorto

from .constants import BASE_DIR, TESTS_FOLDER


def join_path(path: tuple) -> str:
    return os.path.join(BASE_DIR, TESTS_FOLDER, *path)


def parse_content_from_file(path: str):
    content = open(path).read()
    tree = ast.parse(content)
    return tree


def run_plugin(path, config: Namespace = None):
    path_joined = join_path(path)
    tree = parse_content_from_file(path_joined)
    plugin = PyPorto(tree, path_joined)

    if config is not None:
        plugin.parse_options(config)

    return {f'{line}:{col} {msg}' for line, col, msg, _ in plugin.run()}
