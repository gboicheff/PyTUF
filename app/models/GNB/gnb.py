from model import Model
from sklearn.naive_bayes import GaussianNB


class GNB(Model):
    def __init__(self):
        self.model = GaussianNB()
    
    def fit(self, data, target):
        self.model = self.model.fit(data, target)
    
    def predict(self, data):
        return self.model.predict(data)