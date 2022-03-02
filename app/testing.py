from path import PathManager, PathType
from results import ResultManager, Result
from sklearn import datasets
import inspect



pm = PathManager()

model_path = "C:/Dev/PythonEELDemo/app/data/test/iris.py"
pm.add_path("iris", PathType.DATA, model_path)
iris = pm.load("iris", PathType.DATA)

pm.add_path("GNB", PathType.MODEL, "C:/Dev/PythonEELDemo/app/models/testing/gnb.py")
model = pm.load("GNB", PathType.MODEL)




model.fit(iris.get_training_data(), iris.get_training_target())

result_arr = model.predict(iris.get_testing_data()).tolist()

result = Result(model_path, {}, result_arr)

rm = ResultManager()

rm.add_result(result)

print(rm.load_result(model_path, {}))

 
