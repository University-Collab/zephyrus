import json
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
        with open(self.meta_path) as data_file:
            self.meta_data = json.load(data_file)
            self.search_key = self.meta_data["search key"]
            self.linked_file_path = (
                self.path.split("storage/")[0]
                + "storage/"
                + self.meta_data["linked file"]
            )

        if self.is_parent_table == True:
            with open(self.path) as data_file:
                self.data = json.load(data_file)

        if self.is_parent_table == False:
            with open(self.linked_file_path) as data_file:
                self.loaded_data = json.load(data_file)
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
        self.save()

    def save(self):
        if self.is_parent_table == True:
            with open(self.path, "w") as json_file:
                json.dump(self.data, json_file, indent=4)
        else:
            data = []
            for d in self.loaded_data:
                data.append(d)
            i = 0

            # removing old objects that were shown
            for d in data:
                if d[self.search_key] == self.unique_data:
                    data.pop(i)
                i += 1

            for updated_obj in self.data:
                data.append(updated_obj)

            with open(self.linked_file_path, "w") as json_file:
                json.dump(data, json_file, indent=4)

    def edit(self, obj):
        for d in self.data:
            if getattr(d, self.search_key) == getattr(obj, self.search_key):
                for key in self.meta_data["columns"]:
                    d[key] = obj[key]
                self.save()
                return
        return

    def edit_subtable_unique_data(self, old_value, new_value):
        subtable_data = []
        with open(self.linked_file_path) as data_file:
            subtable_data = json.load(data_file)
        for d in subtable_data:
            if d[self.meta_data["search key"]] == old_value:
                d[self.meta_data["search key"]] = new_value

        with open(self.linked_file_path, "w") as json_file:
            json.dump(subtable_data, json_file, indent=4)

    def delete_one(self, unique_data):
        position = 0
        for d in self.data:
            if getattr(d, self.search_key) == unique_data:
                self.data.pop(position)
                self.save()
                return
            position += 1
        return

    def add_multiple(self, array):
        for element in array:
            self.data.append(element)
        self.save()
        return
