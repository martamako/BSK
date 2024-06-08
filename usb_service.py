
import keyboard
from time import sleep
import os
import wmi
import cryptography


import usb.core
import usb.backend.libusb1

my_key = 'PROFIL'
files = r'E:\160578\WZR_JADE_2023.pdf'

c = wmi.WMI()

def check_for_key():
   for disk in c.Win32_LogicalDisk():
      if disk.VolumeName==my_key:
         return disk

print(check_for_key())

backend = usb.backend.libusb1.get_backend(find_library=lambda x:"D:\\Programowanie\\PycharmProjects\\BSK\\.venv\\Lib\\site-packages\\libusb\\_platform\\_windows\\x64\\libusb-1.0.dll")
print(backend)
dev = usb.core.find(backend=backend, find_all=True)
#for d in dev:
#    print(d)

#for dev in usb.core.find(find_all=True):
#    print(dev)

#programRun = True

#while programRun:
#    if keyboard.is_pressed('a'):
#        programRun = False

#    sleep(1)

