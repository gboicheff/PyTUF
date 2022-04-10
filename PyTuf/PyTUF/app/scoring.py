import numpy as np
from sklearn import metrics
from sklearn.metrics import roc_auc_score

# https://towardsdatascience.com/multi-class-metrics-made-simple-part-ii-the-f1-score-ebe8b2c2ca1
# https://towardsdatascience.com/multi-class-metrics-made-simple-part-i-precision-and-recall-9250280bddc2


class Score:
    def __init__(self, classifier, training_X, training_y, test_X, test_y):

        self.training_X = training_X
        self.training_y = training_y
        self.test_X = test_X
        self.test_y = test_y

        self.classes = list(
            set(np.unique(training_y)).intersection(set(np.unique(test_y)))
        )
        self.mappings = dict([(c, index) for index, c in enumerate(self.classes)])

        # binary classifier for the one vs rest ROCs
        self.binary_classifiers = [classifier() for i in range(len(self.classes))]
        self.train_binary_classifiers()

        # full classifier for non ROC metrics
        full_classifier = classifier()
        full_classifier.fit(training_X, training_y)
        self.predictions = full_classifier.predict(test_X)
        self.actual = test_y
        self.confusion_matrix = self.calculate_confusion_matrix()

    def calculate_confusion_matrix(self):
        confusion_matrix = np.zeros((len(self.mappings), len(self.mappings)))
        for prediction, actual_value in zip(self.predictions, self.actual):
            confusion_matrix[
                self.mappings[prediction], self.mappings[actual_value]
            ] += 1
        return confusion_matrix

    def calculate_accuracy(self):
        return np.trace(self.confusion_matrix) / len(self.actual)

    def calculate_precision(self, c):
        if self.confusion_matrix[self.mappings[c], self.mappings[c]] == 0:
            return 0.0
        return (
            self.confusion_matrix[self.mappings[c], self.mappings[c]]
            / self.confusion_matrix[:, self.mappings[c]].sum()
        )

    def calculate_recall(self, c):
        if self.confusion_matrix[self.mappings[c], self.mappings[c]] == 0:
            return 0.0
        return (
            self.confusion_matrix[self.mappings[c], self.mappings[c]]
            / self.confusion_matrix[self.mappings[c], :].sum()
        )

    def calculate_f1(self, c):
        precision = self.calculate_precision(c)
        recall = self.calculate_recall(c)
        if precision * recall == 0:
            return 0.0
        return (2 * precision * recall) / (precision + recall)

    def calculate_avg_precision(self):
        return sum(self.calculate_precision(c) for c in self.mappings.keys()) / len(
            self.mappings.keys()
        )

    def calculate_avg_recall(self):
        return sum(self.calculate_recall(c) for c in self.mappings.keys()) / len(
            self.mappings.keys()
        )

    def calculate_avg_f1(self):
        # return 2*(self.calculate_avg_precision()*self.calculate_avg_recall()) / ((1 / self.calculate_avg_precision()) + (1 / self.calculate_avg_recall()))
        return sum(self.calculate_f1(c) for c in self.mappings.keys()) / len(
            self.mappings.keys()
        )

    def binarize_labels(self, labels, selected_label):
        c_labels = np.zeros((len(labels),))
        for index, label in enumerate(labels):
            if label == selected_label:
                c_labels[index] = 1
            else:
                c_labels[index] = 0
        return c_labels

    def train_binary_classifiers(self):
        for index, current_class in enumerate(self.classes):
            training_y = self.binarize_labels(self.training_y, current_class)
            self.binary_classifiers[index].fit(self.training_X, training_y)

    def calculate_binary_rocs(self):
        rocs = {}
        for index, current_class in enumerate(self.classes):
            test_y = self.binarize_labels(self.test_y, current_class)
            # predictions = self.binary_classifiers[index].predict(self.test_X)
            probs = self.binary_classifiers[index].predict_prob(self.test_X)
            print(probs)
            tprs, fprs = self.calculate_roc(probs, test_y)
            auc_score = round(roc_auc_score(test_y, probs[:, 1]), 3)
            rocs["{}(AUC:{})".format(str(current_class), str(auc_score))] = {
                "tprs": tprs,
                "fprs": fprs,
            }
        return rocs

    def find_thresholds(self, probs, num_thresholds):
        sorted_probs = np.sort(probs).tolist()
        num_thresholds = min(num_thresholds, len(sorted_probs))
        window_size = int(len(sorted_probs) / num_thresholds)
        print(window_size)
        # thresholds[-1] = 1.0
        thresholds = [
            prob for index, prob in enumerate(sorted_probs) if index % window_size == 0
        ]
        thresholds.insert(0, 0.0)
        thresholds.append(1.0)
        return thresholds

    def calculate_roc(self, probs, labels):
        tprs, fprs = [], []
        thresholds = self.find_thresholds(probs[:, 1], 50)
        for thresh in thresholds:
            tp, fp, tn, fn = 0, 0, 0, 0
            for prob, actual in zip(probs[:, 1], labels):
                if prob > thresh:
                    if actual == 1:
                        tp += 1
                    else:
                        fp += 1
                else:
                    if actual == 0:
                        tn += 1
                    else:
                        fn += 1
            tpr, fpr = 0.0, 0.0
            if tp != 0:
                tpr = tp / (tp + fn)
            if fp != 0:
                fpr = fp / (fp + tn)
            tprs.append(tpr)
            fprs.append(fpr)

        # fprs, tprs, thresholds = metrics.roc_curve(labels, probs[:, 1])
        # fprs = fprs.tolist()
        # tprs = tprs.tolist()
        # print(fprs)
        # print(tprs)

        return tprs, fprs

    # # https://github.com/akshaykapoor347/Compute-AUC-ROC-from-scratch-python/blob/master/AUCROCPython.ipynb
    # # https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html
    # # https://mmuratarat.github.io/2019-10-01/how-to-compute-AUC-plot-ROC-by-hand
    # # https://stackoverflow.com/questions/45332410/roc-for-multiclass-classification
    # # https://towardsdatascience.com/comprehensive-guide-on-multiclass-classification-metrics-af94cfb83fbd
    # def calculate_rocs(self):
    #     rocs = {}
    #     for c in self.classes:
    #         tprs = []
    #         fprs = []
    #         for thresh in np.linspace(0, 1, 50):
    #             tp, fp, tn, fn = 0, 0, 0, 0
    #             for prediction, actual, prob in zip(
    #                 self.predictions, self.actual, self.probs[:, self.mappings[c]]
    #             ):
    #                 # above thresh
    #                 if prob > thresh:
    #                     if prediction == actual:
    #                         tp += 1
    #                     else:
    #                         fp += 1
    #                 else:
    #                     if actual == c:
    #                         fn += 1
    #                     else:
    #                         tn += 1

    #             # https://stackoverflow.com/questions/44008563/zero-denominator-in-roc-and-precision-recall
    #             tpr, fpr = 0.0, 0.0
    #             if tp != 0:
    #                 tpr = tp / (tp + fn)
    #             if fp != 0:
    #                 fpr = fp / (fp + tn)
    #             tprs.append(tpr)
    #             fprs.append(fpr)
    #         rocs[str(c)] = {"tprs": tprs, "fprs": fprs}
    #     return rocs

    def get_all_metrics(self):
        num_places = 6
        metric_dict = {
            "accuracy": round(self.calculate_accuracy(), num_places),
            "macro_f1_score": round(self.calculate_avg_f1(), num_places),
            "macro_precision": round(self.calculate_avg_precision(), num_places),
            "macro_recall": round(self.calculate_avg_recall(), num_places),
            "rocs": self.calculate_binary_rocs(),
        }
        # if self.probs is not None:
        #     metric_dict["rocs"] = self.calculate_rocs()
        return metric_dict
