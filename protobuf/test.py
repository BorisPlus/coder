import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import params_pb2


from facets import facets, NUMBER, STRING, RAW_BYTES


if __name__ == "__main__":

    params = params_pb2.Params()

    print(f"ProtoBuf example")
    print(f"Size\tParams")

    for facet in facets:
        params.number = facet.get(NUMBER)
        params.string = facet.get(STRING)
        params.raw_bytes = facet.get(RAW_BYTES)

        # Serialize
        buffer = params.SerializeToString()

        # Deserialize
        deserialized_object = params_pb2.Params()
        deserialized_object.ParseFromString(buffer)

        # Check.
        assert deserialized_object.number == facet.get(NUMBER)
        assert deserialized_object.string == facet.get(STRING)
        assert deserialized_object.raw_bytes == facet.get(RAW_BYTES)

        # Report
        print(f"{len(buffer)}\t{facet}")
