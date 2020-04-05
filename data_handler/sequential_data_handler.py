from data_handler.data_handler import DataHandler
import json

class SequentialDataHandler(DataHandler):
    def __init__(self, path, meta_path):
        super().__init__()
        # polja i funkcije treba napisati i implementirati