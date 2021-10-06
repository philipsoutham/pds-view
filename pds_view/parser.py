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
from collections import deque

from .reader import read_pds3_header

_CONTAINERS = {"OBJECT": "END_OBJECT", "GROUP": "END_GROUP"}
_CONTAINERS_START = list(_CONTAINERS.keys())
_CONTAINERS_END = list(_CONTAINERS.values())


class _ParserNode:
    """A tree-like node structure to maintain structure within PDS labels."""

    def __init__(self, children:dict=None, parent: "_ParserNode"=None):
        if not children:
            children = {}

        self.children = children
        self.parent = parent


class Parser_jh:
    class _ParserNode:
        """A tree-like node structure to maintain structure within PDS labels."""

        def __init__(self, children=None, parent=None):
            if not children:
                children = {}

            self.children = children
            self.parent = parent

    def __init__(self, duplicate_ids: list[str]) -> None:
        super().__init__()

    def parse(self, data: typing.BinaryIO):
        self._parse_header(data)

    def _parse_header(self, data: typing.BinaryIO):
        root = self._ParserNode()
        current_node = root
        expected_end_queue = []
        columns = []


def parse_jh(data: typing.BinaryIO, dup_ids=None):
    root = _ParserNode()
    current_node = root
    expected_end_queue = deque()
    columns = []

    for (k, v) in map(lambda x: (x[0].strip(), x[1].strip()), read_pds3_header(data)):
        if k in _CONTAINERS_START:
            expected_end_queue.append((_CONTAINERS[k], v))
            current_node =  _ParserNode({}, current_node)
        elif k in _CONTAINERS_END:
            try:
                expected_end_queue.pop()
                new_parent = current_node.parent
                new_parent.children[v] = current_node.children
                if dup_ids and v in dup_ids:
                    holder = dict(new_parent.children[v])
                    columns.append(holder)
                current_node = new_parent
            except IndexError:
                assert current_node.parent is None, "Parent node is not None."
        else:
            assert not k.startswith('END_'), f"Detected a possible uncaught nesting {k}"
            current_node.children[k] = v
    assert not expected_end_queue, f"Detected hanging chads, very gory...{expected_end_queue}"

    assert current_node.parent is None, 'Parent is not None, did not make it back up the tree'
    
    print(root.children["TABLE"])

    # if 'TABLE'

