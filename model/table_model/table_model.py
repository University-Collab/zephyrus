from PySide2.QtCore import QAbstractTableModel
from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QLabel


class TableModel(QAbstractTableModel):
    def __init__(self, handler_reference, parent=None):
        super().__init__(parent)
        self.handler_reference = handler_reference
        self.d = self.handler_reference.data
        self.displayed_d = []
        self.metadata = self.handler_reference.meta_data
        self.fill_displayed_data()

    def fill_displayed_data(self):
        for data in self.d:
            self.displayed_d.append(data)

    def get_element(self, index):
        return self.displayed_d[index.row()]

    def get_element_d(self, representing_value):
        for data in self.d:
            if data[self.metadata["representing key"]] == representing_value:
                return data

    def rowCount(self, index):
        return len(self.displayed_d)

    def columnCount(self, index):
        return len(self.metadata["columns"])+2

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            data = self.get_element(index)
            i = 0

            for i in range(len(self.metadata["columns"])+2):
                if index.column() == len(self.metadata["columns"]) and role == QtCore.Qt.DisplayRole:
                    return "connect"
                if index.column() == len(self.metadata["columns"])+1 and role == QtCore.Qt.DisplayRole:
                    return "remove"
                if index.column() == i and role == QtCore.Qt.DisplayRole:
                    return data[self.metadata["columns"][i]]

            return None

        elif role == QtCore.Qt.EditRole:
            self.position = index
            obj = self.displayed_d[index.row()]
            key_number = index.column()
            
            edited_key = self.metadata['columns'][key_number]
            edited_data = obj.get(edited_key)
            return edited_data

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        i = 0
        
        for i in range(len(self.metadata["columns"])):
            if (section == i and orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole):
                return self.metadata["columns"][i]

        return None

    # Editable model methods
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        edited_data = self.get_element(index)
        reference = self.get_element_d(edited_data[self.metadata["representing key"]])
        # print(edited_data)
        i = 0

        if value == "":
            return False

        
        for i in range(len(self.metadata["columns"])):
            if index.column() == i and role == QtCore.Qt.EditRole:
                

                reference[self.metadata["columns"][i]] = value
                self.handler_reference.edit()
                return True

        return False

    def flags(self, index):
        return super().flags(index) | QtCore.Qt.ItemIsEditable

    def removeRows(self, row, rows, index=QtCore.QModelIndex()):

        row_data = self.displayed_d[row]
        self.displayed_d.pop(row)
        # print(row_data)
        i = 0
        for data in self.d:
            if data[self.metadata["representing key"]] == row_data[self.metadata["representing key"]]:
                self.d.pop(i)
                self.layoutChanged.emit()
                break
            i +=1
        self.handler_reference.edit()


        return True

    def insertRows(self, row, rows, index=QtCore.QModelIndex()):
        self.beginInsertRows(index, row, row + rows - 1)
        new_obj = {}
        
        for key in self.metadata['columns']: 
            new_obj[key] = "..."
        new_obj[self.metadata["representing key"]] = self.d[len(self.d)-1][self.metadata["representing key"]]+1

        self.displayed_d.append(new_obj)
        self.d.append(new_obj)
        self.handler_reference.edit()
        self.endInsertRows()
        return True

    def insert_row(self, row_obj):
        
        new_obj = row_obj
        new_obj[self.metadata["representing key"]] = self.d[len(self.d)-1][self.metadata["representing key"]] + 1
       

        self.displayed_d.append(new_obj)
        self.d.append(new_obj)
        self.handler_reference.edit()
        
        self.layoutChanged.emit()
        return True

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