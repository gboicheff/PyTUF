import pandas as pd
import os
import importlib
import inspect
from model import Model
from data import Data
from feature_extractor import FeatureExtractor
import json
from pathlib import Path, WindowsPath
from enum import Enum
import pickle
import ast

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
            raise Exception("Name already assigned to path: {}".format(self.d[key]))
        self.d[key] = path
    
    def remove_path(self, name:str, ptype: PathType):
        key = (name, ptype)
        if not key in self.d:
            raise Exception("No path exists for name: {}".format(name))
        self.d.pop(key)
        

    def get_path(self, name: str, ptype: PathType):
        key = (name, ptype)
        if not key in self.d:
            raise Exception("No path exists for name: {}".format(name))
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


class PathManager:
    def __init__(self):
        self.p_dict = PathDict()
        # enable this after testing
        # self.restore_state()

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

    def add_path(self, name, ptype, path):
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
        # dynamically load module at target path
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        # get dictionary of all classes inside the module
        members = dict(inspect.getmembers(mod))
        # instantiate the class with the given name and return it
        obj = members[name]()
        if ptype == PathType.DATA and not isinstance(obj, Data):
            raise Exception("Data must implement Data class!")
        
        if ptype == PathType.FEXTRACTOR and not isinstance(obj, FeatureExtractor):
            raise Exception("Feature Extractor must implement Data class!")

        if ptype == PathType.MODEL and not isinstance(obj, Model):
            raise Exception("Model must implement Model class!")

        return obj

    def get_entries(self, selected_type):
        entries = self.p_dict.get_entries()
        return [(name, path) for ((name, t), path) in entries if t == selected_type]



def testing():
    pass
