from model import Model
from sklearn.svm import SVC as skSVC


class SVC(Model):
    def __init__(self):
        self.model = skSVC(kernel='linear')
    
    def fit(self, data, target):
        self.model = self.model.fit(data, target)
    
    def predict(self, data):
        return self.model.predict(data)