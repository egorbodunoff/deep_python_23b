import unittest
from unittest import mock
from unittest.mock import mock_open

from generator import gen


class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.text = 'Я помню чудное мгновенье:\n' \
                    'Передо мной явилась ты,\n' \
                    'Как мимолетное виденье,\n' \
                    'Как гений чистой красоты.\n' \
                    'красота'
        self.test_cases = [
            {
                'arg': {'words': ['передо', 'я']},
                'expected_result': ['Я помню чудное мгновенье:',
                                    'Передо мной явилась ты,'
                                    ]

            },
            {
                'arg': {'words': ['как', 'гений']},
                'expected_result': ['Как мимолетное виденье,',
                                    'Как гений чистой красоты.'
                                    ]

            },
            {
                'arg': {'words': ['красота']},
                'expected_result': ['красота']
            },
            {
                'arg': {'words': ['0']},
                'expected_result': []
            }
        ]

    def test_gen_name(self):
        for test_case in self.test_cases:
            with mock.patch('builtins.open', mock_open(read_data=self.text)):
                result = list(gen(*test_case['arg'].values(), file_name='path/to/open'))

            self.assertEqual(test_case['expected_result'], result)

    def test_gen_obj(self):
        for test_case in self.test_cases:
            with mock.patch('builtins.open', mock_open(read_data=self.text)):
                result = list(gen(*test_case['arg'].values(), file_obj=open('path/to/open')))

            self.assertEqual(test_case['expected_result'], result)

    def test_exception(self):
        result = list(gen(['data'], file_name="text1.txt"))

        self.assertEqual(['File not found'], result)


if __name__ == '__main__':
    unittest.main()
