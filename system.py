import os
import socket
import sys
import psutil
import psutil as p
import platform
import getpass
from datetime import datetime
import time
import GPUtil
from tabulate import tabulate


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

        
#OS information
print("System Information")
uname = platform.uname()
print(f"[+] System: {uname.system}")
#print(f"[+] Node Name: {uname.node}")
#print(f"[+] Release: {uname.release}")
print(f"[+] Version: {uname.version}")
print(f"[+] Machine: {uname.machine}")
print(f"[+] Processor: {uname.processor}")

print("")

#CPU information
print("CPU Information")
# number of cores
print("[+] Physical cores:", psutil.cpu_count(logical=False))
print("[+] Total cores:", psutil.cpu_count(logical=True))
# CPU frequencies
cpufreq = psutil.cpu_freq()
print(f"[+] Max Frequency: {cpufreq.max:.2f}Mhz")
print(f"[+] Min Frequency: {cpufreq.min:.2f}Mhz")
print(f"[+] Current Frequency: {cpufreq.current:.2f}Mhz")
# CPU usage
print("[+] CPU Usage Per Core:")
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    print(f"[+] Core {i}: {percentage}%")
print(f"[+] Total CPU Usage: {psutil.cpu_percent()}%")

print("")

# Memory Information
print("RAM Information")
# get the memory details
svmem = psutil.virtual_memory()
print(f"[+] Total RAM: {get_size(svmem.total)}")
print(f"[+] Available RAM: {get_size(svmem.available)}")
print(f"[+] Used RAM: {get_size(svmem.used)}")
print(f"[+] Percentage: {svmem.percent}%")

print("")

# Network information
print("Network Information")
# get all network interfaces (virtual and physical)
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        #print(f"=== Interface: {interface_name} ===")
        if str(address.family) == 'AddressFamily.AF_INET':
            print(f"[+] IP Address: {address.address}")
            print(f"[+] Netmask: {address.netmask}")
            print(f"[+] Broadcast IP: {address.broadcast}")
        elif str(address.family) == 'AddressFamily.AF_PACKET':
            print(f"[+] MAC Address: {address.address}")
            print(f"[+] Netmask: {address.netmask}")
            print(f"[+] Broadcast MAC: {address.broadcast}")
# get IO statistics since boot
net_io = psutil.net_io_counters()
print(f"[+] Total Bytes Sent: {get_size(net_io.bytes_sent)}")
print(f"[+] Total Bytes Received: {get_size(net_io.bytes_recv)}")


print("")

#User Information
print("User Information")
print(f"[+] Username: {getpass.getuser()}")
hostname =socket.gethostname()
print("[+] Hostname: {}".format(hostname))

datetime_format = '%d/%m/%Y %H:%M:%S'
last_reboot=psutil.boot_time()
#print("[+] Last Login time: {}".format(datetime.fromtimestamp(last_reboot)))
boot_time=datetime.fromtimestamp(last_reboot)
print("[+] Last Login time: {}".format(boot_time.strftime(datetime_format)))

print("")



#Function to get info about Disk Usage.

print("Disk Information")
print("Partitions on Drive:")
par = p.disk_partitions()
  # getting all of the disk partitions
for x in par:
    print(f"[+] Drive: ", x.device)
    print(f"[+] File system type: ", x.fstype)

    dsk = p.disk_usage(x.mountpoint)
    print(f"[+] Total Size: ", get_size(dsk.total))
    print(f"[+] Used:       ", get_size(dsk.used))
    print(f"[+] Free:       ", get_size(dsk.free))
    print(f"[+] Percentage: ", dsk.percent, "%\n")




