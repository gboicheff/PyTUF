from .paths import PathType
from .results import ScoreManager, SMError
from .paths import PathManager
from .scoring import *
import matplotlib.pyplot as plt
import pandas as pd


class PyTUFError(Exception):
    def __init__(self, message, val):
        self.message = message
        self.val = val
        super().__init__(self.message)


class Selections:
    def __init__(self):
        self.data_name = ""
        self.ft_name = ""
        self.model_name = ""
        self.use_cache = False


class PyTufInterface:
    def __init__(self):
        self.pm = PathManager()
        self.sm = ScoreManager()
        self.selections = Selections()

    # upload path
    def upload(self, name: str, path: str, type: PathType):
        self.pm.add_path(name, type, path)

    # remove path
    def remove(self, name: str, type: PathType):
        self.pm.remove_path(name, type)

    # get the name:path pairs to be used for the entries in one of the lists
    def get_entries(self, type: PathType):
        return self.pm.get_entries(type)

    # select data, feature extractor or model
    def select(self, name: str, type: PathType):
        if type == PathType.DATA:
            self.selections.data_name = name
        elif type == PathType.FEXTRACTOR:
            self.selections.ft_name = name
        elif type == PathType.MODEL:
            self.selections.model_name = name
        else:
            raise Exception("Invalid type on selected entry!")

    def toggle_use_cache(self):
        self.selections.use_cache = not self.selections.use_cache

    # full process of getting data, extracting features(optional) and then fitting the model
    # all methods called in user written code are wrapped in try catches to prevent errors
    def train_fit(self):
        model_path = self.pm.get_path(self.selections.model_name, PathType.MODEL)

        if self.selections.data_name == "":
            raise Exception("Data must be selected before running")
        elif self.selections.model_name == "":
            raise Exception("Model must be selected before running")

        data = self.pm.load(self.selections.data_name, PathType.DATA)()

        try:
            training_data = data.get_training_data()
            training_target = data.get_training_target()
            testing_data = data.get_testing_data()
            testing_target = data.get_testing_target()
        except Exception as e:
            raise PyTUFError("Exception caused by selected data!", str(e))

        model = self.pm.load(self.selections.model_name, PathType.MODEL)

        if self.selections.ft_name != "" and self.selections.ft_name != "None":
            ft = self.pm.load(self.selections.ft_name, PathType.FEXTRACTOR)()

            try:
                training_data = ft.fit_transform(training_data)
                testing_data = ft.transform(testing_data)
            except Exception as e:
                raise PyTUFError(
                    "Exception caused by selected feature extractor!", str(e)
                )

        # try:
        #     model.fit(training_data, training_target)
        #     result_arr = model.predict(testing_data)
        #     probs = model.predict_prob(testing_data)
        # except Exception as e:
        #     raise PyTUFError("Exception caused by selected classifier!", str(e))

        score = Score(
            model, training_data, training_target, testing_data, testing_target
        )
        metrics = score.get_all_metrics()
        self.sm.add_score(self.selections, metrics, model_path)
        return metrics

    # will be executed when run test button is pressed
    def run(self):
        plt.close("all")
        model_path = self.pm.get_path(self.selections.model_name, PathType.MODEL)
        metric_dict = {}
        if self.selections.use_cache:
            # if classifier file changed since last score then recalculate score
            try:
                metric_dict = self.sm.load_score(self.selections, model_path)
            except SMError as e:
                metric_dict = self.train_fit()
        else:
            metric_dict = self.train_fit()
        self.score(metric_dict)

    # generate matplotlib graph with metrics from score class
    def score(self, metric_dict):

        fig, ax = plt.subplots(figsize=(10, 7), facecolor="#dcdcdc")
        ax.set_xlabel("FPR Rate")
        ax.set_ylabel("TPR Rate")
        ax.plot([0, 1], [0, 1])

        if "rocs" in metric_dict:
            rocs = metric_dict["rocs"]
            for c in rocs.keys():
                ax.plot(rocs[c]["fprs"], rocs[c]["tprs"], label=c)
                ax.legend()

        result_str = ""

        entry = "  {}  :  {}  "
        for metric in metric_dict.keys():
            if metric != "rocs":
                result_str += entry.format(metric, metric_dict[metric])

        table_data = [
            (name, value) for name, value in metric_dict.items() if name != "rocs"
        ]
        df = pd.DataFrame(dict(table_data), index=[1])
        ax.table(
            cellText=df.values,
            colLabels=df.columns,
            rowLoc="center",
            loc="bottom",
            bbox=[0.0, -0.4, 1, 0.2],
        )

        # columns = [name for name in metric_dict.keys() if name != "rocs"]
        # values = [value for name,value in metric_dict.items() if name != "rocs"]

        # table = plt.table()
        # ax.annotate(
        #     result_str,
        #     xy=(0.9, -0.2),
        #     xycoords="axes fraction",
        #     ha="right",
        #     va="center",
        #     fontsize=10,
        # )

        ax.set_title(
            "ROC ({}, {})".format(
                self.selections.data_name, self.selections.model_name
            ),
            fontsize=14,
            fontweight="bold",
        )
        fig.tight_layout()
        plt.show()


if __name__ == "__main__":

    data_path = "app/data/test/iris.py"
    gnb_model_path = "app/models/GNB/gnb.py"
    svc_model_path = "app/models/SVC/svc.py"
    dtree_model_path = "app/models/DecisionTree/dtree.py"

    ti = PyTufInterface()

    ti.upload("iris", data_path, PathType.DATA)

    ti.upload("GNB", gnb_model_path, PathType.MODEL)
    ti.upload("SVC", svc_model_path, PathType.MODEL)
    ti.upload("DecisionTree", dtree_model_path, PathType.MODEL)

    ti.select("iris", PathType.DATA)
    ti.select("GNB", PathType.MODEL)

    # print(ti.get_entries(PathType.MODEL))
    # # ti.remove("GNB", PathType.MODEL)
    # print(ti.get_entries(PathType.MODEL))

    # print(ti.get_entries(PathType.DATA))

    ti.run()

    # score = Score(predictions, actual, prob, classes)
    # ti.score(score)

    # fig = plt.figure()
    # ax = fig.add_subplot()
    # fig.subplots_adjust(top=0.85)
    # fig.suptitle('ROC', fontsize=14, fontweight='bold')
    # ax.set_title('axes title', fontsize=14, fontweight='bold')

    # print(score.calculate_accuracy())
    # print(score.calculate_avg_f1())
    # print(score.calculate_avg_precision())
    # print(score.calculate_avg_recall())
    # print(score.confusion_matrix)
    # ti.run()
    # ti.run()
    # print(ti.run())
    # print(ti.run())
    # print(ti.run())
