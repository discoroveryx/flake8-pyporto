import unittest
from argparse import Namespace

from .helpers import run_plugin


class HandlerClassNameTest(unittest.TestCase):
    def test_handler_class_name(self):
        path = ('app', 'container_1', 'handlers', 'get_product_list_handler.py')

        result = run_plugin(path)

        self.assertEqual(
            result, {'1:0 PYP001 A task/handler class name must have suffix "Handler"'},
        )
        
    def test_handler_class_name_with_confit_handler_suffix(self):
        path = ('app', 'container_1', 'handlers', 'get_product_list_handler.py')
        
        config = Namespace(verbose=0, handler_suffix='MyTaskHandler')

        result = run_plugin(path, config)

        self.assertEqual(
            result, {'1:0 PYP001 A task/handler class name must have suffix "MyTaskHandler"'},
        )


if __name__ == '__main__':
    unittest.main()
