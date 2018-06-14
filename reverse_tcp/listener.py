#!/usr/bin/python3

import socket

#VERBOSE#
verbose = False
#VERBOSE#

def debug(msg):
	if verbose: print("[*] "+msg)

#COLOURS#
RED = "\x1b[31m\x1b[0m"
GREEN = "\x1b[32m%s\x1b[0m"
CYAN = "\x1b[36m%s\x1b[0m"
#COLOURS#

def socket_init(ip,port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((ip,port))
	s.listen(1)
	return s

def socket_listen(server):
	debug("Listening for connection")
	conn, addr = server.accept()
	debug("Connection from [%s]" % str(addr))
	return conn

def conn_handshake(conn):
	conn.send("CLIENT?".encode())
	reply = conn.recv(1024).decode()
	if reply == "YEAH.":
		return conn
	else:
		return False

def conn_handler(conn):
	stream = ''
	errors = 0
	while True:
		try:
			debug("Recieving data")
			req = conn.recv(4096).decode()
			if not len(req) > 0:
				debug("Got empty data")
				continue
			if list(req)[-1] == "?":
				debug("Got '?' msg")
				handle_question(conn, req) #make
			elif req.endswith("#done#"):
				debug("Got '#done#' msg")
				req = req.split("#done")[0]
				stream += req
				print(stream)
				stream = ''
			elif req.endswith("#cont#"):
				debug("Got '#cont#' msg")
				req = req.split("#cont#")[0]
				stream += req
				continue
			else:
				debug("Got unfamiliar msg")
		except Exception as e:
			debug("Error: "+str(e))
			errors += 1
			if errors > 5:
				debug("Re-occuring error: "+str(e))
				print("[!] Re-occuring error: "+str(e))
			errors = 0

def handle_question(conn, msg):
	que = msg.split("?")[0]
	if que == "cmd":
		cmd = input("CMD> ")
		conn.send(cmd.encode())
	else:
		debug("Got unfamiliar '?' msg")


def main():
	try:
		verbose = input("Verbose? y/N: ").lower()
		if not verbose == "y":
			verbose = False
		else:
			verbose = True
		ip = input("IP to listen on: ")
		port = int(input("Port to listen on: "))
		server = socket_init(ip,port)
		client = socket_listen(server)
		hs = conn_handshake(client)
		while not hs:
			client = socket_listen(server)
			hs = conn_handshake(client)
		conn_handler(client)
	except Exception as e:
		debug("Error: "+str(e))

if __name__ == "__main__":
	main()
