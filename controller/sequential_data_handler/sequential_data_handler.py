import json, bisect
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
        with open(self.meta_path) as data_file:
            self.meta_data = json.load(data_file)
            self.search_key = self.meta_data["search key"]
            self.linked_file_path = (self.path.split("storage/")[0] + "storage/" + self.meta_data["linked file"])

        if self.is_parent_table == True:
            with open(self.path) as data_file:
                self.data = sorted(json.load(data_file), key=lambda k: k[self.search_key])

        if self.is_parent_table == False:
            with open(self.linked_file_path) as data_file:
                self.loaded_data = sorted(json.load(data_file), key=lambda k: k[self.search_key])
                for obj in self.loaded_data:
                    if obj[self.search_key] == self.unique_data:
                        self.data.append(obj)

    def get_one(self, unique_data):
        if len(self.data) == 0:
            return None
        elif len(self.data) == 1:
            return data[0]
        else:
            for d in self.data:
                return self.data[bisect.bisect_left(self.data, unique_data)]

    def get_all(self):
        return self.data

    def insert(self, obj):
        if len(self.data) == 0:
            self.data.append(obj)
        else:
            bisect.insort_left(self.data, obj)
        self.save(data=self.data, parent_table=True)

    def save(self, data, parent_table=False, sub_table=False):
        if parent_table and not sub_table:
            with open(self.path, "w") as json_file:
                json.dump(data, json_file, indent=4)
        elif sub_table and not parent_table:
            with open(self.linked_file_path, "w") as json_file:
                json.dump(data, json_file, indent=4)

    def edit(self, obj):
        if self.is_parent_table:
            self.save(data=self.data, parent_table=True)
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

            self.save(data=sorted(data, key=lambda k: k[self.search_key]), sub_table=True)

    def edit_subtable_unique_data(self, old_value, new_value):
        subtable_data = []

        with open(self.linked_file_path) as data_file:
            subtable_data = sorted(json.load(data_file), key=lambda k: k[self.search_key])

        for d in subtable_data:
            if d[self.meta_data["search key"]] == old_value:
                d[self.meta_data["search key"]] = new_value

        self.save(data=subtable_data, sub_table=True)

    def delete_one(self, unique_data):
        if len(self.data) == 1:
            self.data.pop(0)
            self.save(data=self.data, parent_table=True)
        else:
            self.data.pop(bisect.bisect_left(self.data, unique_data))
            self.save(data=self.data, parent_table=True)
        return

    def add_multiple(self, list):
        for element in list:
            bisect.insort_left(self.data, element)
        self.save(data=self.data, parent_table=True)
        return
