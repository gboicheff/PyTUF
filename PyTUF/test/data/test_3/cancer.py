from app.abstract.data import Data
import pandas as pd
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split


class cancer(Data):
    def __init__(self):
        self.X, self.y = load_breast_cancer(return_X_y=True)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.1, random_state=21
        )

    def get_training_data(self):
        return self.X_train

    def get_training_target(self):
        # print(self.y_train)
        return self.y_train

    def get_testing_data(self):
        return self.X_test

    def get_testing_target(self):
        return self.y_test

    def get_all_data(self):
        return self.X

    def get_all_target(self):
        return self.y
