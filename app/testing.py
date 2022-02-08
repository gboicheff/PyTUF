from path import PathManager


pm = PathManager()

# pm.add_data_path("iris", "C:/Dev/PythonEELDemo/app/data/iris.csv")
# print(pm.get_data("iris"))


pm.add_model_path("test", "C:/Dev/PythonEELDemo/app/models/testing/test.py")
mod = pm.get_model("test")
model = mod.GNB()
model.fit()



