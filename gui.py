import eel
import os

# Set web files folder
eel.init('web')

# @eel.expose                         # Expose this function to Javascript
# def say_hello_py(x):
#     print('Hello from %s' % x)

# say_hello_py('Python World!')
# eel.say_hello_js('Python World!')   # Call a Javascript function

@eel.expose
def get_folder():
    path = os.getcwd() + "/collections"
    filelist = os.listdir(path)
    print(filelist)
    return filelist


eel.start('hello.html', size=(1200, 1000), mode='chrome')  # Start