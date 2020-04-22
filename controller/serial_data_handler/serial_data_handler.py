import json, pickle
from controller.data_handler.data_handler import DataHandler


class SerialDataHandler(DataHandler):
    def __init__(self, path, meta_path, is_parent_table=True, unique_data=None):
        super().__init__()
        self.path = path
        self.meta_path = meta_path
        self.loaded_data = []
        self.data = []
        self.meta_data = {}
        self.search_key = ""
        self.linked_file_path = ""
        self.is_parent_table = is_parent_table
        self.unique_data = unique_data
        self.load_data()

    def load_data(self):
        with open(self.meta_path, "r") as data_file:
            self.meta_data = json.load(data_file)
            self.search_key = self.meta_data["search key"]
            self.linked_file_path = (self.path.split("storage/")[0] + "storage/" + self.meta_data["linked file"])

        if self.is_parent_table == True:
            with open(self.path, "rb") as data_file:
                self.data = pickle.load(data_file)

        if self.is_parent_table == False:
            with open(self.linked_file_path, "rb") as data_file:
                self.loaded_data = pickle.load(data_file)
                for obj in self.loaded_data:
                    if obj[self.search_key] == self.unique_data:
                        self.data.append(obj)

    def get_one(self, unique_data):
        for d in self.data:
            if getattr(d, self.search_key) == unique_data:
                return d
        return None

    def get_all(self):
        return self.data

    def insert(self, obj):
        self.data.append(obj)
        self.save(self.data, parent_table=True)

    def save(self, data, parent_table=False, sub_table=False):
        if parent_table and not sub_table:
            with open(self.path, "wb") as pickle_file:
                pickle.dump(data, pickle_file)
        elif sub_table and not parent_table:
            with open(self.linked_file_path, "wb") as pickle_file:
                pickle.dump(data, pickle_file)

    def edit(self, obj):
        if self.is_parent_table:
            self.save(data=self.data, parent_table=True)
        else:
            self.save(data=self.loaded_data, sub_table=True)

    def edit_subtable_unique_data(self, old_value, new_value):
        subtable_data = []
        with open(self.linked_file_path, "rb") as data_file:
            subtable_data = pickle.load(data_file)
        for d in subtable_data:
            if d[self.meta_data["search key"]] == old_value:
                d[self.meta_data["search key"]] = new_value

        self.save(data=subtable_data, sub_table=True)

    def delete_one(self, unique_data):
        position = 0
        for d in self.data:
            if getattr(d, self.search_key) == unique_data:
                self.data.pop(position)
                self.save(self.data, parent_table=True)
                return
            position += 1
        return

    def add_multiple(self, list):
        for element in list:
            self.data.append(element)
        self.save(self.data, parent_table=True)
        return
