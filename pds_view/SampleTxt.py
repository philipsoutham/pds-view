import typing
import dataclasses
from pds4_tools.reader import pds4_read
from pds4_tools.reader.general_objects import Structure


# class StructureSummary(typing.NamedTuple):
#     id: str
#     type: str
#     is_header: bool
#     dimensions: str


# class ItemSummary(typing.NamedTuple):
#     title: str
#     structure_summary: list[StructureSummary]


@dataclasses.dataclass(frozen=True)
class StructureSummary:
    id: str
    type: str
    is_header: bool
    dimensions: str


@dataclasses.dataclass(frozen=True)
class ItemSummary:
    title: str
    structure_summary: list[StructureSummary]


def get_item_summary(fname: str) -> ItemSummary:
    structure_list = pds4_read(fname, lazy_load=True, decode_strings=False, quiet=True)

    title = "{}{}".format(
        "Data Structure Summary" if len(structure_list) > 0 else "Label",
        "" if (fname is None) else " for '{0}'".format(fname),
    )

    def _get_dimension_text(s: Structure) -> str:
        if s.is_header():
            return "---"
        dimensions: list[int] = s.meta_data.dimensions()
        if s.is_table():
            return "{0} cols X {1} rows".format(dimensions[0], dimensions[1])
        if s.is_array():
            return " X ".join(str(dim) for dim in dimensions)
        return "no dimensions found"

    return ItemSummary(
        title=title,
        structure_summary=[
            StructureSummary(
                id=s.id,
                is_header=s.is_header(),
                type=s.type,
                dimensions=_get_dimension_text(s),
            )
            for s in structure_list
        ],
    )


if __name__ == "__main__":
    xml_files = [
        "/home/psoutham/src/JPL/data/_other_tools/transform-1.5.0/examples/20140804T205944Z_MAP_bias_V001.xml",
        "/home/psoutham/src/JPL/data/_other_tools/transform-1.5.0/examples/b0090_p243401_01_01v02.xml",
        "/home/psoutham/src/JPL/data/_other_tools/transform-1.5.0/examples/C000M5232T493378259EDR_F0000_0134M1.xml",
        "/home/psoutham/src/JPL/data/_other_tools/transform-1.5.0/examples/i943630r.xml",
        "/home/psoutham/src/JPL/data/_other_tools/transform-1.5.0/examples/Product_Table_Binary.xml",
        "/home/psoutham/src/JPL/data/_other_tools/transform-1.5.0/examples/Product_Table_Character.xml",
        "/home/psoutham/src/JPL/data/_other_tools/transform-1.5.0/examples/Product_Table_Delimited.xml",
        "/home/psoutham/src/JPL/data/_other_tools/transform-1.5.0/examples/Product_Table_Multiple_Datafiles.xml",
        "/home/psoutham/src/JPL/data/_other_tools/transform-1.5.0/examples/Product_Table_Multiple_Tables.xml",
    ]
    for f in xml_files:
        print(get_item_summary(f))
    
    print(dataclasses.asdict(get_item_summary(xml_files[2])))
