#!/usr/bin/python3

from subprocess import Popen, PIPE
import os
import sys
from termcolor import colored as c

wd = os.getcwd()
oldwd = wd
while not "msploit" in wd.split("/"):
	newdir = input("Enter path to msploit: ")
	os.chdir(newdir)
	wd = os.getcwd()

options_defaults = {'payload':None}

banner = c('''
-------------
|  MSploit! |
-------------
Developed by:
  Marcus Weinberger
____________
''',"magenta")

help_menu = '''
help - prints this
show [options/modules/exploits] - displays selected value(s)
set [name] [value] - sets $name to $value
exploit (alt: run) - runs the listener for selected payload
build (alt: make) - builds the implant for selected payload
exit - exits msploit
'''

def run_cmd(cmd):
	return Popen(cmd,stdout=PIPE,shell=True).communicate()[0].decode()
def error(msg): return c("[!] ","red") + msg
def info(msg): return c("[*] ","cyan") + msg

def check_exists(exploit):
	files = run_cmd("ls").split("\n")
	if exploit.endswith("/"):
		exploit = list(exploit)
		exploit.remove(exploit[-1])
		exploit = ''.join(exploit)
	if exploit in files:
		return True
	else:
		return False

def run_listener(exploit):
	if not check_exists(exploit):
		print(error("Exploit does not exist"))
		return None
	os.chdir(exploit)
	os.system("./listener.py")

def gen_payload(exploit):
	if not check_exists(exploit):
		print(error("Exploit does not exist"))
		return None
	os.chdir(exploit)
	template = open("./implant.py","r")
	tplate = template.read()
	addr = input("Enter argument for implant [usually addr/url]: ")
	tplate += "\tmain(argv=['',\"%s\"])" % addr
	if "/" in list(exploit):
		payload = exploit.split("/")[0]
	else:
		payload = exploit
	payload += ".py"
	os.chdir(oldwd)
	with open(payload,"w") as out_file:
		out_file.write(tplate)
	template.close()
	print(info("Saved payload as: " + payload))


def main():
	global options
	options = options_defaults
	print(banner)
	while True:
		try:
			cmd = input("MS> ")
			if cmd == "exit" or cmd == "quit":
				break
			else:
				handle_cmd(cmd)
		except Exception as e:
			print(error("Error: "+str(e)))
	print(c("Cya later!","magenta"))
	os.chdir(oldwd)
	exit(0)

def handle_cmd(cmd):
	global options
	if not ' ' in cmd:
		if cmd == "help":
			print(help_menu)
			return None
		elif cmd == "build" or cmd == "make":
			if options['payload'] == None:
				print(error("Please set payload first"))
				return None
			else:
				gen_payload(options['payload'])
				return None
		elif cmd == "run" or cmd == "exploit":
			if options['payload'] == None:
				print(error("Please set payload/handler first"))
				return None
			else:
				run_listener(options['payload'])
				return None
		else:
			print(error("Invalid command"))
			return None
	subcmd = cmd.split(" ")
	if subcmd[0] == "set":
		name = subcmd[1]
		value = subcmd[2]
		if name in options:
			options[name] = value
			print(info("Set: '%s'='%s'" % (name, value)))
			return None
		else:
			print(error("'%s' not found in options" % name))
			return None
	elif subcmd[0] == "use":
		options['payload'] = subcmd[1]
		return None
	elif subcmd[0] == "show":
		thing = subcmd[1]
		if thing == "options":
			for i in options:
				print("'%s' : '%s'" % (i,options[i]))
			return None
		elif thing == "exploits" or thing == "modules":
			files = run_cmd("ls").split("\n")
			try:
				files.remove("msploit.py")
				files.remove("payload.py")
			except: pass
			files = ', '.join(files)
			print(info("Current modules/exploits: " + files))
			return None
	else:
		print(error("Invalid command"))

if __name__ == "__main__":
	main()
