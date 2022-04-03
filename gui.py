import eel
import os
from tkinter import filedialog

import sys
sys.path.append('C:/Users/Max/Desktop/College/Spring 2022/Senior Proj/PythonEELDemo/app')

from tuf import Selections, TufInterface

from paths import PathType

#from paths import PathDict, PathType

#initialize tuf object:
ti = TufInterface()

# Set web files folder
eel.init('web')

# @eel.expose                         # Expose this function to Javascript
# def say_hello_py(x):
#     print('Hello from %s' % x)

# say_hello_py('Python World!')
# eel.say_hello_js('Python World!')   # Call a Javascript function

@eel.expose
def get_folder(foldname):
    if (foldname == "/collections"):
        foldname = os.getcwd() + "/collections"
    filelist = os.listdir(foldname)
    print(filelist)
    return filelist

@eel.expose
def select_path():
    filepath = filedialog.askopenfilename()
    #use tuf to add path:
    return filepath

@eel.expose
def upload_path(name, path, type):
    print(name, "", path, "", type)

    if type == 1:
        ti.upload(name, path, PathType.DATA)
    elif type == 2:
        ti.upload(name, path, PathType.FEXTRACTOR)
    elif type == 3:
        ti.upload(name, path, PathType.MODEL)

@eel.expose
def remove_path(name, type):
    print("remove")
    if type == 1:
        ti.remove(name, PathType.DATA)
    elif type == 2:
        ti.remove(name, PathType.FEXTRACTOR)
    elif type == 3:
        ti.remove(name, PathType.MODEL)


@eel.expose
def get_paths(type):
    if type == 1:
        entries = ti.get_entries(PathType.DATA)
    elif type == 2:
        entries = ti.get_entries(PathType.FEXTRACTOR)
    elif type == 3:
        entries = ti.get_entries(PathType.MODEL)

    retlist = []
    for e in entries:
        retlist.append(e[0])
    return list(retlist)

@eel.expose
def run_test(dataname, fextractname, modelname, cache):
    print("run attempt:")
    ti.select(dataname, PathType.DATA)
    ti.select(fextractname, PathType.FEXTRACTOR)
    ti.select(modelname, PathType.MODEL)

    print(ti.run())






eel.start('hello.html', size=(1200, 1000), mode='chrome')  # Start
