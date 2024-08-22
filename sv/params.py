from typing import Union


class Params:
    number: Union[int, None] = None
    string: Union[str, None] = None
    raw_bytes: Union[bytes, None] = None

    def __init__(
        self,
        number: Union[int, None] = None,
        string: Union[str, None] = None,
        raw_bytes: Union[bytes, None] = None,
    ):
        self.number = number
        self.string = string
        self.raw_bytes = raw_bytes

    def __str__(self) -> str:
        return str(f"{self.number}, {self.number}, {self.raw_bytes}")
