from path import PathManager
from sklearn import datasets
import inspect
pm = PathManager()

pm.add_data_path("iris", "C:/Dev/PythonEELDemo/app/data/iris.csv")
print(pm.get_data("iris"))






iris = datasets.load_iris()

pm.add_model_path("GNB", "C:/Dev/PythonEELDemo/app/models/testing/gnb.py")
model = pm.get_model("GNB")

model.fit(iris.data, iris.target)

print(model.predict(iris.data[:100,]))


 
