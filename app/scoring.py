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
        return self.confusion_matrix[self.mappings[c],self.mappings[c]] / self.confusion_matrix[self.mappings[c],:].sum()

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


    #https://github.com/akshaykapoor347/Compute-AUC-ROC-from-scratch-python/blob/master/AUCROCPython.ipynb
    #https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html
    #https://mmuratarat.github.io/2019-10-01/how-to-compute-AUC-plot-ROC-by-hand
    #https://stackoverflow.com/questions/45332410/roc-for-multiclass-classification
    def calculate_rocs(self):
        rocs = {}
        for index,c in enumerate(self.classes):
            tprs = []
            fprs = []
            for thresh in np.linspace(0,1,1000):
                tp = 0
                fp = 0
                tn = 0
                fn = 0
                for prediction, actual, prob in zip(self.predictions, self.actual, self.probs[:, index]):
                        # above thresh
                        if prob >= thresh:
                            if prediction == actual:
                                tp+=1
                            else:
                                fp+=1
                        else:
                            if actual == c:
                                fn+=1
                            else:
                                tn+=1
                tpr = tp/(tp+fn+1)
                fpr = fp/(fp+tn+1)
                # print((thresh, tp, fp, tn, fn))
                tprs.append(tpr)
                fprs.append(fpr)
            rocs[c] = {
                "tprs": tprs,
                "fprs": fprs 
            }
        return rocs

    def get_all_metrics(self, num_places):
        return {
            "accuracy": round(self.calculate_accuracy(),num_places),
            "f1_score": round(self.calculate_avg_f1(),num_places),
            "avg_precision": round(self.calculate_avg_precision(),num_places),
            "avg_recall": round(self.calculate_avg_recall(),num_places)
        }
            
                


