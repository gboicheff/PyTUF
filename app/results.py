import redis
import hashlib
import ast
import json
#https://github.com/redis/redis-py

# class Options:

def convert_options(options):
    return ""
class Result:
    def __init__(self, filename, options, result_arr):
        self.name = filename + convert_options(options)
        self.result_arr = result_arr

class ResultManager:
    def __init__(self):
        self.db = redis.Redis(host='localhost', port=6379, db=0)
        pass

    def hash_file(self, filename):
        h = hashlib.sha256()
        with open(filename, "r") as file:
            while True:
                data = file.read(8192).encode('utf-8')
                if not data:
                    break
                h.update(data)
        return h.hexdigest()


    def add_result(self, result):
        hash = self.hash_file(result.name)
        d = {
            "hash": hash,
            "result_arr":result.result_arr
        }
        json_d = json.dumps(d)
        self.db.set(result.name, json_d)

    def load_result(self, filename, options):
        name = filename + convert_options(options)
        if self.db.exists(name):
            d = json.loads(self.db.get(name))
            old_hash, result_arr = d["hash"], d["result_arr"]
            hash = self.hash_file(filename)
            if old_hash != hash:
                raise Exception("{} has been modified!".format(filename))
            return result_arr
        else:
            raise Exception("Record with name {} does not exist!".format(name))



if __name__ == "__main__":
    rm = ResultManager()
    result = Result("C:\Dev\PythonEELDemo\gui\gui.py", {}, [1,2,1,3,2,1,0,1,1,2,3])
    
    # rm.add_result(result)
    # print("test:")
    print(rm.load_result("C:\Dev\PythonEELDemo\gui\gui.py", {}))
