from sklearn import preprocessing
from app.abstract.model import Model
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import Binarizer


class MLP(Model):
    def __init__(self):
        self.model = MLPClassifier(random_state=1)
    
    def fit(self, data, target):
        self.model = self.model.fit(data, target)
    
    def predict(self, data):
        return self.model.predict(data)
    
    def predict_prob(self, data):
        return self.model.predict_proba(data)
    
    def get_classes(self):
        return self.model.classes_