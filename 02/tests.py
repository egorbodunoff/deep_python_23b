import time
import unittest
from unittest import mock

from parse_json import parse_json
from decorator import mean


class TestParseJson(unittest.TestCase):
    def setUp(self) -> None:
        self.json_str = '{"key1": "Word1 word23", "key2": "word23 word3"}'

    def test_parse_json(self):
        test_cases = [
            {
                'arg': {'required_fields': ['key1', 'key2'], 'keywords': ['word23', 'word3']},
                'expected_result': {'word3', 'word23'}

            },
            {
                'arg': {'required_fields': ['key1'], 'keywords': ['word23', 'word3']},
                'expected_result': {'word23'}

            },
            {
                'arg': {'required_fields': ['key10'], 'keywords': ['word23', 'word3']},
                'expected_result': set()
            }
        ]

        expected_callback = [2, 1, 0]
        for i, test_case in enumerate(test_cases):
            mock_callback = mock.Mock()

            result = parse_json(self.json_str, mock_callback, *test_case['arg'].values())
            self.assertEqual(mock_callback.call_count, expected_callback[i])

            self.assertEqual(result, test_case['expected_result'])


class TestDecorator(unittest.TestCase):
    def test_count_call(self):
        mock_func = mock.Mock()

        @mean(3)
        def foo(*args):
            return mock_func(*args)

        for _ in range(3):
            print(foo(1))

        self.assertEqual(mock_func.call_count, 3)

    def test_err(self):
        @mean('a')
        def foo(*args):
            return args

        with self.assertRaises(TypeError) as err:
            foo(1)

        self.assertEqual(type(err.exception), TypeError)

    def test_calc(self):
        @mean(3)
        def foo(*args):
            time.sleep(2)
            return args

        @mean(5)
        def boo(*args):
            time.sleep(2)
            return args

        for _ in range(4):
            foo(1)
            boo(1)

        self.assertEqual(int(foo.mean), 2)
        self.assertEqual(int(boo.mean), 2)
