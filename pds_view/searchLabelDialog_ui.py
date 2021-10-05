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

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'searchLabelDialog.ui'
#
# Created by: PyQt4 UI code generator 4.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

# try:
#     _fromUtf8 = QtCore.QString.fromUtf8
# except AttributeError:
#     def _fromUtf8(s):
#         return s


class Ui_SearchLabelDialog(object):
    def setupUi(self, SearchLabelDialog: QtWidgets.QDialog):
        SearchLabelDialog.setObjectName("SearchLabelDialog")
        SearchLabelDialog.setWindowModality(QtCore.Qt.NonModal)
        SearchLabelDialog.resize(649, 519)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(SearchLabelDialog.sizePolicy().hasHeightForWidth())
        SearchLabelDialog.setSizePolicy(sizePolicy)
        SearchLabelDialog.setMaximumSize(QtCore.QSize(10000, 10000))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        SearchLabelDialog.setFont(font)
        SearchLabelDialog.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        SearchLabelDialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(SearchLabelDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontal_line_top = QtWidgets.QFrame(SearchLabelDialog)
        self.horizontal_line_top.setFrameShape(QtWidgets.QFrame.HLine)
        self.horizontal_line_top.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontal_line_top.setObjectName("horizontal_line_top")
        self.gridLayout.addWidget(self.horizontal_line_top, 7, 0, 1, 3)
        self.value_label = QtWidgets.QLabel(SearchLabelDialog)
        self.value_label.setObjectName("value_label")
        self.gridLayout.addWidget(self.value_label, 1, 0, 1, 1)
        self.value_line_edit = QtWidgets.QLineEdit(SearchLabelDialog)
        font = QtGui.QFont()
        font.setItalic(False)
        self.value_line_edit.setFont(font)
        self.value_line_edit.setToolTip("")
        self.value_line_edit.setObjectName("value_line_edit")
        self.gridLayout.addWidget(self.value_line_edit, 3, 0, 1, 2)
        self.results_label = QtWidgets.QLabel(SearchLabelDialog)
        self.results_label.setObjectName("results_label")
        self.gridLayout.addWidget(self.results_label, 8, 0, 1, 1)
        self.search_button = QtWidgets.QPushButton(SearchLabelDialog)
        self.search_button.setObjectName("search_button")
        self.gridLayout.addWidget(self.search_button, 20, 2, 1, 1)
        self.cancel_button = QtWidgets.QPushButton(SearchLabelDialog)
        self.cancel_button.setObjectName("cancel_button")
        self.gridLayout.addWidget(self.cancel_button, 20, 1, 1, 1)
        self.results_textEdit = QtWidgets.QTextEdit(SearchLabelDialog)
        self.results_textEdit.setObjectName("results_textEdit")
        self.gridLayout.addWidget(self.results_textEdit, 17, 0, 1, 3)
        self.line_2 = QtWidgets.QFrame(SearchLabelDialog)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 18, 0, 1, 3)
        self.case_sensitive_check_box = QtWidgets.QCheckBox(SearchLabelDialog)
        self.case_sensitive_check_box.setChecked(True)
        self.case_sensitive_check_box.setObjectName("case_sensitive_check_box")
        self.gridLayout.addWidget(self.case_sensitive_check_box, 3, 2, 1, 1)

        self.retranslateUi(SearchLabelDialog)
        QtCore.QMetaObject.connectSlotsByName(SearchLabelDialog)

    def retranslateUi(self, SearchLabelDialog: QtWidgets.QDialog):
        # TODO: text translation
        # translator = QtCore.QTranslator(SearchLabelDialog)
        # SearchLabelDialog.setWindowTitle(translator.translate("SearchLabelDialog", "Find Text in Currently Selected Label", None))
        SearchLabelDialog.setWindowTitle("Find Text in Currently Selected Label")
        # self.value_label.setText(translator.translate("SearchLabelDialog", "Search for:", None))
        self.value_label.setText("Search for:")
        # self.results_label.setText(translator.translate("SearchLabelDialog", "Results", None))
        self.results_label.setText("Results")
        # self.search_button.setText(translator.translate("SearchLabelDialog", "Search", None))
        self.search_button.setText("Search")
        # self.cancel_button.setText(translator.translate("SearchLabelDialog", "Done", None))
        self.cancel_button.setText("Done")
        # self.case_sensitive_check_box.setText(translator.translate("SearchLabelDialog", "  Case Sensitive", None))
        self.case_sensitive_check_box.setText("  Case Sensitive")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    SearchLabelDialog = QtWidgets.QDialog()
    ui = Ui_SearchLabelDialog()
    ui.setupUi(SearchLabelDialog)
    SearchLabelDialog.show()
    sys.exit(app.exec_())
