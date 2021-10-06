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

from pathlib import Path
from datetime import datetime

from .parse_duplicate_ids import parse_for_multiple_ids
from .parser import Parser_jh, parse_jh

_DATA_POINTERS = ["^IMAGE", "^TABLE", "^SERIES", "^SPREADSHEET"]


def translate(file_: Path):
    iso_date = datetime.utcnow().strftime("%Y-%m-%d")

    generate = {
        "file_name": file_.stem,
        "current_date_utc": datetime.utcnow().strftime(
            "%Y-%m-%d"
        ),  # TODO: why not datetime.utcnow().isoformat()?
        "model_version": "1.11.0.0",  # TODO: where does this version come from?
    }
    # print(generate)
    with open(file_, "rb") as f:
        # parse_ids = ParseDuplicateIds()
        # duplicate_ids = parse_ids.parse(f)
        duplicate_ids = parse_for_multiple_ids(f)
        
        print(duplicate_ids)
        if duplicate_ids:
            parser = Parser_jh(duplicate_ids)
        else:
            parser = Parser_jh([])

        f.seek(0, 0) # reset file to beginning
        labels = parse_jh(f)


if __name__ == "__main__":
    test_file_base = "/srv/nfs_share_code/JPL/pds/data/_other_tools/pds-view/"
    test_files = [
        "test_data/ELE_MOM.LBL",
        "test_data/FF01.LBL",
        "test_data/FHA01118.LBL",
        "test_data/N1727539187_1.LBL",
        "test_data/BA03S183.IMG",
        "test_data/C000M5232T493378259EDR_F0000_0134M1.IMG",
        "test_data/FF01.IMG",
        "test_data/N1727539187_1.IMG",
        "test_data/ELE_MOM.TAB",
        "test_data/PDS4_ATM_TABLE_CHAR_MULTIPLE.TAB",
        "test_data/PDS4_ATM_TABLE_CHAR.TAB",
        "test_data/2d234493326edratf3d2537n0m1.dat",
        "test_data/PDS4_TABLE_DELIMITED.csv",
    ]

    # for tf in test_files:
    #     print(f"**{tf}")
    #     translate(Path(test_file_base, tf))

    # translate(Path(test_file_base, "test_data/FHA01118.LBL"))

    translate(Path(test_file_base, "test_data/ELE_MOM.LBL"))
