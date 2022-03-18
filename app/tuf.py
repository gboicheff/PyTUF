from app.paths import PathType
from results import ResultManager
from paths import PathManager

class Options:
    def __init__(self):
        self.data_path = None
        self.ft_path = None
        self.model_path = None
        self.use_cache = False

class TufInterface:
    def __init__(self):
        self.pm = PathManager()
        self.rm = ResultManager()
        self.options = Options()

    # upload path
    def upload(self, name, path, type):
        self.pm.add_path(name, path, type)


    # select data, feature extractor or model
    def select(self, name, type):
        if type == PathType.DATA:
            self.options.data_path = (name, type)
        elif type == PathType.FEXTRACTOR:
            self.options.ft_path = (name, type)
        elif type == PathType.MODEL:
            self.options.model_path = (name, type)
        else:
            raise Exception("Invalid type on selected entry!")
    
    # select options + maybe scoring method
    def select_options():
        pass

    # fit transform model
    def run(self):
        if self.options.data_path is None:
            raise Exception("Data must be selected before running")
        elif self.options.model_path is None:
            raise Exception("Model must be selected before running")

        data = self.pm.load(*self.options.data_path)
        training_data = data.get_testing_data()
        testing_data = data.get_testing_data()
        model = self.pm.load(*self.options.model_path)
        
        if self.options.ft_path is not None:
            ft = self.pm.load(*self.options.ft_path)
            training_data = ft.fit_transform(training_data)
            testing_data = ft.fit(testing_data)

        model.fit(training_data)
        return model.predict(testing_data)

    # do scoring
    def score():
        pass


        
        

    