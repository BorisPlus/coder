class Params:
    number: int
    string: str
    raw_bytes: bytes

    __slots__ = ("number","string",  "raw_bytes")

    @classmethod
    def new(cls, number: int, string: str, raw_bytes: bytes):
        return cls( number, string, raw_bytes)

    def __init__(self, number: int, string: str, raw_bytes: bytes):
        self.number = number
        self.string = string
        self.raw_bytes = raw_bytes

    def fields_values(self) -> tuple:
        return tuple(getattr(self, x) for x in self.__slots__)

    def __str__(self) -> str:
        return str(self.fields_values())
