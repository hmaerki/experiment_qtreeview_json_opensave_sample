from typing import Any, List, Union
from PySide6 import QtCore


class Model(QtCore.QAbstractTableModel):
    def __init__(self, parent_=None):
        super(Model, self).__init__(parent_)
        self._parent_model_index = QtCore.QModelIndex()
        self.columns = ["ID", "Name"]
        self.rows = []

    def set_data(self, rows) -> None:
        self.beginInsertRows(self._parent_model_index, 0, len(rows) - 1)
        self.rows = rows
        self.endInsertRows()
        # self.layoutChanged.emit()

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.rows)

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.columns)

    def data(self, index: QtCore.QModelIndex, role: int) -> Any:
        if not index.isValid():
            return None
        if role == QtCore.Qt.EditRole or role == QtCore.Qt.DisplayRole:
            column_name = self.columns[index.column()]
            return self.rows[index.row()][column_name]
        return None
