from collections import defaultdict
import time


def mean(k):
    def inner_mean(func):
        def wrapper(*args, **kwargs):
            time_start = time.time()

            func(*args, **kwargs)
            duration = time.time() - time_start
            wrapper.runtime[func.__name__].append(duration)

            if len(wrapper.runtime[func.__name__]) >= k:
                wrapper.mean = sum(wrapper.runtime[func.__name__][-k:]) / k
            else:
                wrapper.mean = (sum(wrapper.runtime[func.__name__]) /
                                len(wrapper.runtime[func.__name__]))

            return wrapper.mean

        wrapper.runtime = defaultdict(list)
        wrapper.mean = None

        return wrapper

    return inner_mean


# @mean('a')
# def foo(arg):
#     return arg
# print(f.mean)
# # print(f.mean)
# @mean(3)
# def bar():
#     time.sleep(0.5)
#
#
# for _ in range(3):
#     print(foo(1))
#     print(bar())
# for _ in range(4):
#     bar()
#
# # print(bar.__dict__['mean'])
