from typing import Iterable
from typing import Union
from typing import TextIO
from io import TextIOWrapper


def gen(
        words: list[str],
        file_name: str = None,
        file_obj: Union[TextIOWrapper, TextIO] = None
) -> Iterable[str]:
    words = [word.lower() for word in words]

    def file_process(set_words: set,
                     file: Union[TextIOWrapper, TextIO] = None
                     ) -> Iterable[str]:

        for row in file:
            if set_words & set(row.lower().split()):
                yield row.rstrip()

    if file_name is not None:
        try:
            with open(file_name, "r") as f:
                yield from file_process(set(words), f)

        except FileNotFoundError:
            yield "File not found"

    elif file_obj is not None:
        with file_obj as f:
            yield from file_process(set(words), f)
