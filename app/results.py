import redis
import hashlib
import ast
import json
import pickledb
import numpy as np
#https://github.com/redis/redis-py


# this will be used to add option information to the stored result name later
# def convert_options(options):
#     return ""

# class Result:
#     def __init__(self, filename, options, result_arr):
#         self.name = filename + convert_options(options)
#         self.result_arr = result_arr

class RMError(Exception):
    def __init__(self, message, val):
        self.message = message
        self.val = val
        super().__init__(self.message)


class ResultManager:
    def __init__(self):
        self.db = pickledb.load("result.db", False)
        pass

    def get_name(self, selections):
        return selections.data_name + "-" + selections.ft_name + "-" + selections.model_name

    def hash_file(self, filename):
        h = hashlib.sha256()
        with open(filename, "r") as file:
            while True:
                data = file.read(8192).encode('utf-8')
                if not data:
                    break
                h.update(data)
        return h.hexdigest()

    def add_result(self, selections, result_arr, model_path):
        name = self.get_name(selections)
        hash = self.hash_file(model_path)
        d = {
            "hash": hash,
            "result_arr":str(result_arr.tolist())
        }
        json_d = json.dumps(d)
        self.db.set(name, json_d)

    def load_result(self, selections, model_path):
        name = self.get_name(selections)
        if self.db.exists(name):
            d = json.loads(self.db.get(name))
            old_hash, result_arr = d["hash"], d["result_arr"]
            result_arr = np.array(ast.literal_eval(result_arr))
            hash = self.hash_file(model_path)
            if old_hash != hash:
                raise RMError("Model has been modified!", model_path)
            return result_arr
        else:
            raise RMError("Result does not exist!", name)



# if __name__ == "__main__":
#     rm = ResultManager()
#     result = Result("C:\Dev\PythonEELDemo\gui\gui.py", {}, [1,2,1,3,2,1,0,1,1,2,3])
    
#     # rm.add_result(result)
#     # print("test:")
#     print(rm.load_result("C:\Dev\PythonEELDemo\gui\gui.py", {}))
