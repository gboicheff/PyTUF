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


class SMError(Exception):
    '''Exception type for errors coming from ScoreManager'''
    def __init__(self, message, val):
        self.message = message
        self.val = val
        super().__init__(self.message)


class ScoreManager:
    '''
        ScoreManager handles score caching for the application.
        ScoreManager uses pickledb as a fast temporary store for previous scores.
    '''
    def __init__(self):
        self.database = pickledb.load("result.db", False)

    '''get_name is u'''
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

    def add_score(self, selections, metric_dict, model_path):
        name = self.get_name(selections)
        hash = self.hash_file(model_path)
        d = {
            "hash": hash,
            "metrics": metric_dict,
        }
        json_d = json.dumps(d)
        self.database.set(name, json_d)

    def load_score(self, selections, model_path):
        name = self.get_name(selections)
        if self.database.exists(name):
            d = json.loads(self.database.get(name))
            old_hash, metrics = d["hash"], d["metrics"]
            # result_arr = np.array(ast.literal_eval(result_arr))
            hash = self.hash_file(model_path)
            if old_hash != hash:
                raise SMError("Model has been modified!", model_path)
            return metrics
        else:
            raise SMError("Result does not exist!", name)



# if __name__ == "__main__":
#     rm = ResultManager()
#     result = Result("C:\Dev\PythonEELDemo\gui\gui.py", {}, [1,2,1,3,2,1,0,1,1,2,3])
    
#     # rm.add_result(result)
#     # print("test:")
#     print(rm.load_result("C:\Dev\PythonEELDemo\gui\gui.py", {}))
