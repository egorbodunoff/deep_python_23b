import cProfile


def profile_deco(func):
    def wrapper(*args, **kwargs):
        print(wrapper.profiler)
        profiler = wrapper.profiler
        result = profiler.runcall(func, *args, **kwargs)
        return result

    wrapper.profiler = cProfile.Profile()

    wrapper.print_stat = lambda: wrapper.profiler.print_stats()

    return wrapper


@profile_deco
def add(a, b):
    for _ in range(1_000_000):
        a + b
    return a + b


@profile_deco
def sub(a, b):
    return a - b


print(add(1, 2))
print(add(4, 5))
print(add(1, 5))
print(sub(4, 2))
print(sub(4, 2))
add.print_stat()  # выводится результат профилирования суммарно по всем вызовам функции add (всего два вызова)
sub.print_stat()  # выводится результат профилирования суммарно по всем вызовам функции sub (всего один вызов)
print(add(1, 2))
print(add(4, 5))
add.print_stat()