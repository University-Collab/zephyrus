import json, pickle, bisect
from controller.data_handler.data_handler import DataHandler


class SequentialDataHandler(DataHandler):
    def __init__(self, path, meta_path, unique_data=None):
        super().__init__()
        self.path = path
        self.meta_path = meta_path
        self.loaded_data = []
        self.data = []
        self.meta_data = {}
        self.search_key = ""
        self.linked_file_path = ""
        self.unique_data = unique_data
        self.load_data()

    def load_data(self):
        with open(self.meta_path, "r") as data_file:
            self.meta_data = json.load(data_file)
            self.search_key = self.meta_data["search key"]
            
        with open(self.linked_file_path, "rb") as data_file:
            loaded_data = sorted(pickle.load(data_file), key=lambda k: k[self.search_key])
            if self.unique_data:
                for obj in self.loaded_data:
                    if obj[self.search_key] == self.unique_data:
                        self.data.append(obj)
            else:
                self.data = loaded_data

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
            self.save(data=self.data)

    def save(self, data):
        with open(self.path, "wb") as pickle_file:
            pickle.dump(data, pickle_file)

    def edit(self, obj):
        self.save(data=sorted(self.data, key=lambda k: k[self.search_key]))

    def delete_one(self, unique_data):
        if len(self.data) == 1:
            self.data.pop(0)
            self.save(data=self.data)
        else:
            self.data.pop(self.find_index(self.data, unique_data))
            self.save(data=self.data)
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
