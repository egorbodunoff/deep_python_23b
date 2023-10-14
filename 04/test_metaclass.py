import unittest

from metaclass import CustomMeta


class TestMetaClass(unittest.TestCase):
    def setUp(self) -> None:
        class CustomClass(metaclass=CustomMeta):
            x = 50

            def __init__(self, val=99):
                self.val = val

            @staticmethod
            def line():
                return 100

            def my_add(self):
                return self.x + self.val

            def __str__(self):
                return "Custom_by_metaclass"

        self.custom_class = CustomClass

    def test_class_atr(self):
        self.assertEqual(self.custom_class.custom_x, 50)

        self.assertEqual(self.custom_class.custom_line(), 100)

        with self.assertRaises(AttributeError) as err:
            print(self.custom_class.x)
        self.assertEqual(type(err.exception), AttributeError)

        with self.assertRaises(AttributeError) as err:
            print(self.custom_class.line())
        self.assertEqual(type(err.exception), AttributeError)

    def test_inst_atr(self):
        inst = self.custom_class()

        self.assertEqual(inst.custom_x, 50)
        self.assertEqual(inst.custom_val, 99)
        self.assertEqual(inst.custom_line(), 100)
        self.assertEqual(str(inst), "Custom_by_metaclass")

        with self.assertRaises(AttributeError) as err:
            print(inst.x)
        self.assertEqual(type(err.exception), AttributeError)

        with self.assertRaises(AttributeError) as err:
            print(inst.val)
        self.assertEqual(type(err.exception), AttributeError)

        with self.assertRaises(AttributeError) as err:
            print(inst.line())
        self.assertEqual(type(err.exception), AttributeError)

    def test_dynamic_atr(self):
        inst = self.custom_class(30)
        inst.dynamic = "added later"

        self.assertEqual(inst.custom_val, 30)
        self.assertEqual(inst.custom_dynamic, "added later")

        with self.assertRaises(AttributeError) as err:
            print(inst.dynamic)
        self.assertEqual(type(err.exception), AttributeError)

