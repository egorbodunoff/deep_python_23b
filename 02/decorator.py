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

            print(wrapper.mean)

        wrapper.runtime = defaultdict(list)
        wrapper.mean = None

        return wrapper

    return inner_mean
