import pandas as pd
import numpy as np
from app.abstract.data import Data


class iris(Data):
    def __init__(self):
        self.data = pd.read_csv("test/data/test/test.csv").to_numpy()
        np.random.shuffle(self.data)
        self.training = self.data[50:, :]
        self.testing = self.data[:50, :]

    def convert_target(self, target):
        # target_dict = {
        #     "Setosa": 0,
        #     "Virginica":1,
        #     "Versicolor":2
        # }
        # return list(map(lambda x: target_dict[x], target))
        return target

    def get_training_data(self):
        return self.training[:, :-1]

    def get_training_target(self):
        return self.convert_target(self.training[:, -1])

    def get_testing_data(self):
        return self.testing[:, :-1]

    def get_testing_target(self):
        return self.convert_target(self.testing[:, -1])

    def get_all_data(self):
        return self.data[:, :-1]

    def get_all_target(self):
        return self.convert_target(self.data[:, -1])
    
    
