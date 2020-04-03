from abc import ABC, abstractclassmethod

class DataHandler(ABC):
    def __init__(self):
        super().__init__()

    @abstractclassmethod
    def get_one(cls, id):
        pass
    
    @abstractclassmethod
    def get_all(cls):
        pass

    @abstractclassmethod
    def edit(cls, obj):
        pass
    
    @abstractclassmethod
    def delete_one(cls, id):
        pass

    @abstractclassmethod
    def insert(cls, obj):
        pass