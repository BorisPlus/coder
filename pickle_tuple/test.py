import os
import pickle
import sys


from params import Params

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from facets import facets, RAW_BYTES, NUMBER, STRING


if __name__ == "__main__":

    print(f"Pickle example")
    print(f"Size\tParams")

    for facet in facets:
        NUMBER_VALUE: int = facet[NUMBER]
        STRING_VALUE: str = facet[STRING]
        RAW_BYTES_VALUE: bytes = facet[RAW_BYTES]

        # Create
        obj_for_serializing: Params = Params(
            number=NUMBER_VALUE,
            string=STRING_VALUE,
            raw_bytes=RAW_BYTES_VALUE,
        )

        # Serialize
        serialized_fields = pickle.dumps(
            obj_for_serializing.fields_for_object_serialization(),
            protocol=3,
            fix_imports=False,
        )

        # Deserialize
        deserialized_fields = pickle.loads(serialized_fields)
        deserialized_object: Params = Params.deserialization_object_from_fields(
            deserialized_fields
        )

        # Check.
        assert deserialized_object.number == NUMBER_VALUE
        assert deserialized_object.string == STRING_VALUE
        assert deserialized_object.raw_bytes == RAW_BYTES_VALUE

        # Report
        print(f"{len(serialized_fields)}\t{facet}")
