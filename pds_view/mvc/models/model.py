import typing

import pandas as pd
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, QObject, Qt
from PyQt5.QtWidgets import QPushButton

__all__ = ["TableModel", "SummaryTableModel"]


class TableModel(QAbstractTableModel):
    def __init__(
        self, data: pd.DataFrame, parent: typing.Optional[QObject] = None
    ) -> None:
        super().__init__(parent=parent)
        self._data = data

    def rowCount(self, parent: typing.Optional[QObject] = None) -> int:
        return self._data.shape[0]

    def columnCount(self, parent: typing.Optional[QObject] = None) -> int:
        return self._data.shape[1]

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: int = ...
    ) -> typing.Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[section]
        return None

    def to_csv(self, fname: str) -> None:
        self._data.to_csv(fname, index=False, header=True)


class SummaryTableModel(TableModel):
    def __init__(
        self, data: pd.DataFrame, parent: typing.Optional[QObject] = None
    ) -> None:
        super().__init__(data=data, parent=parent)

    def columnCount(self, parent: typing.Optional[QObject] = None) -> int:
        return super().columnCount(parent) + 1

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        try:
            return super().data(index, role)
        except IndexError:
            return "VIEW"

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: int = None
    ) -> typing.Any:
        try:
            return super().headerData(section, orientation, role)
        except IndexError:
            return "Select"
