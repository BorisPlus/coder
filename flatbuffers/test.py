import os
import sys


import flatbuffers


from params.Params import (
    Params,
    ParamsStart,
    ParamsEnd,
    ParamsAddNumber,
    ParamsAddString,
    ParamsAddRawBytes,
)


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from facets import facets, NUMBER, STRING, RAW_BYTES


if __name__ == "__main__":

    print(f"FlatBuffers example")
    print(f"Size\tParams")

    for facet in facets:

        # Create
        builder = flatbuffers.Builder(0)
        flat_buffered_string = builder.CreateString(facet[STRING])
        flat_buffered_bytes = builder.CreateByteVector(facet[RAW_BYTES])
        ParamsStart(builder)
        ParamsAddString(builder, flat_buffered_string)
        ParamsAddNumber(builder, facet[NUMBER])
        ParamsAddRawBytes(builder, flat_buffered_bytes)
        flat_buffered_object = ParamsEnd(builder)
        builder.Finish(flat_buffered_object)

        # Serialize
        # We now have a FlatBuffer that we could store on disk or send over a network.
        buffer = builder.Output()

        # Deserialize
        params = Params.GetRootAsParams(buffer, 0)

        # Check.
        assert params.Number() == facet[NUMBER]
        assert params.String() == facet[STRING].encode()
        assert params.RawBytesLength() == len(facet[RAW_BYTES])
        assert b"".join(params.RawBytesAsNumpy()) == facet[RAW_BYTES]

        # Report
        print(f"{len(buffer)}\t{facet}")
