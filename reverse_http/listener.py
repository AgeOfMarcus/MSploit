#!/usr/bin/python3

from flask import Flask, jsonify, request
from sys import argv

app = Flask(__name__)

@app.route("/",methods=['GET'])
def info():
	if len(request.args) > 0:
		print(request.args['data'])
	cmd = input("CMD> ")
	return cmd, 200

def main(argv=argv):
	addr = argv[1].split(":")
	app.run(host=addr[0],port=int(addr[1]))

if __name__ == "__main__":
	ip = input("Enter IP to listen on: ")
	port= int(input("Enter port to listen on: "))
	addr = ip + ":" + str(port)
	main(argv=['',addr])
