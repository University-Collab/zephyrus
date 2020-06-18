import json, pickle
from controller.data_handler.data_handler import DataHandler


class SerialDataHandler(DataHandler):
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
        
            
        with open(self.path, "rb") as data_file:
            loaded_data = pickle.load(data_file)
            if self.unique_data:
                for obj in loaded_data:
                    if obj[self.search_key] == self.unique_data:
                        self.data.append(obj)
                # print(self.data)
            else:
                self.data = loaded_data
                

 
    def get_one(self, unique_data):
        for d in self.data:
            if getattr(d, self.search_key) == unique_data:
                return d
        return None

    def get_all(self):
        return self.data

    def insert(self, obj):
        self.data.append(obj)
        self.save(self.data)

    def save(self):
        with open(self.path, "wb") as pickle_file:
            pickle.dump(self.data, pickle_file)

    def edit(self):
        self.save()


    def delete_one(self, unique_data):
        position = 0
        for d in self.data:
            if getattr(d, self.search_key) == unique_data:
                self.data.pop(position)
                self.save(self.data)
                return
            position += 1
        return

    def add_multiple(self, list):
        for element in list:
            self.insert(element)
        
        return
