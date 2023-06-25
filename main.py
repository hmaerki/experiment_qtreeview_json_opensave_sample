import json
import sys
from mainwindow import Ui_MainWindow
import treeview
import tableview
from PySide6 import QtWidgets, QtCore


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model = treeview.Model(self)

        self.ui.treeView.setModel(self.model)
        self.ui.treeView.setItemDelegate(treeview.Delegate())
        self.ui.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.treeView.customContextMenuRequested.connect(self.contextMenu)

        self.ui.actionAddChild.triggered.connect(self.add_child)
        self.ui.actionDelete.triggered.connect(self.delete_item)
        self.ui.actionOpen.triggered.connect(self.open_json)
        self.ui.actionSave.triggered.connect(self.save_json)

        self.open_json(filename="data.json")

        self.table_model = tableview.Model(self)

        self.ui.tableView.setModel(self.table_model)
        self.ui.actionOpenTable.triggered.connect(self.open_view_json)

        self.open_view_json(filename="data_table.json")

    def open_json(self, filename):
        def recursion(_part, _parent, _parts):
            d = {key: _part[key] for key in _part if not "parts" == key}
            parent_index = self.model.addItem(d, _parent)
            if "parts" in _part:
                for child in _part["parts"]:
                    recursion(child, parent_index, parts)

        if filename is None:
            filename = QtWidgets.QFileDialog.getOpenFileName(
                self, "Save file", "", "JSON File (*.json)"
            )
            if not filename[0]:
                return
            filename = filename[0]

        json_data = json.load(open(filename))
        self.model.removeAllItems()
        self.model.removeAllColumns()
        self.model.addColumns(json_data["columns"])
        parts = json_data["parts"]
        for part in parts:
            recursion(part, QtCore.QModelIndex(), parts)

    def save_json(self):
        def recursion(parent):
            _dict1 = parent.dict
            if parent.hasChildren():
                _dict1["parts"] = [recursion(child) for child in parent.children]
            return _dict1

        parts = []
        for child in self.model.root_item.children:
            parts.append(recursion(child))

        parts = {"columns": self.model.columns, "parts": parts}

        filename = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save file", "", "JSON File (*.json)"
        )
        if filename[0]:
            json.dump(parts, open(filename[0], "w"), indent=4)

    def contextMenu(self, point):
        self.menu = QtWidgets.QMenu(self)
        self.menu.addAction("Add child", self.add_child)
        self.menu.addAction("Delete", self.delete_item)
        self.menu.exec_(self.focusWidget().mapToGlobal(point))

    def add_child(self):
        indexes = self.ui.treeView.selectedIndexes()

        if len(indexes) == 0:
            self.model.addItem()
            return

        indexes2 = []
        for index in indexes:
            if not index.row() in [
                i.row() for i in indexes2 if i.parent() == index.parent()
            ]:
                indexes2.append(index)

        for index in indexes2:
            self.model.addItem({}, index)

    def delete_item(self):
        indexes = self.ui.treeView.selectedIndexes()

        if len(indexes) == 0:
            return

        indexes2 = []
        for index in indexes:
            if not index.row() in [
                i.row() for i in indexes2 if i.parent() == index.parent()
            ]:
                indexes2.append(index)

        for index in indexes2:
            self.model.removeItem(index)

    def open_view_json(self, filename):
        if filename is None:
            filename = QtWidgets.QFileDialog.getOpenFileName(
                self, "Save file", "", "JSON File (*.json)"
            )
            if not filename[0]:
                return
            filename = filename[0]

        json_data = json.load(open(filename))
        # self.table_model.removeAllItems()
        # self.table_model.removeAllColumns()
        # self.table_model.set_columns(columns=json_data["columns"])

        parts = json_data["parts"]

        self.table_model.set_data(rows=parts)
        # for part in parts:
        #     # d = { key:part[key] for key in part if not 'parts' == key }
        #     self.table_model.addItem(part)
        # self.table_model.resetInternalData()
        # self.table_model.layoutChanged()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(app)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
