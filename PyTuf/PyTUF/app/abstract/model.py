from abc import ABC, abstractmethod

class Model(ABC):
    @abstractmethod
    def fit(self, data, target):
        pass

    @abstractmethod
    def predict(self, data):
        pass

    @abstractmethod
    def get_classes(self, data):
        pass


class ProbModel(Model):
    @abstractmethod
    def predict_prob(self, data):
        pass