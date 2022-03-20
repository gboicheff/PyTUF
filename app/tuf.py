from paths import PathType
from results import ResultManager
from paths import PathManager

class Selections:
    def __init__(self):
        self.data_name = ""
        self.ft_name = ""
        self.model_name = ""
        self.use_cache = False

class TufInterface:
    def __init__(self):
        self.pm = PathManager()
        self.rm = ResultManager()
        self.selections = Selections()

    # upload path
    def upload(self, name: str, path: str, type: PathType):
        self.pm.add_path(name, type, path)
    
    # get the name:path pairs to be used for the entries in one of the lists
    def get_entries(self, type: PathType):
        return self.pm.get_entries(type)


    # select data, feature extractor or model
    def select(self, name: str, type: PathType):
        if type == PathType.DATA:
            self.selections.data_name = name
        elif type == PathType.FEXTRACTOR:
            self.selections.ft_name = name
        elif type == PathType.MODEL:
            self.selections.model_name = name
        else:
            raise Exception("Invalid type on selected entry!")
    
    # select options + maybe scoring method
    def select_options():
        pass

    # fit transform model
    def run(self):
        # data_path = self.pm.get_path(self.selections.data_name)
        # ft_path = self.pm.get_path(self.selections.ft_name)
        model_path = self.pm.get_path(self.selections.model_name, PathType.MODEL)

        try:
            return self.rm.load_result(self.selections, model_path)
        except:
            if self.selections.data_name == "":
                raise Exception("Data must be selected before running")
            elif self.selections.model_name == "":
                raise Exception("Model must be selected before running")

            data = self.pm.load(self.selections.data_name, PathType.DATA)
            training_data = data.get_testing_data()
            testing_data = data.get_testing_data()
            model = self.pm.load(self.selections.model_name, PathType.MODEL)
            
            if self.selections.ft_path != "":
                ft = self.pm.load(self.selections.ft_name, PathType.FEXTRACTOR)
                training_data = ft.fit_transform(training_data)
                testing_data = ft.fit(testing_data)

            model.fit(training_data)
            return model.predict(testing_data)

    # do scoring
    def score():
        pass




def test():
    pass


if __name__ == "__main__":

    data_path = "app/data/test/iris.py"
    gnb_model_path = "app/models/GNB/gnb.py"
    svc_model_path = "app/models/SVC/svc.py"
    dtree_model_path = "app/models/DecisionTree/dtree.py"

    ti = TufInterface()


    ti.upload("iris", data_path, PathType.DATA)
    ti.upload("model", gnb_model_path, PathType.MODEL)


    ti.select("iris", PathType.DATA)
    ti.select("model", PathType.MODEL)



    ti.run()


        
        

    