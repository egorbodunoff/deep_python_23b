import unittest

from custom_list import CustomList


class TestCustomList(unittest.TestCase):
    def setUp(self) -> None:
        self.l1 = CustomList([5, 1, 3, 7])
        self.l2 = CustomList([1, 2, 7])
        self.l3 = CustomList([5, 4, 2])
        self.l4 = [3, 5, 3, 1]
        self.l5 = [1, 6, 2]
        self.l6 = [6, 2]

    def compare(self, list1, list2):
        for i in range(len(list1)):
            self.assertEqual(list1[i], list2[i])

    def test_add(self):
        self.compare(self.l1 + self.l2, CustomList([6, 3, 10, 7]))
        self.compare(self.l1 + self.l2, CustomList([6, 3, 10, 7]))
        self.compare(self.l2 + self.l3, CustomList([6, 6, 9]))
        self.compare(self.l3 + self.l1, CustomList([10, 5, 5, 7]))
        self.compare(self.l4 + self.l1, CustomList([8, 6, 6, 8]))
        self.compare(self.l5 + self.l1, CustomList([6, 7, 5, 7]))
        self.compare(self.l3 + self.l6, CustomList([11, 6, 2]))

        self.compare(self.l1, CustomList([5, 1, 3, 7]))
        self.compare(self.l2, CustomList([1, 2, 7]))
        self.compare(self.l3, CustomList([5, 4, 2]))
        self.compare(self.l4, [3, 5, 3, 1])
        self.compare(self.l5, [1, 6, 2])
        self.compare(self.l6, [6, 2])

    def test_sub(self):
        self.compare(self.l2 - self.l3, CustomList([-4, -2, 5]))
        self.compare(self.l1 - self.l3, CustomList([0, -3, 1, 7]))
        self.compare(self.l5 - self.l3, CustomList([-4, 2, 0]))
        self.compare(self.l6 - self.l2, CustomList([5, 0, -7]))
        self.compare(self.l2 - self.l4, CustomList([-2, -3, 4, -1]))
        self.compare(self.l4 - self.l2, CustomList([2, 3, -4, 1]))

        self.compare(self.l1, CustomList([5, 1, 3, 7]))
        self.compare(self.l2, CustomList([1, 2, 7]))
        self.compare(self.l3, CustomList([5, 4, 2]))
        self.compare(self.l4, [3, 5, 3, 1])
        self.compare(self.l5, [1, 6, 2])
        self.compare(self.l6, [6, 2])

    def test_compare(self):
        self.assertEqual(CustomList([5, 1, 3]) == CustomList([2, 7]), True)
        self.assertEqual(CustomList([6, 3, 3]) == CustomList([2, 6, 1]), False)

        self.assertEqual(CustomList([5, 1, 3]) != CustomList([2, 7]), False)
        self.assertEqual(CustomList([6, 3, 3]) != CustomList([2, 6, 1]), True)

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

        self.assertEqual(res, "элементы CustomList: [4, 3, 3], их сумма: 10")

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
            trash = CustomList([2, 1, 1]) != 4
        with self.assertRaises(TypeError):
            trash = 'ff' != CustomList([3, 5, 3])

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
