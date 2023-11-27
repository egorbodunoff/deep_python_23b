from memory_profiler import profile
import weakref


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


@profile
def com(n):
    c = [CommonClass(d1, arr1) for _ in range(n)]

    for i in c:
        i.arr[2] = 4
        i.d['k2'] = 4


@profile
def slots(n):
    sl = [SlotClass(d1, arr1) for _ in range(n)]

    for i in sl:
        i.arr[2] = 4
        i.d['k2'] = 4


@profile
def ref(n):
    r = [RefClass(d_r, arr_r) for _ in range(n)]

    for i in r:
        i.wr_arr()[2] = 4
        i.wr_d()['k2'] = 4


if __name__ == "__main__":
    d1 = {'k1': 1, 'k2': 2, 'k3': 3}
    arr1 = [1, 2, '3', '4', 5, '6']
    arr_r = ListObj(arr1)
    d_r = DictObj(d1)

    N = 100000

    com(N)
    slots(N)
    ref(N)
