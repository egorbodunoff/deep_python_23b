import time
import math
import unittest
from unittest import mock

from decorator import mean


class TestDecorator(unittest.TestCase):
    def setUp(self) -> None:
        self.call_count = 5
        self.time = 1.

    def test_count_call(self):
        @mean(3)
        def foo(*args):
            return args

        with mock.patch('builtins.print') as mock_print:
            for _ in range(self.call_count):
                foo(1)

        self.assertEqual(mock_print.call_count, self.call_count)

    def test_err(self):
        @mean('a')
        def foo(*args):
            return args

        with self.assertRaises(TypeError) as err:
            foo(1)

        self.assertEqual(type(err.exception), TypeError)

    def test_calc(self):
        @mean(8)
        def foo(*args):
            time.sleep(self.time)
            return args

        @mean(3)
        def boo(*args):
            time.sleep(self.time)
            return args

        with mock.patch('builtins.print') as mock_print:
            for _ in range(self.call_count):
                foo(1)
                boo(1)

        for i in mock_print.call_args_list:
            result = math.isclose(i[0][0], 1.0, rel_tol=1e-2)

            self.assertEqual(result, True)

    def test_func_return(self):
        @mean(3)
        def foo(*args):
            return args

        result = foo(1)
        self.assertEqual(result, (1,))
