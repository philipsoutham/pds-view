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
import itertools
import typing
import re

_comment_start = re.compile(br"/\*")
_comment_end = re.compile(br"(.)+\*/")
_magic_record_finding_token = "="


def read_pds3_header(data: typing.BinaryIO):
    def _line_filter(line: bytes) -> list[bytes]:
        if not line or line == b"END":
            return []
        elif _comment_start.match(line):
            if not _comment_end.match(line):
                print(
                    "Detected possible multiline comment near line %s" % line.decode()
                )
        else:
            return [t for t in line.split() if t]

        return []

    tokens: list[bytes] = list(map(lambda x: x.decode(),
        itertools.chain.from_iterable(map(_line_filter, map(lambda x: x.strip(), data)))
    ))

    record_indicies = [
        i for (i, t) in enumerate(tokens) if t == _magic_record_finding_token
    ]
    # print('Found %d possible key, value pairs' % (len(record_indicies)))

    for (i, rec_idx) in enumerate(record_indicies):
        key_idx = rec_idx - 1
        data_start_idx = rec_idx + 1
        try:
            data_end_idx = record_indicies[i + 1] - 1
        except IndexError:
            errorMessage = "i: %d, Number of tokens: %d" % (i, len(tokens))
            assert i == (len(record_indicies) - 1), errorMessage
            data_end_idx = len(tokens) - 1
        finally:
            if data_start_idx == data_end_idx:
                yield tokens[key_idx], " ".join(tokens[data_start_idx:])
                break
            yield tokens[key_idx], " ".join(tokens[data_start_idx:data_end_idx])
