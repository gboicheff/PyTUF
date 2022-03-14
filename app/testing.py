from paths import PathManager, PathType
from results import ResultManager, Result
from sklearn import datasets
import inspect



def add_paths(pm):
    pm.add_path("iris", PathType.DATA, data_path)
    pm.add_path("GNB", PathType.MODEL, gnb_model_path)
    pm.add_path("SVC", PathType.MODEL, svc_model_path)
    pm.add_path("DecisionTree", PathType.MODEL, dtree_model_path)

data_path = "app/data/test/iris.py"
gnb_model_path = "app/models/GNB/gnb.py"
svc_model_path = "app/models/SVC/svc.py"
dtree_model_path = "app/models/DecisionTree/dtree.py"


pm = PathManager()

# add_paths(pm)

data = pm.load("iris", PathType.DATA)
gnb = pm.load("GNB", PathType.MODEL)
svc = pm.load("SVC", PathType.MODEL)
dtree = pm.load("DecisionTree", PathType.MODEL)



gnb.fit(data.get_training_data(), data.get_training_target())
svc.fit(data.get_training_data(), data.get_training_target())
dtree.fit(data.get_training_data(), data.get_training_target())



rm = ResultManager()

gnb_result_arr = gnb.predict(data.get_testing_data()).tolist()
svc_result_arr = svc.predict(data.get_testing_data()).tolist()
dtree_result_arr = dtree.predict(data.get_testing_data()).tolist()

gnb_result = Result(gnb_model_path, {}, gnb_result_arr)
svc_result = Result(svc_model_path, {}, svc_result_arr)
dtree_result = Result(dtree_model_path, {}, dtree_result_arr)


rm.add_result(gnb_result)
rm.add_result(svc_result)
rm.add_result(dtree_result)



print(rm.load_result(gnb_model_path, {}))
print(rm.load_result(svc_model_path, {}))
print(rm.load_result(dtree_model_path, {}))

 
