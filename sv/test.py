from typing import Any, Union
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from facets import facets, RAW_BYTES, NUMBER, STRING

from params import Params

DELIMITER = "\x00"


def encoder(
    item: Union[
        bytes,
        int,
        str,
    ]
):
    if isinstance(item, str):
        return item
    if isinstance(item, int):
        return str(item)
    if isinstance(item, bytes):
        return item.decode()
    raise Exception("Invalid instance")


def decoder(item: str, type):
    if type == str:
        return item
    if type == int:
        return int(item)
    if type == bytes:
        return item.encode()
    raise Exception("Invalid instance")


if __name__ == "__main__":

    print(f"Separated Value example")
    print(f"Size\tParams")

    for facet in facets:
        NUMBER_VALUE: int = facet[NUMBER]
        STRING_VALUE: str = facet[STRING]
        RAW_BYTES_VALUE: bytes = facet[RAW_BYTES]

        # Create
        obj_for_serializing: Params = Params.new(
            NUMBER_VALUE,
            STRING_VALUE,
            RAW_BYTES_VALUE,
        )

        # Serialize FIELDS
        serialized_fields = DELIMITER.join(
            [encoder(i) for i in obj_for_serializing.fields_values()]
        )

        # Deserialize FIELDS
        deserialized_fields = serialized_fields.split(DELIMITER)
        deserialized_object: Params = Params.new(
            number=decoder(deserialized_fields[0], int),
            string=decoder(deserialized_fields[1], str),
            raw_bytes=decoder(deserialized_fields[2], bytes),
        )

        # Check.
        assert deserialized_object.number == NUMBER_VALUE
        assert deserialized_object.string == STRING_VALUE
        assert deserialized_object.raw_bytes == RAW_BYTES_VALUE

        # Report
        print(f"{len(serialized_fields)}\t{facet}")
