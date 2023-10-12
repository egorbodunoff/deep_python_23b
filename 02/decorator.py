from collections import defaultdict
import time


def mean(k):
    def inner_mean(func):
        def wrapper(*args, **kwargs):
            time_start = time.time()

            result = func(*args, **kwargs)
            duration = time.time() - time_start
            wrapper.runtime.append(duration)

            if len(wrapper.runtime) >= k:
                wrapper.mean = sum(wrapper.runtime[-k:]) / k
            else:
                wrapper.mean = (sum(wrapper.runtime) /
                                len(wrapper.runtime))

            print(wrapper.mean)
            return result

        wrapper.runtime = list()
        wrapper.mean = None

        return wrapper

    return inner_mean
