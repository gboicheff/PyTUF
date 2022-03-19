import eel
import os
from tkinter import filedialog

from paths import PathDict, PathType

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
    foldername = filedialog.askdirectory()
    return foldername



eel.start('hello.html', size=(1200, 1000), mode='chrome')  # Start