import unittest
from unittest import mock
from unittest.mock import mock_open

from message_evaluation import SomeModel, predict_message_mood
from generator import gen


class TestEvaluation(unittest.TestCase):
    def test_predict(self):
        test_cases = [
            {
                'arg': {'message': 'Чапаев и пустота'},
                'expected_result': 'отл'

            },
            {
                'arg': {'message': 'Золотой ключ'},
                'expected_result': 'норм'

            },
            {
                'arg': {'message': 'Вулкан'},
                'expected_result': 'неуд'
            }
        ]
        with mock.patch('message_evaluation.SomeModel.predict') as mock_predict:
            mock_predict.side_effect = [0.9, 0.6, 0.2]

            for test_case in test_cases:
                model = SomeModel()
                result = predict_message_mood(str(*test_case['arg'].values()), model)

                self.assertEqual(test_case['expected_result'], result)

    def test_exception(self):
        with mock.patch('message_evaluation.SomeModel.predict') as mock_predict:
            mock_predict.side_effect = TypeError

            with self.assertRaises(TypeError) as err:
                predict_message_mood('груша', SomeModel())

            self.assertEqual(TypeError, type(err.exception))

    def test_model(self):
        with mock.patch('message_evaluation.SomeModel.predict') as mock_predict:
            mock_predict.return_value = 0.8

            self.assertEqual(0.8, SomeModel().predict('яблоко'))

        self.assertEqual(SomeModel().predict('яблоко и груша'), 0.7300408448338399)


class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.text = 'Я помню чудное мгновенье:\n' \
                    'Передо мной явилась ты,\n' \
                    'Как мимолетное виденье,\n' \
                    'Как гений чистой красоты.\n'
        self.test_cases = [
            {
                'arg': {'words': ['передо', 'я']},
                'expected_result': ['Я помню чудное мгновенье:',
                                    'Передо мной явилась ты,'
                                    ]

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
