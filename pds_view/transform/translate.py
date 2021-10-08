# Copyright (c) 2021, California Institute of Technology ("Caltech").
# U.S. Government sponsorship acknowledged.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions must reproduce the above copyright notice, this list of
#   conditions and the following disclaimer in the documentation and/or other
#   materials provided with the distribution.
# * Neither the name of Caltech nor its operating division, the Jet Propulsion
#   Laboratory, nor the names of its contributors may be used to endorse or
#   promote products derived from this software without specific prior written
#   permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
import typing
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .parser import parse_pds3_lbl


__all__ = ["translate_to_pds4"]

_DATA_POINTERS = ["^IMAGE", "^TABLE", "^SERIES", "^SPREADSHEET"]
_JINJA_ENV = Environment(
    loader=FileSystemLoader(Path(__file__).parent.joinpath("templates", "j2")),
    autoescape=select_autoescape(),
)
_JINJA_TEMPLATE = _JINJA_ENV.get_template("0_base.xml.j2")
_IMG_DATA_TYPES = {
    ("MSB_INTEGER", "INTEGER", "SUN_INTEGER", "MAC_INTEGER"): {
        "8": "SignedByte",
        "16": "SignedMSB2",
        "32": "SignedMSB4",
    },
    (
        "MSB_UNSIGNED_INTEGER",
        "SUN_UNSIGNED_INTEGER",
        "MAC_UNSIGNED_INTEGER",
        "UNSIGNED_INTEGER",
    ): {
        "8": "UnsignedByte",
        "16": "UnsignedMSB2",
        "32": "UnsignedMSB4",
    },
    ("LSB_INTEGER", "PC_INTEGER", "VAX_INTEGER"): {
        "8": "SignedByte",
        "16": "SignedLSB2",
        "32": "SignedLSB4",
    },
    ("LSB_UNSIGNED_INTEGER", "PC_UNSIGNED_INTEGER", "VAX_UNSIGNED_INTEGER"): {
        "8": "UnsignedByte",
        "16": "UnsignedLSB2",
        "32": "UnsignedLSB4",
    },
    (
        "IEEE_REAL",
        "FLOAT",
        "REAL",
        "MAC_REAL",
        "SUN_REAL",
        "VAX_REAL",
        "VAXG_REAL",
        "VAX_DOUBLE",
    ): {
        "4": "IEEE754MSBSingle",
        "8": "IEEE754MSBDouble",
    },
    ("PC_REAL",): {
        "4": "IEEE754LSBSingle",
        "8": "IEEE754LSBDouble",
    },
    ("PC_COMPLEX",): {
        "1": "ComplexLSB8",
        "2": "ComplexLSB16",
    },
    ("VAX_COMPLEX", "VAXG_COMPLEX"): {
        "8": "ComplexMSB8",
        "16": "ComplexMSB16",
    },
    ("MSB_BIT_STRING", "LSB_BIT_STRING", "VAX_BIT_STRING"): defaultdict(
        lambda: "UnsignedBitString"
    ),
}
_TBL_DATA_TYPES = {
    (
        ("Field_Binary",),
        ("MSB_INTEGER", "INTEGER", "SUN_INTEGER", "MAC_INTEGER"),
    ): defaultdict(
        lambda: "Unknown",
        {
            "1": "SignedByte",
            "2": "SignedMSB2",
            "4": "SignedMSB4",
            "8": "SignedMSB8",
        },
    ),
    (
        ("Field_Binary",),
        (
            "MSB_UNSIGNED_INTEGER",
            "SUN_UNSIGNED_INTEGER",
            "MAC_UNSIGNED_INTEGER",
            "UNSIGNED_INTEGER",
        ),
    ): defaultdict(
        lambda: "Unknown",
        {
            "1": "UnsignedByte",
            "2": "UnsignedMSB2",
            "4": "UnsignedMSB4",
            "8": "UnsignedMSB8",
        },
    ),
    (("Field_Binary",), ("LSB_INTEGER", "PC_INTEGER", "VAX_INTEGER")): defaultdict(
        lambda: "Unknown",
        {
            "1": "SignedByte",
            "2": "SignedLSB2",
            "4": "SignedLSB4",
            "8": "SignedLSB8",
        },
    ),
    (
        ("Field_Binary",),
        ("LSB_UNSIGNED_INTEGER", "PC_UNSIGNED_INTEGER", "VAX_UNSIGNED_INTEGER"),
    ): defaultdict(
        lambda: "Unknown",
        {
            "1": "UnsignedByte",
            "2": "UnsignedLSB2",
            "4": "UnsignedLSB4",
            "8": "UnsignedLSB8",
        },
    ),
    (
        ("Field_Binary",),
        (
            "IEEE_REAL",
            "FLOAT",
            "REAL",
            "MAC_REAL",
            "SUN_REAL",
            "VAX_REAL",
            "VAXG_REAL",
            "VAX_DOUBLE",
        ),
    ): defaultdict(
        lambda: "Unknown",
        {
            "4": "IEEE754MSBSingle",
            "8": "IEEE754MSBDouble",
        },
    ),
    (("Field_Binary",), ("PC_REAL",)): defaultdict(
        lambda: "Unknown",
        {
            "4": "IEEE754LSBSingle",
            "8": "IEEE754LSBDouble",
        },
    ),
    (("Field_Binary",), ("PC_COMPLEX",)): defaultdict(
        lambda: "Unknown",
        {
            "1": "ComplexLSB8",
            "2": "ComplexLSB16",
        },
    ),
    (
        ("Field_Binary",),
        ("COMPLEX", "MAC_COMPLEX", "SUN_COMPLEX", "VAX_COMPLEX", "VAXG_COMPLEX"),
    ): defaultdict(
        lambda: "Unknown",
        {
            "1": "ComplexMSB8",
            "2": "ComplexMSB16",
        },
    ),
    (
        ("Field_Binary", "Field_Character"),
        (
            "MSB_BIT_STRING",
            "LSB_BIT_STRING",
            "VAX_BIT_STRING",
            "BCD",
            "BINARY_CODED_DECIMAL",
            "BINARY CODED DECIMAL",
        ),
    ): defaultdict(lambda: "SignedBitString"),
    (("Field_Binary", "Field_Character"), ("CHARACTER",)): defaultdict(
        lambda: "ASCII_String"
    ),
    (("Field_Binary", "Field_Character"), ("TIME", "DATE")): defaultdict(
        lambda: "ASCII_Date_Time_YMD_UTC"
    ),
    (("Field_Binary", "Field_Character"), ("BOOLEAN")): defaultdict(
        lambda: "UnsignedByte"
    ),
    (("Field_Character",), ("ASCII_REAL", "ASCII REAL")): defaultdict(
        lambda: "ASCII_Real"
    ),
    (("Field_Character",), ("ASCII_INTEGER", "ASCII INTEGER", "INTEGER")): defaultdict(
        lambda: "ASCII_Integer"
    ),
}


def translate_to_pds4(file_: Path):
    with open(file_, "rb") as f:
        labels = parse_pds3_lbl(f)

    _convert_to_pds4(file_, labels)
    # from pprint import pprint
    # pprint(labels)


def _represents_int(s: typing.Any) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False


## TODO: this is still a bit of a mess, look for opportunities to clean up
def _convert_to_pds4(file_: Path, labels: dict[str, typing.Union[str, dict]]):
    generate = {
        "file_name": file_.stem,
        "current_date_utc": datetime.utcnow().strftime(
            "%Y-%m-%d"
        ),  # TODO: why not datetime.utcnow().isoformat()?
        "model_version": "1.11.0.0",  # TODO: where does this version come from?
    }

    ptr_object_dict = defaultdict(list)
    ptr_offset_dict = defaultdict(list)
    record_bytes = int(next(v for (k, v) in labels.items() if k == "RECORD_BYTES"))
    keys = list(labels.keys())
    for key in keys:
        # TODO: does this ever show up outside of key[0]
        if "^" == key[0]:
            pointer_fname = file_.name
            associated_object = key.split("_")[-1].replace("^", "")
            if labels[key][0] == "(" and labels[key][-1] == ")":
                labels[key] = labels[key][1:-1]
            if "_" in key:
                ptr_key = f"^{key.split('_')[-1]}"
            else:
                ptr_key = key

            labels[key] = labels[key].replace('"', "").replace("'", "")

            if ptr_key in _DATA_POINTERS:
                split_lbl = labels[key].split(",")
                if "<BYTES>" in labels[key]:
                    if len(split_lbl) == 1:
                        labels[key] = f"{pointer_fname},{labels[key]}"
                    else:
                        pointer_fname = split_lbl[0]
                else:
                    if len(split_lbl) == 1:
                        if _represents_int(labels[key]):
                            bytes_ = record_bytes * (int(labels[key]) - 1)
                            labels[key] = f"{file_},{bytes_}<BYTES>"
                        else:
                            pointer_fname = labels[key]
                            labels[key] = f"{labels[key]},0<BYTES>"
                    elif len(split_lbl) == 2:
                        bytes_ = record_bytes * (int(split_lbl[1]) - 1)
                        pointer_fname = split_lbl[0]
                        labels[key] = f"{split_lbl[0]},{bytes_}<BYTES>"
                    else:
                        print("some kind of error")

                offset = labels[key].split(",")[1].split("<")[0]
            new_key = key.replace("^", "PTR_")
            object_type = f'{new_key.split("_")[-1]}_0'
            if "HEADER" in object_type:
                continue
            labels[new_key] = labels.pop(key)
            # this replaces the add_to_file_dict method
            ptr_object_dict[pointer_fname].append(associated_object)
            ptr_offset_dict[pointer_fname].append(int(offset))

    # todo: see if this needs to be cleaned up in favor
    # of less logic in the templates
    map_ = {
        "label": labels,
        "generate": generate,
        "ptr_object_map": ptr_object_dict,
        "ptr_offset_map": ptr_offset_dict,
        "object_placeholder": object_type,
        "tbl_data_types": _TBL_DATA_TYPES,
        "img_data_types": _IMG_DATA_TYPES,
    }
    # TODO: write file here
    print(_JINJA_TEMPLATE.render(**map_))
    # from pprint import pprint
    # pprint(labels)


if __name__ == "__main__":
    cwd = Path(__file__).parent
    test_file_base = cwd.joinpath("..","..")
    test_files = [
        # "test_data/ELE_MOM.LBL",
        "test_data/FF01.LBL",
        # "test_data/FHA01118.LBL",
        # "test_data/N1727539187_1.LBL", # todo, why this think it's a table
        # "test_data/BA03S183.IMG",
        # "test_data/C000M5232T493378259EDR_F0000_0134M1.IMG",
        # "test_data/FF01.IMG",
        # "test_data/N1727539187_1.IMG",
        # "test_data/ELE_MOM.TAB",
        # "test_data/PDS4_ATM_TABLE_CHAR_MULTIPLE.TAB",
        # "test_data/PDS4_ATM_TABLE_CHAR.TAB",
        # "test_data/2d234493326edratf3d2537n0m1.dat",
        # "test_data/PDS4_TABLE_DELIMITED.csv",
    ]

    for tf in test_files:
        print(f"^^^^^^^^^{tf}")
        translate_to_pds4(Path(test_file_base, tf))
