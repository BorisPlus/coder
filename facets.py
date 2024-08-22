NUMBER = "number"
STRING = "string"
RAW_BYTES = "bytes"

facets = [
    {NUMBER: 1, STRING: r"", RAW_BYTES: b""},
    {NUMBER: 1, STRING: r"t", RAW_BYTES: b"b"},
    {NUMBER: 1, STRING: r"text_0123456", RAW_BYTES: b"bytes_0"},
    {NUMBER: 10, STRING: r"text_0123456", RAW_BYTES: b"bytes_0"},
    {NUMBER: 10, STRING: r"text_0123456", RAW_BYTES: b"bytes_01"},
    {NUMBER: 10, STRING: r"text_01234567", RAW_BYTES: b"bytes_01"},
    {NUMBER: 17, STRING: r"text_0123456", RAW_BYTES: b"bytes_01"},
    {NUMBER: 1000000000, STRING: r"text_0123456789", RAW_BYTES: b"bytes_0123456789"},
]
