from app.paths import PathType
from results import ResultManager
from paths import PathManager

class Options:
    def __init__(self):
        self.data_path = None
        self.ft_path = None
        self.model_path = None
        self.use_cache = False

class TufManager:
    def __init__(self):
        self.pm = PathManager()
        self.rm = ResultManager()
        self.options = Options()

    def upload(self, name, path, type):
        self.pm.add_path(name, path, type)

    def select(self, name, type):
        if type == PathType.DATA:
            self.options.data_path = (name, type)
        elif type == PathType.FEXTRACTOR:
            self.options.ft_path = (name, type)
        elif type == PathType.MODEL:
            self.options.model_path = (name, type)
        else:
            raise Exception("Invalid type on selected entry!")

    def run(self):
        if self.options.data_path is None:
            raise Exception("Data must be selected before running")
        elif self.options.model_path is None:
            raise Exception("Model must be selected before running")

        data = self.pm.load(*self.options.data_path)
        if self.options.ft_path is not None:
            ft = self.pm.load(*self.options.ft_path)
            data = ft.fit_transform(data)
        
        

    