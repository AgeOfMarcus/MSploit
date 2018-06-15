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

help_dict = {
	'help':'prints a help menu',
	'use [payload]':'sets $payload as \'payload\'',
	'set [name] [value]':'sets $name to $value in options',
	'show [object]':'displays object (available: options, modules, exploits',
	'build':'builds the selected payload',
	'exploit':'runs the listener for selected payload',
	'exit':'exits this program',
}

def help_menu():
	for i in help_dict:
		print(c(i,"magenta") + " - " + c(help_dict[i],"magenta"))

def run_cmd(cmd):
	return Popen(cmd,stdout=PIPE,shell=True).communicate()[0].decode()
def error(msg): return c("[!] ","red") + msg
def info(msg): return c("[*] ","cyan") + msg
def yorn(msg):
	pretty = c("y","green") + "/" + c("n","red")
	ch = input(c("[=] ","yellow") + msg + "? [%s]: " % pretty).lower()
	while not ch == "y" or ch == "n":
		ch = input(c("[=] ","yellow") + msg + "? [%s]: " % pretty).lower()
	if ch == "y": return True
	elif ch == "n": return False

def list_exploits():
	ls = Popen("ls",stdout=PIPE,shell=True).communicate()[0].decode().split("\n")
	for i in ls:
		try:
			os.chdir(i)
			os.chdir("..")
		except:
			ls.remove(i)
	try:
		ls.remove("msploit.py")
	except: pass
	for i in ls:
		if i.endswith(".py"): ls.remove(i)
		elif i.endswith(".md"): ls.remove(i)
	return ls

def check_exists(exploit):
	os.chdir(wd)
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
	# obfuscate with: b64, 
	# add staged payloads?
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
			help_menu()
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
				print("'%s' : [%s]" % (c(i,"cyan"),c(options[i],"cyan")))
			return None
		elif thing == "exploits" or thing == "modules":
			files = list_exploits()
			files = ', '.join(files)
			print(info("Current modules/exploits: " + files))
			return None
	else:
		print(error("Invalid command"))

if __name__ == "__main__":
	main()
