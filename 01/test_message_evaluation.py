import unittest
from unittest import mock

from message_evaluation import SomeModel, predict_message_mood


class TestEvaluation(unittest.TestCase):
    def setUp(self) -> None:
        self.test_cases = [
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
            },
            {
                'arg': {'message': 'зеленая трава'},
                'expected_result': 'норм'
            },
            {
                'arg': {'message': 'светлая комната'},
                'expected_result': 'отл'
            },
            {
                'arg': {'message': 'дерево'},
                'expected_result': 'норм'
            }
        ]

    def test_predict(self):
        with mock.patch('message_evaluation.SomeModel.predict') as mock_predict:
            mock_predict.side_effect = [0.9, 0.6, 0.29, 0.8, 0.81, 0.31]

            for test_case in self.test_cases:
                model = SomeModel()
                result = predict_message_mood(str(*test_case['arg'].values()), model)

                self.assertEqual(test_case['expected_result'], result)

    def test_change_threshold(self):
        with mock.patch('message_evaluation.SomeModel.predict') as mock_predict:
            mock_predict.side_effect = [0.95, 0.83, 0.50, 0.8, 0.91, 0.51]

            for test_case in self.test_cases:
                model = SomeModel()
                result = predict_message_mood(str(*test_case['arg'].values()),
                                              model,
                                              bad_thresholds=0.51,
                                              good_thresholds=0.90)

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

    def test_arg_transfer(self):
        with mock.patch('message_evaluation.SomeModel.predict') as mock_predict:
            mock_predict.return_value = 0.8

            predict_message_mood('груша', SomeModel())

        self.assertEqual(mock_predict.call_args[0][0], 'груша')

    def test_bad_argument(self):
        with self.assertRaises(TypeError):
            SomeModel().predict([1])


if __name__ == '__main__':
    unittest.main()
