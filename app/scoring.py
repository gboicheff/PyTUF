import numpy as np
from sklearn import metrics
#https://towardsdatascience.com/multi-class-metrics-made-simple-part-ii-the-f1-score-ebe8b2c2ca1
#https://towardsdatascience.com/multi-class-metrics-made-simple-part-i-precision-and-recall-9250280bddc2
class Score:
    def __init__(self, predictions, actual, probs, classes):
        if len(predictions) != len(actual):
            raise Exception("Length mismatch!")
        self.classes = classes
        self.predictions = predictions
        self.actual = actual
        self.probs = probs
        self.mappings = dict([(c, index) for index,c in enumerate(self.classes)])
        self.confusion_matrix = self.calculate_confusion_matrix(predictions, actual)
        

    # def setup(self, predictions, actual,):
    #     classes = set(actual)
    #     self.predictions = predictions
    #     self.actual = actual
    #     self.mappings = dict([(c, index) for index,c in enumerate(classes)])
    #     self.confusion_matrix = self.calculate_confusion_matrix(predictions, actual)

    def calculate_confusion_matrix(self, predictions, actual):
        confusion_matrix = np.zeros((len(self.mappings),len(self.mappings)))
        for prediction, actual_value in zip(predictions, actual):
            confusion_matrix[self.mappings[prediction],self.mappings[actual_value]]+=1
        return confusion_matrix

    def calculate_accuracy(self):
        return np.trace(self.confusion_matrix) / len(self.actual)

    def calculate_precision(self, c):
        return self.confusion_matrix[self.mappings[c],self.mappings[c]] / self.confusion_matrix[:,self.mappings[c]].sum()

    def calculate_recall(self, c):
        return self.confusion_matrix[self.mappings[c],self.mappings[c]] / self.confusion_matrix[self.mappings[c]].sum()

    def calculate_f1(self, c):
        precision = self.calculate_precision(c)
        recall = self.calculate_recall(c)
        return (2*precision*recall)/(precision+recall)

    def calculate_avg_precision(self):
        return sum(self.calculate_precision(c) for c in self.mappings.keys()) / len(self.mappings.keys())

    def calculate_avg_recall(self):
        return sum(self.calculate_recall(c) for c in self.mappings.keys()) / len(self.mappings.keys())

    def calculate_avg_f1(self):
        return sum(self.calculate_f1(c) for c in self.mappings.keys()) / len(self.mappings.keys())


    # def calculate_ovr(self, c, thresh):
    #     tp = 0
    #     fp = 0
    #     tn = 0
    #     fn = 0
    #     for prediction, prob in zip(self.predictions, self.probs[]):
    #         if prob > thresh:
    #             if 



