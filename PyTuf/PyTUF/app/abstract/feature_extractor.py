from abc import ABC, abstractmethod

class FeatureExtractor(ABC):
    
    @abstractmethod
    def fit_transform(self, data_set):
        pass

    @abstractmethod
    def fit(self, data_set):
        pass

    @abstractmethod
    def transform(self, data_set):
        pass
