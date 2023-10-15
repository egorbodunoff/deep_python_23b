import unittest
from unittest import mock

from descriptors import LineUpDescriptor, DurationDescriptor, ResDescriptor


class TestDescriptors(unittest.TestCase):
    def setUp(self) -> None:
        class Match:
            line_up = LineUpDescriptor()
            duration = DurationDescriptor()
            res = ResDescriptor()

            def __init__(self, line_up, duration, res):
                self.line_up = line_up
                self.duration = duration
                self.res = res

        self.Match = Match

        self.test_cases = [
            {
                'arg': {'line_up': ['вася', 'петя', 'артем'],
                        'duration': 25, 'res': {'Звезда': 3, 'Искра': 2}},
                'expected_result': ['Cтартовый состав на сегодняшний матч: вася, петя, артем',
                                    'Длительность матча 25 минут',
                                    'со счетом 3 : 2 победила команда Звезда']
            },
            {
                'arg': {'line_up': ['вася', 'петя', 'артем', 'дима'],
                        'duration': 22, 'res': {'Звезда': 2, 'Искра': 2}},
                'expected_result': ['Cтартовый состав на сегодняшний матч: вася, петя, артем, дима',
                                    'Длительность матча 22 минуты',
                                    'ничейный резултат']
            },
            {
                'arg': {'line_up': ['вася', 'петя', 'артем'],
                        'duration': 1, 'res': {'Звезда': 1, 'Искра': 2}},
                'expected_result': ['Cтартовый состав на сегодняшний матч: вася, петя, артем',
                                    'Длительность матча 1 минута',
                                    'со счетом 2 : 1 победила команда Искра']
            }
        ]

        self.test_err = [
            {
                'arg': {'line_up': ['вася', 'петя'],
                        'duration': 25, 'res': {'Звезда': 3, 'Искра': 2}},
                'expected_result': ValueError,
                'error_arg': ('В стартовом составе должно быть от 3 до 5 игроков',)
            },
            {
                'arg': {'line_up': ['вася', 'петя'],
                        'duration': 25, 'res': {'Звезда': 3, 'Искра': 2}},
                'expected_result': TypeError,
                'error_arg': ('имена игроков должны быть строками',)
            },
            {
                'arg': {'line_up': 'вася, петя, саша',
                        'duration': 25, 'res': {'Звезда': 3, 'Искра': 2}},
                'expected_result': TypeError,
                'error_arg': ('необходимо передать список игроков',)
            },
            {
                'arg': {'line_up': ['вася', 'петя', 'артем'],
                        'duration': '25', 'res': {'Звезда': 3, 'Искра': 2}},
                'expected_result': TypeError,
                'error_arg': ('продолжительность матча должна быть целым числом',)
            },
            {
                'arg': {'line_up': ['вася', 'петя', 'артем'],
                        'duration': -5, 'res': {'Звезда': 3, 'Искра': 2}},
                'expected_result': ValueError,
                'error_arg': ('длительность матча должна лежать в диапазоне [0, 60]',)
            },
            {
                'arg': {'line_up': ['вася', 'петя', 'артем'],
                        'duration': 25, 'res': ['Звезда', 3, 'Искра', 2]},
                'expected_result': TypeError,
                'error_arg': ('необходимо передать результаты в виде словаря'
                              'например {Искра: 3, Звезда: 1',)
            },
            {
                'arg': {'line_up': ['вася', 'петя', 'артем'],
                        'duration': 25, 'res': {'Звезда': 4.0, 'Искра': 2}},
                'expected_result': TypeError,
                'error_arg': ('количество забитых мячей должно быть целым числом',)
            },
            {
                'arg': {'line_up': ['вася', 'петя', 'артем'],
                        'duration': 25, 'res': {1: 3, 'Искра': 2}},
                'expected_result': TypeError,
                'error_arg': ('названия команд должны быть строками',)
            },
            {
                'arg': {'line_up': ['вася', 'петя', 'артем'],
                        'duration': 25, 'res': {'Звезда': -3, 'Искра': 2}},
                'expected_result': ValueError,
                'error_arg': ('количество голов не может быть меньше 0',)
            }

        ]

    def test_line_up_desc(self):
        for test_case in self.test_cases:
            m = self.Match(*test_case['arg'].values())
            res = [m.line_up, m.duration, m.res]

            self.assertEqual(res, test_case['expected_result'])

    def test_err(self):
        for test_case in self.test_err[:1]:
            with self.assertRaises(ValueError) as err:
                self.Match(*test_case['arg'].values())

            self.assertEqual(err.exception.args, test_case['error_arg'])
            self.assertEqual(type(err.exception), test_case['expected_result'])

    def set_attr(self):
        m = self.Match(['вася', 'петя', 'артем'], 25, {'Звезда': 3, 'Искра': 2})

        m.line_up = ['ваня', 'дима', 'егор']
        self.assertEqual(m.line_up, 'Cтартовый состав на сегодняшний матч: ваня, дима, егор')

        m.duration = 15
        self.assertEqual(m.duration, 'Длительность матча 25 минут')

        m.res = {'команда1': 2, 'команда2': 1}
        self.assertEqual(m.res, 'со счетом 2 : 1 победила команда команда1')

    def set_bad_attr(self):
        m = self.Match(['вася', 'петя', 'артем'], 25, {'Звезда': 3, 'Искра': 2})

        with self.assertRaises(ValueError) as err:
            m.line_up = ['ваня', 'дима']
        self.assertEqual(err.exception.args,
                         "В стартовом составе должно быть от 3 до 5 игроков")
        self.assertEqual(type(err.exception), ValueError)

        with self.assertRaises(ValueError) as err:
            m.duration = -1
        self.assertEqual(err.exception.args,
                         "продолжительность матча должна быть целым числом")
        self.assertEqual(type(err.exception), TypeError)

        with self.assertRaises(ValueError) as err:
            m.res = ['команда1', 2, 'команда2', 1]
        self.assertEqual(err.exception.args, "необходимо передать результаты в виде словаря"
                                             "например {Искра: 3, Звезда: 1")
        self.assertEqual(type(err.exception), TypeError)
