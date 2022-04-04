from abc import ABC, abstractmethod


class Data(ABC):
    @abstractmethod
    def get_training_data(self):
        pass

    def get_training_target(self):
        pass

    @abstractmethod
    def get_testing_data(self):
        pass

    @abstractmethod
    def get_testing_target(self):
        pass

    @abstractmethod
    def get_all_data(self):
        pass

    @abstractmethod
    def get_all_target(self):
        pass

    # @abstractmethod
    # def get_feature_headings(self):
    #     pass
