import weakref
import time


class DictObj(dict):
    pass


class ListObj(list):
    pass


class RefClass:
    def __init__(self, obj, arr):
        self.wr_d = weakref.ref(obj)
        self.wr_arr = weakref.ref(arr)


class SlotClass:
    __slots__ = ('arr', 'd')

    def __init__(self, d, arr):
        self.d = d
        self.arr = arr


class CommonClass:
    def __init__(self, d, arr):
        self.d = d
        self.arr = arr


N = 10 ** 6
d1 = {'k1': 1, 'k2': 2, 'k3': 3}
arr1 = [1, 2, '3', '4', 5, '6']
arr_r = ListObj(arr1)
d_r = DictObj(d1)

def com():
    t_start = time.time()
    for _ in range(6):
        com = [CommonClass(d1, arr1) for _ in range(N)]

        for i in com:
            i.arr[2] = 4
            i.d['k2'] = 4
    t_end = time.time() - t_start
    print(f'изменение атрибутов класса с обычными атрибутами: {t_end / 6}')

def slots():
    t_start = time.time()
    for _ in range(6):
        slots = [SlotClass(d1, arr1) for _ in range(N)]

        for i in slots:
            i.arr[2] = 4
            i.d['k2'] = 4
    t_end = time.time() - t_start
    print(f'изменение атрибутов класса с слотами: {t_end / 6}')


def ref():
    t_start = time.time()
    for _ in range(6):
        ref = [RefClass(d_r, arr_r) for _ in range(N)]
        for i in ref:
            arr = i.wr_arr()
            d = i.wr_d()
    t_end = time.time() - t_start
    print(f'создание экзэмпляров класса с атрибутами weakref: {t_end / 6}')
