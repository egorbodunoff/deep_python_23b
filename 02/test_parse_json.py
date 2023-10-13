import unittest
from unittest import mock

from parse_json import parse_json


class TestParseJson(unittest.TestCase):
    def setUp(self) -> None:
        self.json_str = ('{"key1": "ultrasound imaging", "key2": "CT imaging",'
                         ' "KEy1": "diagnostic and imaging", "key3": "plants is plants"}')

        self.test_cases = [
            {
                'arg': {'required_fields': ['key1', 'key2'], 'keywords': ['imaging', 'CT']},
                'expected_result': [('key1', 'imaging'), ('key2', 'imaging'), ('key2', 'CT')],
                'expected_callback': 3

            },
            {
                'arg': {'required_fields': ['key1', 'key2'], 'keywords': ['Imaging', 'ct']},
                'expected_result': [('key1', 'Imaging'), ('key2', 'Imaging'), ('key2', 'ct')],
                'expected_callback': 3

            },
            {
                'arg': {'required_fields': ['key3'], 'keywords': ['and', 'plants']},
                'expected_result': [('key3', 'plants')],
                'expected_callback': 1

            },
            {
                'arg': {'required_fields': ['KEy1'], 'keywords': ['and', 'imaging']},
                'expected_result': [('KEy1', 'and'), ('KEy1', 'imaging')],
                'expected_callback': 2

            },
            {
                'arg': {'required_fields': ['key10'], 'keywords': ['word23', 'word3']},
                'expected_result': [],
                'expected_callback': 0
            },
            {
                'arg': {'required_fields': ['key1', 'key2'], 'keywords': ['int']},
                'expected_result': [],
                'expected_callback': 0
            }
        ]

    def test_keyword_callback(self):
        for i, test_case in enumerate(self.test_cases):
            mock_callback = mock.Mock()

            parse_json(self.json_str, mock_callback, *test_case['arg'].values())

            call_arg = []
            for call in mock_callback.call_args_list:
                call_arg.append(call[0])

            self.assertEqual(call_arg, test_case['expected_result'])

    def test_call_count(self):
        for test_case in self.test_cases:
            mock_callback = mock.Mock()
            parse_json(self.json_str, mock_callback, *test_case['arg'].values())

            self.assertEqual(mock_callback.call_count, test_case['expected_callback'])

    def test_err(self):
        with self.assertRaises(TypeError) as err:
            parse_json(self.json_str, "not_func", ['key1'], ['ffv'])

        self.assertEqual(type(err.exception), TypeError)
