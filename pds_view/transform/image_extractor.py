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
import hashlib
import typing
from pathlib import Path

from .parser import parse_pds3_lbl

_SUPPORTED = {
    "RECORD_TYPE": "FIXED_LENGTH",
    "SAMPLE_BITS": ("8", "16"),
    "SAMPLE_TYPE": (
        "UNSIGNED_INTEGER",
        "MSB_UNSIGNED_INTEGER",
        "LSB_INTEGER",
        "MSB_INTEGER",
    ),
}


def _is_supported(labels: dict[str, typing.Union[dict, str]]) -> bool:
    return (
        "IMAGE" in labels
        and labels["RECORD_TYPE"] == _SUPPORTED["RECORD_TYPE"]
        and labels["IMAGE"]["SAMPLE_BITS"] in _SUPPORTED["SAMPLE_BITS"]
        and labels["IMAGE"]["SAMPLE_TYPE"] in _SUPPORTED["SAMPLE_TYPE"]
    )


def _get_image_dimensions(
    labels: dict[str, typing.Union[dict, str]]
) -> tuple[str, str]:
    # (width, height)
    return (labels["IMAGE"]["LINES"], labels["IMAGE"]["LINE_SAMPLES"])


def _get_image_location(labels: dict[str, typing.Union[dict, str]]) -> int:
    image_pointer = labels["^IMAGE"].replace("(","").replace(")","").split(",")[-1].split()
    if len(image_pointer) == 1:
        return (int(image_pointer[0]) - 1) * int(labels["RECORD_BYTES"])
    elif len(image_pointer) == 2:
        units = image_pointer[1]
        if not units == "<BYTES>":
            errorMessage = ("Expected <BYTES> image pointer units but found %s") % (
                units
            )
            raise ValueError(errorMessage)
        return int(image_pointer[0])
    else:
        errorMessage = ("^IMAGE contains extra information") % (image_pointer[2:])
        raise ValueError(errorMessage)


def _get_image_checksum(
    labels: dict[str, typing.Union[dict, str]]
) -> typing.Optional[str]:
    try:
        return labels["IMAGE"]["MD5_CHECKSUM"][1:-1]
    except (KeyError, IndexError):
        return None


def extract(file_: Path):
    with open(file_, "rb") as f:
        labels = parse_pds3_lbl(f)
        
    if _is_supported(labels):
        # from pprint import pprint
        # pprint(labels)
        dim = _get_image_dimensions(labels)
        loc = _get_image_location(labels)
        image_sample_bits = int(labels["IMAGE"]["SAMPLE_BITS"])
        image_sample_type = labels["IMAGE"]["SAMPLE_TYPE"]
        md5_checksum = _get_image_checksum(labels)
        print(loc)
        # with open()
        # f.seek(loc)
            # if md5_checksum:


if __name__ == "__main__":
    cwd = Path(__file__).parent
    test_file_base = cwd.joinpath("..", "..")
    test_files = [
        # "test_data/ELE_MOM.LBL",
        "test_data/FF01.LBL",
        "test_data/FHA01118.LBL",
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
        extract(Path(test_file_base, tf))
