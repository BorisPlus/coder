import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import pickle


from facets import facets, RAW_BYTES, NUMBER, STRING
from sv.params import Params


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
        serialized_object = pickle.dumps(
            obj_for_serializing,
            protocol=3,
            fix_imports=False,
        )

        # Deserialize
        deserialized_object: Params = pickle.loads(serialized_object)

        # Check.
        assert deserialized_object.number == NUMBER_VALUE
        assert deserialized_object.string == STRING_VALUE
        assert deserialized_object.raw_bytes == RAW_BYTES_VALUE

        # Report
        print(f"{len(serialized_object)}\t{facet}")
