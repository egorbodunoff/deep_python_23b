from typing import Iterable
from typing import Union
from typing import TextIO
from io import TextIOWrapper


def gen(
        words: list[str],
        file_name: str = None,
        file_obj: Union[TextIOWrapper, TextIO] = None
) -> Iterable[str]:
    if file_name is not None:
        try:
            with open(file_name, "r") as file:
                words = [word.lower() for word in words]
                for row in file:
                    if set(words) & set(row.lower().split()):
                        yield row.rstrip()
        except FileNotFoundError:
            yield "File not found"

    elif file_obj is not None:
        with file_obj as file:
            words = [word.lower() for word in words]
            for row in file:
                if set(words) & set(row.lower().split()):
                    yield row.rstrip()
