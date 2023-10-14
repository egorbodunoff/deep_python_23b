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
