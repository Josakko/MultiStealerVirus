import subprocess
import os
import getpass


class StartUp:
    def main(self):
        #print("Enabled")

        username = getpass.getuser()
        app = r"C:\Path\to\your\program.exe"

        batch = os.path.join(os.getenv('TEMP'), 'SystemBin-64bit.bat')
        with open(batch, 'w') as f:
            f.write(f'@echo off\nstart "" "{app}"')

        task = "SystemBin-64bit"
        os.system(f'schtasks /create /tn "{task}" /tr "{batch}" /sc "ONSTART" /ru "{username}"')
        
        
        
    
    def create_batch(self):
        with open(f"{self.dir}/run.bat", "w") as f:
            f.write("@echo off")
            f.write(f'\nstart "" "{self.dir}"')
        self.reg_edit()
            
    def reg_edit(self):
        subprocess.run(args=["reg", "delete", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", "/v", "SystemBit-64bit", "/f"], shell=True)
        subprocess.run(args=["reg", "add", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", "/v", "SystemBit-64bit", "/t", "REG_SZ", "/d", f"{self.dir}\\run.bat", "/f"], shell=True)
    
    def run(self):
        try:
            with open("todo.txt", "r") as f:
                startup = f.readlines()[4]
        except:
            startup = False
            
        if not startup or startup == "False":
            return
        elif startup == "True":
            self.dir = os.getcwd()
            self.create_batch()
        else:
            return
        
#startup = StartUp()
#startup.run()
