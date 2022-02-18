from path import PathManager, PathType
from sklearn import datasets
import inspect



pm = PathManager()

pm.add_path("iris", PathType.DATA, "C:/Dev/PythonEELDemo/app/data/test/iris.py")
iris = pm.load("iris", PathType.DATA)

pm.add_path("GNB", PathType.MODEL, "C:/Dev/PythonEELDemo/app/models/testing/gnb.py")
model = pm.load("GNB", PathType.MODEL)




model.fit(iris.get_training_data(), iris.get_training_target())

print(model.predict(iris.get_testing_data()))


 
