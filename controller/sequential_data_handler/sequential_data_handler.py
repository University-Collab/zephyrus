import json, pickle, bisect
from controller.data_handler.data_handler import DataHandler


class SequentialDataHandler(DataHandler):
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
                self.data = sorted(pickle.load(data_file), key=lambda k: k[self.search_key])

        if self.is_parent_table == False:
            with open(self.linked_file_path, "rb") as data_file:
                self.loaded_data = sorted(pickle.load(data_file), key=lambda k: k[self.search_key])
                for obj in self.loaded_data:
                    if obj[self.search_key] == self.unique_data:
                        self.data.append(obj)

    def get_one(self, unique_data):
        if len(self.data) == 0:
            return None
        elif len(self.data) == 1:
            return data[0]
        else:
            one = self.data[self.find_index(self.data, unique_data)]
            if one is not None:
                return one

    def get_all(self):
        return self.data

    def insert(self, obj):
        key_exists = self.find_index(self.data, obj[self.search_key])

        if key_exists is not None:
            return
        else:
            keys = [unique[self.search_key] for unique in self.data]
            bisect.insort_left(keys, obj[self.search_key])
            index = self.find_index(keys, obj[self.search_key])

            self.data.insert(index, obj)
            self.save(data=self.data, parent_table=True)

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
            self.save(data=sorted(self.loaded_data, key=lambda k: k[self.search_key]), sub_table=True)

    def edit_subtable_unique_data(self, old_value, new_value):
        subtable_data = []

        with open(self.linked_file_path, "rb") as data_file:
            subtable_data = sorted(pickle.load(data_file), key=lambda k: k[self.search_key])

        for d in subtable_data:
            if d[self.meta_data["search key"]] == new_value:
                return
            if d[self.meta_data["search key"]] == old_value:
                d[self.meta_data["search key"]] = new_value

        self.save(data=subtable_data, sub_table=True)

    def delete_one(self, unique_data):
        if len(self.data) == 1:
            self.data.pop(0)
            self.save(data=self.data, parent_table=True)
        else:
            self.data.pop(self.find_index(self.data, unique_data))
            self.save(data=self.data, parent_table=True)
        return

    def add_multiple(self, list):
        for element in list:
            self.insert(element)
        return

    def find_index(self, list, value):
        start, end = 0, len(list) - 1

        while start <= end:
            middle = (start + end) // 2

            if getattr(list[middle], self.search_key) == value:
                return middle
            elif getattr(list[middle], self.search_key) < value:
                start = middle + 1
            elif getattr(list[middle], self.search_key) > value:
                end = middle - 1

        return None
