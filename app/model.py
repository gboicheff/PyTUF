from abc import ABC, abstractmethod

class Model(ABC):
    
    @abstractmethod
    def fit_predict(features):
        pass

    @abstractmethod
    def fit(features):
        pass

    @abstractmethod
    def predict(features):
        pass
