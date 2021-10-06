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

from airspeed import CachingFileLoader

from pds_view import resource_path

from .parse_duplicate_ids import parse_for_multiple_ids
from .parser import parse_jh

_DATA_POINTERS = ["^IMAGE", "^TABLE", "^SERIES", "^SPREADSHEET"]


def translate(file_: Path):
    iso_date = datetime.utcnow().strftime("%Y-%m-%d")

    with open(file_, "rb") as f:
        duplicate_ids = parse_for_multiple_ids(f) or []
        f.seek(0, 0)  # reset file to beginning
        labels = parse_jh(f, dup_ids=duplicate_ids)

    # debug
    _convert_to_pds4(file_, labels)


def _represents_int(s: typing.Any) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False


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
        if "^" in key:
            pointer_fname = str(file_)
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

    loader = CachingFileLoader(resource_path("./templates"))
    template = loader.load_template("inspectTemplate.vm")
    map_ = {
        "label": labels,
        "str": str,
        "generate": generate,
        "ptr_object_map": dict(ptr_object_dict),
        "ptr_offset_map": dict(ptr_offset_dict),
        "object_placeholder": object_type,
    }
    from pprint import pprint
    pprint(map_)
    # out = template.merge(map_, loader=loader)
    # print(out)


if __name__ == "__main__":
    test_file_base = "/home/psoutham/src/JPL/data/_other_tools/pds-view"
    # test_file_base = "/srv/nfs_share_code/JPL/pds/data/_other_tools/pds-view/"
    test_files = [
        "test_data/ELE_MOM.LBL",
        # "test_data/FF01.LBL",
        # "test_data/FHA01118.LBL",
        # "test_data/N1727539187_1.LBL",

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
        translate(Path(test_file_base, tf))

    # translate(Path(test_file_base, "test_data/FHA01118.LBL"))

    # translate(Path(test_file_base, "test_data/FF01.LBL"))
