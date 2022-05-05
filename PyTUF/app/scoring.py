import numpy as np
import math
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

    def calculate_macro_precision(self):
        return sum(self.calculate_precision(c) for c in self.mappings.keys()) / len(
            self.mappings.keys()
        )

    def calculate_macro_recall(self):
        return sum(self.calculate_recall(c) for c in self.mappings.keys()) / len(
            self.mappings.keys()
        )

    def calculate_macro_f1(self):
        return sum(self.calculate_f1(c) for c in self.mappings.keys()) / len(
            self.mappings.keys()
        )

    def calculate_micro_precision(self):
        num = 0
        denom = 0
        for c in self.classes:
            num += self.confusion_matrix[self.mappings[c], self.mappings[c]]
            denom += self.confusion_matrix[:, self.mappings[c]].sum()
        if num == 0.0:
            return 0.0
        else:
            return num / denom

    def calculate_micro_recall(self):
        num = 0
        denom = 0
        for c in self.classes:
            num += self.confusion_matrix[self.mappings[c], self.mappings[c]]
            denom += self.confusion_matrix[self.mappings[c], :].sum()
        if num == 0.0:
            return 0.0
        else:
            return num / denom

    def calculate_micro_recall(self):
        num = 0
        denom = 0
        for c in self.classes:
            num += self.confusion_matrix[self.mappings[c], self.mappings[c]]
            denom += self.confusion_matrix[self.mappings[c], :].sum()
        if num == 0.0:
            return 0.0
        else:
            return num / denom

    def calculate_micro_f1(self):
        tp = 0
        fp = 0
        fn = 0
        for c in self.classes:
            tp += self.confusion_matrix[self.mappings[c], self.mappings[c]]
            fn += (
                self.confusion_matrix[self.mappings[c], :].sum()
                - self.confusion_matrix[self.mappings[c], self.mappings[c]]
            )
            fn += (
                self.confusion_matrix[:, self.mappings[c]].sum()
                - self.confusion_matrix[self.mappings[c], self.mappings[c]]
            )
        if tp == 0.0:
            return 0.0
        else:
            return tp / (tp + (1 / 2) * (fp + fn))

    # convert labels from multiclass to 1 for target label and 0 otherwise
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

    # calculate ROC curves for all binary classifiers
    def calculate_binary_rocs(self):
        rocs = {}
        for index, current_class in enumerate(self.classes):
            test_y = self.binarize_labels(self.test_y, current_class)
            probs = self.binary_classifiers[index].predict_prob(self.test_X)
            tprs, fprs = self.calculate_roc(probs, test_y)
            auc_score = round(
                roc_auc_score(test_y, probs[:, 1]), 3
            )  # get AUC from sklearn
            rocs["{}(AUC:{})".format(str(current_class), str(auc_score))] = {
                "tprs": tprs,
                "fprs": fprs,
            }
        return rocs

    # generate thresholds for the ROC curves based on the minimum value of prob when the probabilties are partitioned into num_thresholds groups
    def find_thresholds(self, probs, num_thresholds):
        sorted_probs = np.sort(probs).tolist()
        num_thresholds = min(num_thresholds, len(sorted_probs))
        window_size = int(len(sorted_probs) / num_thresholds)
        thresholds = [
            prob for index, prob in enumerate(sorted_probs) if index % window_size == 0
        ]
        thresholds.insert(0, 0.0)
        thresholds.append(math.nextafter(max(sorted_probs), 2))
        return thresholds

    # calculate a single ROC
    def calculate_roc(self, probs, labels):
        tprs, fprs = [], []
        thresholds = self.find_thresholds(probs[:, 1], 50)
        for thresh in thresholds:
            tp, fp, tn, fn = 0, 0, 0, 0
            for prob, actual in zip(probs[:, 1], labels):
                if prob >= thresh:
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

    # output all metrics for scoring page
    def get_all_metrics(self):
        num_places = 6
        metric_dict = {
            "accuracy": round(self.calculate_accuracy(), num_places),
            "macro_f1_score": round(self.calculate_macro_f1(), num_places),
            "macro_precision": round(self.calculate_macro_precision(), num_places),
            "macro_recall": round(self.calculate_macro_recall(), num_places),
            "micro_f1": round(self.calculate_micro_f1(), num_places),
            "micro_precision": round(self.calculate_micro_precision(), num_places),
            "micro_recall": round(self.calculate_micro_recall(), num_places),
            "rocs": self.calculate_binary_rocs(),
        }
        return metric_dict
