import pandas as pd
import os
import importlib
import inspect
from model import Model
import json
from pathlib import Path, WindowsPath

class PathManager:
    def __init__(self, data_paths={}, model_paths={}):
        self.data_paths = data_paths
        self.model_paths = model_paths
        self.restore_state()

    def __del__(self):
        self.save_state()

    def save_state(self):
        with open("data_paths.json", "w", encoding="UTF-8") as outfile:
            json.dump(self.data_paths, outfile)
        with open("model_paths.json", "w", encoding="UTF-8") as outfile:
            json.dump(self.model_paths, outfile)

    def restore_state(self):
        if os.path.exists("data_paths.json"):
            with open("data_paths.json", "r", encoding="UTF-8") as file:
                self.data_paths.update(json.load(file))
        if os.path.exists("model_paths.json"):
            with open("model_paths.json", "r", encoding="UTF-8") as file:
                self.model_paths.update(json.load(file))

    def check_data_file(self, path):
        if os.path.splitext(path)[-1].lower() != ".csv":
            raise Exception("File at given path is not a csv file!")
        if not os.path.exists(path):
            raise Exception("File at given path does not exist!")

    def check_model_file(self, path):
        if os.path.splitext(path)[-1].lower() != ".py":
            raise Exception("File at given path is not a csv file!")
        if not os.path.exists(path):
            raise Exception("File at given path does not exist!")

    def add_data_path(self, name, path):
        # path = WindowsPath(path)
        print(path)
        if name in self.data_paths:
            raise Exception("Name already exists!")
        self.check_data_file(path)
        self.data_paths[name] = path

    def add_model_path(self, name, path):
        # path = WindowsPath(path)
        print(path)
        if name in self.data_paths:
            raise Exception("Name already exists!")
        self.check_model_file(path)
        self.model_paths[name] = path
    
    def get_data(self, name):
        path = self.data_paths[name]
        self.check_data_file(path)
        data = pd.read_csv(path)
        return data

    def get_model(self, name):
        path = self.model_paths[name]
        self.check_model_file(path)
        # dynamically load module at target path
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        # get dictionary of all classes inside the module
        members = dict(inspect.getmembers(mod))
        # instantiate the class with the given name and return it
        model = members[name]()
        if not isinstance(model, Model):
            raise Exception("Model must implement abstract Model class!")
        return model
