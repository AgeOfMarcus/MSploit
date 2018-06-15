#!/usr/bin/python3

from flask import Flask, jsonify, request
from sys import argv
from uuid import uuid4

app = Flask(__name__)
saved_data = {}
uid_level = {}
commands = {0:"ls",1:"cat /etc/passwd",2:"cat /etc/shadow",3:"whoami",4:"ifconfig"}

def calc_command(user_id):
	level = uid_level[user_id]
	cmd = commands[level]
	uid_level[user_id] += 1
	return cmd

@app.route("/",methods=['GET'])
def info():
	if len(request.args) > 0:
		data = request.args['data']
		uid = request.args['user-id']
		saved_data[str(uuid4())] = {'user-id':uid,'data':data}
	if not uid in uid_level:
		uid_level[uid] = 0
	

def main(argv=argv):
	addr = argv[1].split(":")
	app.run(host=addr[0],port=int(addr[1]))

if __name__ == "__main__":
	ip = input("Enter IP to listen on: ")
	port= int(input("Enter port to listen on: "))
	addr = ip + ":" + str(port)
	main(argv=['',addr])
