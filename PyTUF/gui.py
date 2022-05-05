import eel
import os
from tkinter import filedialog, Tk
from app.pyTUF import PyTufInterface, PyTUFError
from app.paths import PathType, PathDictError, PMError


# from paths import PathDict, PathType

# initialize tuf object:
ti = PyTufInterface()

root = Tk()
root.withdraw()
root.wm_attributes("-topmost", 1)

# Set web files folder
eel.init("web")

# @eel.expose                         # Expose this function to Javascript
# def say_hello_py(x):
#     print('Hello from %s' % x)

# say_hello_py('Python World!')
# eel.say_hello_js('Python World!')   # Call a Javascript function


@eel.expose
def get_folder(foldname):
    if foldname == "/collections":
        foldname = os.getcwd() + "/collections"
    filelist = os.listdir(foldname)
    print(filelist)
    return filelist


@eel.expose
def select_path():
    filepath = filedialog.askopenfilename(
        parent=root, initialdir="/", filetypes=[("Python File", ".py")]
    )
    # use tuf to add path:
    print(filepath)
    return filepath


@eel.expose
def upload_path(name, path, type):
    print(name, "", path, "", type)

    try:
        if type == 1:
            ti.upload(name, path, PathType.DATA)
            ti.select(name, PathType.DATA)
        elif type == 2:
            ti.upload(name, path, PathType.FEXTRACTOR)
            ti.select(name, PathType.FEXTRACTOR)
        elif type == 3:
            ti.upload(name, path, PathType.MODEL)
            ti.select(name, PathType.MODEL)
    except PathDictError as e:
        # handle
        print(e.message)
        if e.val is None:
            return "PathDictError: " + e.message
        else:
            return "PathDictError: " + e.message + " " + e.val
    except PMError as e:
        # handle
        if e.val is None:
            return "PMError: " + e.message
        else:
            return "PMError: " + e.message + " " + e.val
    except Exception as e:
        return str(e)


@eel.expose
def remove_path(name, type):
    
    try:
        if type == 1:
            ti.remove(name, PathType.DATA)
            ti.select("", PathType.DATA)
        elif type == 2:
            ti.remove(name, PathType.FEXTRACTOR)
            ti.select("", PathType.FEXTRACTOR)
        elif type == 3:
            ti.remove(name, PathType.MODEL)
            ti.select("", PathType.MODEL)
    except PathDictError as e:
        # handle
        if e.val is None:
            return "PathDictError: " + e.message
        else:
            return "PathDictError: " + e.message + " " + e.val
    except Exception as e:
        return str(e)


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

    try:
        ti.run()
    except PathDictError as e:
        # handle
        if e.val is None:
            return "PathDictError: " + e.message
        else:
            return "PathDictError: " + e.message + " " + e.val
    except PMError as e:
        # handle
        if e.val is None:
            return "PMError: " + e.message
        else:
            return "PMError: " + e.message + " " + e.val
    except PyTUFError as e:
        # handle
        if e.val is None:
            return "PyTUFError: " + e.message
        else:
            return "PyTUFError: " + e.message + " " + e.val
    # except Exception as e:
    #     return str(e)

@eel.expose
def update_selection(name, type):
    if type == 1:
        ti.select(name, PathType.DATA)
    elif type == 2:
        ti.select(name, PathType.FEXTRACTOR)
    elif type == 3:
        ti.select(name, PathType.MODEL)

@eel.expose
def get_selections():
    s = []
    s.append(ti.selections.data_name) 
    s.append(ti.selections.ft_name)
    s.append(ti.selections.model_name)

    return list(s)



@eel.expose
def get_toggle():
    return ti.selections.use_cache


@eel.expose
def toggle_check():
    ti.toggle_use_cache()


eel.start("index.html", size=(1200, 1000), mode="chrome")  # Start
