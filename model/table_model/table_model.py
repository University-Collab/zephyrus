from PySide2.QtCore import QAbstractTableModel
from PySide2 import QtCore


class TableModel(QAbstractTableModel):
    def __init__(self, handler_reference, parent=None):
        super().__init__(parent)
        self.handler_reference = handler_reference
        self.d = self.handler_reference.data
        self.metadata = self.handler_reference.meta_data
        self.is_parent_table = self.handler_reference.is_parent_table

    # helper method
    def get_element(self, index):
        return self.d[index.row()]

    def rowCount(self, index):
        return len(self.d)

    def columnCount(self, index):
        if self.is_parent_table == True:
            return len(self.metadata["columns"])
        else:
            return len(self.metadata["subtable columns"])

    def data(self, index, role=QtCore.Qt.DisplayRole):
        # TODO: dodati obradu uloga (role)
        data = self.get_element(index)
        i = 0

        if self.is_parent_table == True:
            for i in range(len(self.metadata["columns"])):
                if index.column() == i and role == QtCore.Qt.DisplayRole:
                    return data[self.metadata["columns"][i]]
        else:
            for i in range(len(self.metadata["subtable columns"])):
                if index.column() == i and role == QtCore.Qt.DisplayRole:
                    return data[self.metadata["subtable columns"][i]]

        return None

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        i = 0
        if self.is_parent_table == True:
            for i in range(len(self.metadata["columns"])):
                if (section == i and orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole):
                    return self.metadata["columns"][i]

        if self.is_parent_table == False:
            for i in range(len(self.metadata["subtable columns"])):
                if (section == i and orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole):
                    return self.metadata["subtable columns"][i]

        return None

    # Editable model methods
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        data = self.get_element(index)
        i = 0
        if value == "":
            return False

        if self.is_parent_table == True:
            for i in range(len(self.metadata["columns"])):
                if index.column() == i and role == QtCore.Qt.EditRole:
                    if self.metadata["columns"][i] == self.metadata["search key"]:
                        old_value = data[self.metadata["columns"][i]]
                        self.handler_reference.edit_subtable_unique_data(old_value, value)

                    data[self.metadata["columns"][i]] = value
                    self.handler_reference.edit(data)
                    return True

        if self.is_parent_table == False:
            for i in range(len(self.metadata["subtable columns"])):
                if index.column() == i and role == QtCore.Qt.EditRole:
                    data[self.metadata["subtable columns"][i]] = value
                    self.handler_reference.edit(data)
                    return True

        return False

    def flags(self, index):
        return super().flags(index) | QtCore.Qt.ItemIsEditable
