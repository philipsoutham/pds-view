# Copyright (c) 2019, California Institute of Technology ("Caltech").
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

import sys

from PyQt5 import QtWidgets, QtCore, QtGui

from . import searchLabelDialog_ui

# TODO: why
MAC = sys.platform.startswith("darwin")
# try:
#     from PyQt4.QtGui import qt_mac_set_native_menubar
# except ImportError:
#     MAC = False


class SearchLabelDialog(QtWidgets.QDialog, searchLabelDialog_ui.Ui_SearchLabelDialog):
    def __init__(self, label_dict, label_widget, parent=None):
        super(SearchLabelDialog, self).__init__(parent)
        self.setupUi(self)

        self.search_dict = label_dict

        self.lw = label_widget

        dict = self.lw.get_parent_child_dict
        # print(dict)

        self.matches = []
        self.value = ""

        # Callbacks for buttons clicked
        self.cancel_button.clicked.connect(self.reject)
        self.search_button.clicked.connect(self.handle_search_clicked)

        # print('instantiated label dialog')

    @QtCore.pyqtSlot()
    def handle_search_clicked(self):
        # decide if it is a single value search or a range search
        if self.value_line_edit.text() == "":
            results = "Nothing entered."
            QtWidgets.QMessageBox.information(
                self, "Enter a value to search for", results
            )
            return
        else:
            self.handle_search()
            return

    @QtCore.pyqtSlot()
    def handle_search(self):
        self.value = self.value_line_edit.text()
        case_sensitive = True
        find = str(self.value)
        num_found = 0
        found = []
        matches = []
        # test case sensitive checkbox.
        if not self.case_sensitive_check_box.isChecked():
            case_sensitive = False
        # find matches of sting entered.
        for key in self.search_dict:
            label_heading = self.search_dict[key][0]

            for i in self.search_dict[key]:
                if case_sensitive:
                    if find in i:
                        num_found += 1
                        matches.append(i)
                else:
                    if find.lower() in i.lower():
                        num_found += 1
                        matches.append(i)

            if matches:
                # insert label_heading at front of list
                matches.insert(0, label_heading)
                # use 'list of lists' data structure
                found.append(matches)
                # get ready for next round
                matches = []

        # print('Found: {} matches'.format(num_found))
        # Test for match in label heading, if there remove the duplicate entry
        for i in found:
            if i[0] == i[1]:
                i.pop(0)
        # print(found)

        self.display_search_results(num_found, found)
        self.value_line_edit.clear()

    def display_search_results(self, num_found, found):
        # print('display search results')
        self.results_textEdit.clear()
        if found:
            results = 'Found %d matches for value "%s".' % (num_found, str(self.value))
            self.results_textEdit.insertPlainText(results + "\n")
            for i in found:
                heading = i[0]
                self.results_textEdit.setTextColor(QtGui.QColor(150, 25, 0))
                self.results_textEdit.insertPlainText(heading + "\n")
                for j in range(len(i) - 1):
                    if (
                        j == heading
                    ):  # the match was in the heading so don't print it as another match
                        continue
                    self.results_textEdit.setTextColor(QtGui.QColor(0, 25, 150))
                    self.results_textEdit.insertPlainText("    " + i[j + 1] + "\n")
                self.results_textEdit.setTextColor(QtGui.QColor(0, 0, 0))

                # Write results to the textEdit widget

        else:
            results = 'No matches found for: "%s".' % str(self.value)
            QtWidgets.QMessageBox.information(self, "Search Results", results)
