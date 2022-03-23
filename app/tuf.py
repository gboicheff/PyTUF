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

    # remove path
    def remove(self, name:str, type: PathType):
        self.pm.remove_path(name, type)
    
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
    
    def toggle_use_cache(self):
        self.selections.use_cache = not self.selections.use_cache


    def train_fit(self):
        model_path = self.pm.get_path(self.selections.model_name, PathType.MODEL)
        if self.selections.data_name == "":
                raise Exception("Data must be selected before running")
        elif self.selections.model_name == "":
            raise Exception("Model must be selected before running")

        data = self.pm.load(self.selections.data_name, PathType.DATA)
        training_data = data.get_training_data()
        training_target = data.get_training_target()
        testing_data = data.get_testing_data()
        model = self.pm.load(self.selections.model_name, PathType.MODEL)
        
        if self.selections.ft_name != "":
            ft = self.pm.load(self.selections.ft_name, PathType.FEXTRACTOR)
            training_data = ft.fit_transform(training_data)
            testing_data = ft.fit(testing_data)

        model.fit(training_data, training_target)
        result_arr = model.predict(testing_data)
        self.rm.add_result(self.selections, result_arr, model_path)
        return result_arr

    # will be executed when run test button is pressed
    def run(self):
        model_path = self.pm.get_path(self.selections.model_name, PathType.MODEL)
        if self.selections.use_cache:
            try:
                return self.rm.load_result(self.selections, model_path)
            except Exception as e:
                return self.train_fit()
        else:
            return self.train_fit()

    # do scoring
    def score():
        pass




if __name__ == "__main__":

    data_path = "app/data/test/iris.py"
    gnb_model_path = "app/models/GNB/gnb.py"
    svc_model_path = "app/models/SVC/svc.py"
    dtree_model_path = "app/models/DecisionTree/dtree.py"

    ti = TufInterface()


    ti.upload("iris", data_path, PathType.DATA)

    ti.upload("GNB", gnb_model_path, PathType.MODEL)
    ti.upload("SVC", svc_model_path, PathType.MODEL)
    ti.upload("DecisionTree", dtree_model_path, PathType.MODEL)



    ti.select("iris", PathType.DATA)
    ti.select("GNB", PathType.MODEL)



    print(ti.get_entries(PathType.MODEL))
    ti.remove("SVC", PathType.MODEL)
    print(ti.get_entries(PathType.MODEL))



    print(ti.get_entries(PathType.DATA))



    ti.run()
    ti.run()
    ti.run()
    print(ti.run())
    print(ti.run())
    print(ti.run())


        
        

    