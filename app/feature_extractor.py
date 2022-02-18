from abc import ABC, abstractmethod

class FeatureExtractor(ABC):
    
    @abstractmethod
    def fit_transform():
        pass

    @abstractmethod
    def fit(data_set):
        pass

    @abstractmethod
    def transform(data_set):
        pass
