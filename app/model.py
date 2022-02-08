from abc import ABC, abstractmethod

class Model(ABC):
    
    # @abstractmethod
    # def fit_predict(data, target):
    #     pass

    @abstractmethod
    def fit(self, data, target):
        pass

    @abstractmethod
    def predict(self, data):
        pass
