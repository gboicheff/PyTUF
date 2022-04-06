import pandas as pd
import os
import importlib
import inspect
from .model import Model
from .data import Data
from .feature_extractor import FeatureExtractor
import json
from pathlib import Path, WindowsPath
from enum import Enum
import pickle
import ast
import numpy as np


class PathDictError(Exception):
    def __init__(self, message, val):
        self.message = message
        self.val = val
        super().__init__(self.message)

class PathType(Enum):
    DATA = 1
    FEXTRACTOR = 2
    MODEL = 3

class PathDict:
    def __init__(self):
        self.d = {}
        self.STATE_PATH = "path_dict.pkl"

    def add_path(self, name: str, ptype: PathType, path: str):
        key = (name, ptype)
        if key in self.d:
            raise PathDictError("Name already assigned", self.d[key])
        self.d[key] = path
    
    def remove_path(self, name:str, ptype: PathType):
        key = (name, ptype)
        if not key in self.d:
            raise PathDictError("No path exists", name)
        self.d.pop(key)
        

    def get_path(self, name: str, ptype: PathType):
        key = (name, ptype)
        if not key in self.d:
            raise PathDictError("No path exists", name)
        return self.d[key]

    def save_state(self):
        with open(self.STATE_PATH, "wb") as outfile:
            pickle.dump(self.d, outfile)
    
    def load_state(self):
        if os.path.exists(self.STATE_PATH):
            with open(self.STATE_PATH, "rb") as infile:
                self.d = pickle.load(infile)

    def get_entries(self):
        return self.d.items()

    def clear(self):
        self.d = {}
    
    def reset(self):
        self.clear()
        os.remove(self.STATE_PATH)


class PMError(Exception):
    def __init__(self, message, val=None):
        self.message = message
        self.val = val
        super().__init__(self.message)


class PathManager:
    def __init__(self):
        self.p_dict = PathDict()
        # enable this after testing
        self.restore_state()

    def __del__(self):
        #self.save_state()
        pass

    def save_state(self):
        self.p_dict.save_state()

    def restore_state(self):
        self.p_dict.load_state()

    def reset_state(self):
        self.p_dict.reset()

    def check_file(self, path):
        if os.path.splitext(path)[-1].lower() != ".py":
            raise Exception("File at given path is not a csv file!")
        if not os.path.exists(path):
            raise Exception("File at given path does not exist!")

    def check_data(self, data):
        if isinstance(data, np.ndarray):
            return True
        return False

    def get_class(self, name: str, path: str, ptype: PathType):
        # dynamically load module at target path
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        # get dictionary of all classes inside the module
        members = dict(inspect.getmembers(mod))
        # instantiate the class with the given name and return it
        obj = members[name]()
        if ptype == PathType.DATA:
            if not isinstance(obj, Data):
                raise PMError("Data must implement Data class!")
            if not isinstance(obj.get_all_data(), np.ndarray):
                raise PMError("get_all_data() does not return numpy matrix")
            if not isinstance(obj.get_all_target(), np.ndarray):
                raise PMError("get_all_target() does not return numpy matrix")
            if not isinstance(obj.get_training_data(), np.ndarray):
                raise PMError("get_training_data() does not return numpy matrix")
            if not isinstance(obj.get_testing_data(), np.ndarray):
                raise PMError("get_testing_data() does not return numpy matrix")
            if not isinstance(obj.get_training_target(), np.ndarray):
                raise PMError("get_training_target() does not return numpy matrix")
            if not isinstance(obj.get_testing_target(), np.ndarray):
                raise PMError("get_testing_target() does not return numpy matrix")

        
        if ptype == PathType.FEXTRACTOR and not isinstance(obj, FeatureExtractor):
            raise PMError("Feature Extractor must implement FeatureExtractor class!")

        if ptype == PathType.MODEL and not isinstance(obj, Model):
            raise PMError("Model must implement Model class!")


        return obj

    def add_path(self, name, ptype, path):
        self.get_class(name, path, ptype)
        self.p_dict.add_path(name, ptype, path)
        self.save_state()
    
    def remove_path(self, name, ptype):
        self.p_dict.remove_path(name, ptype)
        self.save_state()
    
    def get_path(self, name, ptype):
        return self.p_dict.get_path(name, ptype)

    
    def load(self, name, ptype):
        path = self.p_dict.get_path(name, ptype)
        self.check_file(path)
        return self.get_class(name, path, ptype)

    def get_entries(self, selected_type):
        entries = self.p_dict.get_entries()
        return [(name, path) for ((name, t), path) in entries if t == selected_type]



# if __name__ == "__main__":

    # quick pathdict tests
    # pd = PathDict()

    # duplicate add error
    # pd.add_path("test", PathType.MODEL, "test")
    # pd.add_path("test", PathType.MODEL, "test")

    # duplicate remove error
    # pd.add_path("test", PathType.MODEL, "test")
    # pd.remove_path("test", PathType.MODEL)
    # pd.remove_path("test", PathType.MODEL)

    #nonexistent key error
    # pd.get_path("bob", PathType.DATA)


    #basic functionality
    # pd.add_path("test", PathType.MODEL, "home/test")
    # print(pd.get_path("test", PathType.MODEL))


    # quick pm tests
    # pm = PathManager()
    # pm.add_path("iris", PathType.DATA, "C:/Users/Grant/Dev/PythonEELDemo/app/data/test/iris.py")
