from sklearn.tree import DecisionTreeClassifier
from app.abstract.model import Model


class DecisionTree(Model):
    def __init__(self):
        self.model = DecisionTreeClassifier()
    
    def fit(self, data, target):
        self.model = self.model.fit(data, target)
    
    def predict(self, data):
        return self.model.predict(data)

    def predict_prob(self, data):
        return self.model.predict_proba(data)

    def get_classes(self):
        return self.model.classes_