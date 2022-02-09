from path import PathManager
from sklearn import datasets
import inspect
pm = PathManager()

pm.add_data_path("iris", "C:/Dev/PythonEELDemo/app/data/iris.csv")
print(pm.get_data("iris"))





iris = pm.get_data("iris")
print(iris)
print(iris.shape)
data = iris[iris.columns[:-1]]


target = iris[iris.columns[-1]]


target_dict = {
    "Setosa": 0,
    "Virginica":1,
    "Versicolor":2
}


target = list(map(lambda x: target_dict[x], target))



pm.add_model_path("GNB", "C:/Dev/PythonEELDemo/app/models/testing/gnb.py")
model = pm.get_model("GNB")

model.fit(data, target)

print(model.predict(data[:100]))


 
