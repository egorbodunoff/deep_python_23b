import unittest

from custom_list import CustomList


class TestCustomList(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_add(self):
        self.assertEqual(CustomList([5, 1, 3, 7]) + CustomList([1, 2, 7]), CustomList([6, 3, 10, 7]))
        self.assertEqual((CustomList([1])) + [2, 5], CustomList([3, 5]))
        self.assertEqual([2, 5] + CustomList([1]), CustomList([3, 5]))

    def test_sub(self):
        self.assertEqual(CustomList([5, 1, 3, 7]) - CustomList([1, 2, 7]), CustomList([4, -1, -4, 7]))
        self.assertEqual(CustomList([1]) - [2, 5], CustomList([-1, -5]))
        self.assertEqual([2, 5] - CustomList([1]), CustomList([1, 5]))

    def test_compare(self):
        self.assertEqual(CustomList([5, 1, 3]) == CustomList([2, 7]), True)
        self.assertEqual(CustomList([6, 3, 3]) == CustomList([2, 6, 1]), False)

        self.assertEqual(CustomList([1, 4, 3]) > CustomList([1, 5]), True)
        self.assertEqual(CustomList([3, 3, 3]) > CustomList([2, 6, 1]), False)

        self.assertEqual(CustomList([1, 4, 3]) < CustomList([1, 5]), False)
        self.assertEqual(CustomList([3, 1, 3]) < CustomList([2, 6, 1]), True)

        self.assertEqual(CustomList([1, 4, 3]) >= CustomList([8]), True)
        self.assertEqual(CustomList([1, 4, 3, 7]) >= CustomList([8, 2]), True)
        self.assertEqual(CustomList([3, 3, 3]) >= CustomList([2, 6, 2]), False)

        self.assertEqual(CustomList([1, 2, 3]) <= CustomList([8]), True)
        self.assertEqual(CustomList([1, 4, 3, 0]) <= CustomList([8, 2, 9]), True)
        self.assertEqual(CustomList([3, 8, 8]) <= CustomList([2, 6, 2]), False)

    def test_str(self):
        res = str(CustomList([4, 3, 3]))

        self.assertEqual(res, "элементы: [4, 3, 3], их сумма: 10")

    def test_setter(self):
        l1 = CustomList([3, 5, 3])

        with self.assertRaises(TypeError):
            l1.data = 6

    def test_get(self):
        l1 = CustomList([3, 5, 3])

        res = l1.data
        self.assertEqual(res, [3, 5, 3])

    def test_add_error(self):
        with self.assertRaises(TypeError):
            CustomList([3, 5, 3]) + 4
        with self.assertRaises(TypeError):
            4 + CustomList([3, 5, 3])

        with self.assertRaises(TypeError):
            CustomList([3, 5, 3]) - 4
        with self.assertRaises(TypeError):
            4 - CustomList([3, 5, 3])

        with self.assertRaises(TypeError):
            trash = CustomList([3, 5, 3]) == 4
        with self.assertRaises(TypeError):
            trash = 'ff' == CustomList([3, 5, 3])

        with self.assertRaises(TypeError):
            trash = CustomList([3, 5, 3]) > 4
        with self.assertRaises(TypeError):
            trash = 'ff' > CustomList([3, 5, 3])

        with self.assertRaises(TypeError):
            trash = CustomList([3, 5, 3]) < 4
        with self.assertRaises(TypeError):
            trash = 'ff' < CustomList([3, 5, 3])

        with self.assertRaises(TypeError):
            trash = CustomList([3, 5, 3]) >= 4
        with self.assertRaises(TypeError):
            trash = 'ff' >= CustomList([3, 5, 3])

        with self.assertRaises(TypeError):
            trash = CustomList([3, 5, 3]) <= 4
        with self.assertRaises(TypeError):
            trash = 'ff' <= CustomList([3, 5, 3])
