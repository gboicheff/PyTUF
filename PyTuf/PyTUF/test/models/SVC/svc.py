from sklearn import preprocessing
from app.abstract.model import Model
from sklearn.svm import SVC as skSVC
from sklearn.preprocessing import Binarizer


class SVC(Model):
    def __init__(self):
        self.model = skSVC(kernel="linear", probability=True)
        self.binarizer = preprocessing.LabelBinarizer()
    
    def fit(self, data, target):
        self.model = self.model.fit(data, target)
    
    def predict(self, data):
        return self.model.predict(data)
    
    def predict_prob(self, data):
        return self.binarizer.fit_transform(self.predict(data))
    
    def get_classes(self):
        return self.model.classes_