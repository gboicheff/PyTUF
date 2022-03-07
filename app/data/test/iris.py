from data import Data
import pandas as pd

class iris(Data):
    def __init__(self):
        self.data = pd.read_csv("app/data/test/test.csv")
        self.training = self.data[50:]
        self.testing = self.data[:50]


    def convert_target(self, target):
        target_dict = {
            "Setosa": 0,
            "Virginica":1,
            "Versicolor":2
        }
        return list(map(lambda x: target_dict[x], target))

    def get_training_data(self):
        return self.training[self.data.columns[:-1]]

    def get_training_target(self):
        return self.convert_target(self.training[self.data.columns[-1]])

    def get_testing_data(self):
        return self.testing[self.data.columns[:-1]]

    def get_testing_target(self):
        return self.convert_target(self.testing[self.data.columns[-1]])

    def get_all_data(self):
        return self.data[self.data.columns[:-1]]

    def get_all_target(self):
        return self.convert_target(self.data[self.data.columns[-1]])
    
    
