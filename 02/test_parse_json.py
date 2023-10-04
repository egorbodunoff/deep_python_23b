import unittest
from unittest import mock

from parse_json import parse_json


class TestParseJson(unittest.TestCase):
    def setUp(self) -> None:
        self.json_str = ('{"key1": "ultrasound imaging", "key2": "CT imaging",'
                         ' "KEy1": "diagnostic and imaging", "key3": "plants"}')

        self.test_cases = [
            {
                'arg': {'required_fields': ['key1', 'key2'], 'keywords': ['imaging', 'CT']},
                'expected_result': ['imaging', 'CT'],
                'expected_callback': 2

            },
            {
                'arg': {'required_fields': ['key1', 'key2'], 'keywords': ['Imaging', 'ct']},
                'expected_result': ['Imaging', 'ct'],
                'expected_callback': 2

            },
            {
                'arg': {'required_fields': ['key3'], 'keywords': ['and', 'plants']},
                'expected_result': ['plants'],
                'expected_callback': 1

            },
            {
                'arg': {'required_fields': ['KEy1'], 'keywords': ['and', 'imaging']},
                'expected_result': ['and', 'imaging'],
                'expected_callback': 2

            },
            {
                'arg': {'required_fields': ['key10'], 'keywords': ['word23', 'word3']},
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
                call_arg.append(call[0][0])

            self.assertEqual(set(call_arg), set(test_case['expected_result']))  # Чтобы не учитывался порядок

    def test_call_count(self):
        expected_callback = [2, 2, 1, 2, 0]

        for i, test_case in enumerate(self.test_cases):
            mock_callback = mock.Mock()
            parse_json(self.json_str, mock_callback, *test_case['arg'].values())

            self.assertEqual(mock_callback.call_count, expected_callback[i])
