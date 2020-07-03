from PySide2.QtCore import QAbstractTableModel
from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QLabel

class DBTableModel(QAbstractTableModel):
    def __init__(self, handler_reference, parent=None):
        super().__init__(parent)

        self.handler_reference = handler_reference
        self.d = self.handler_reference.data
        self.displayed_d = []
        self.columns = self.handler_reference.columns
        self.fill_displayed_data()
        
    def fill_displayed_data(self):
        for data in self.d:
            self.displayed_d.append(data)

    def get_element(self, index):
        return self.displayed_d[index.row()]

    def rowCount(self, index):
        return len(self.displayed_d)

    def columnCount(self, index):
        return len(self.columns) + 2

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            data = self.get_element(index)

            for i in range(len(self.columns) + 2):
                if index.column() == len(self.columns) and role == QtCore.Qt.DisplayRole:
                    return "connect"
                if index.column() == len(self.columns) + 1 and role == QtCore.Qt.DisplayRole:
                    return "remove"
                if index.column() == i and role == QtCore.Qt.DisplayRole:
                    return data[self.columns[i]]
            return None

        elif role == QtCore.Qt.EditRole:
            self.position = index
            obj = self.displayed_d[index.row()]
            key_number = index.column()

            edited_key = self.columns[key_number]
            edited_data = obj.get(edited_key)

            return edited_data

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        for i in range(len(self.columns)):
            if (section == i and orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole):
                return self.columns[i]
        return None

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        edited_data = self.get_element(index)
        
        print(edited_data)

        if value == "":
            return False

        for i in range(len(self.columns)):
            if index.column() == i and role == QtCore.Qt.EditRole:
                self.handler_reference.edit(value)
                self.handler_reference.load_data()
                self.layoutChanged.emit()
                return True
        return False

    def flags(self, index):
        return super().flags(index) | QtCore.Qt.ItemIsEditable

    def removeRows(self, row, rows, index=QtCore.QModelIndex()):
        pass

    def insertRows(self, row, rows, index=QtCore.QModelIndex()):
        pass

    def insert_row(self, row_obj):
        pass

    def table_search(self, search_line, combo_line):
        if self.data == []:
            return
        elif combo_line == "None chosen":
            key_array = self.d[0].keys()
            new_data = []
            for each_data in self.d:
                matched = False
                for key in key_array:
                    if search_line.lower() in str(each_data[key]).lower():
                        matched = True
                if matched:
                    new_data.append(each_data)
            self.displayed_d = new_data
            self.layoutChanged.emit()
        else:
            new_data = []
            for each_data in self.d:
                if search_line.lower() in str(each_data[combo_line]).lower():
                    new_data.append(each_data)                
            self.displayed_d = new_data
            self.layoutChanged.emit()
        
        
        


    