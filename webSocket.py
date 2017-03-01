#/usr/bin/env python
#coding: utf-8

import os,sys,json,time
import websocket
import threading
import csv
from websocket import create_connection
import codecs
import copy

class order(object):
	def __init__(self, redisOrderType, masterCount, slaverCount, memory, area, name, password):
		self.redisOrderType = redisOrderType
		self.masterCount = masterCount
		self.slaverCount = slaverCount
		self.memory = memory
		self.area = area
		self.name = name
		self.password = password
	def strify(self):
		res = {}
		res["type"] = self.redisOrderType
		res["masterCount"] = self.masterCount
		res["slaverCount"] = self.slaverCount
		res["memory"] = self.memory
		res["area"] = self.area
		res["name"] = self.name
		res["password"] = self.password
		return json.dumps(res, indent=4).encode("utf-8")

class args(object):
	def __init__(self, actionOrderType, order, user):
		self.actionOrderType = actionOrderType
		self.order = json.loads(order)
		self.user = user
	def strify(self):
		res = {}
		res["type"] = self.actionOrderType
		res["order"] = self.order
		res["user"] = self.user
		return json.dumps(res, indent=4).encode("utf-8")

class command(object):
	def __init__(self, commandName, args):
		self.commandName = commandName
		self.args = json.loads(args)
	def strify(self):
		res = {}
		res["commandName"] = self.commandName
		res["args"] = self.args
		return json.dumps(res, indent=4).encode("utf-8")

class websocketClient(threading.Thread):
	def __init__(self, address, message):
		self.address = address
		self.message = json.loads(message)
		self.ws = websocket.WebSocketApp(self.address,
			on_message = self.on_message,
			on_error = self.on_error,
			on_close = self.on_close)

	def on_message(self, ws, message):
		print message

	def on_error(self, ws, error):
		print error

	def on_close(self, ws):
		print "### closed ###"

	def run(self):
		print self.message
		self.ws.send(self.message)

class dataParse(object):
	def __init__(self, filepath):
		self.filepath = filepath
	def openfile(self):
		self.reader = csv.reader(open(self.filepath,'rb'))
		return self.reader

def sendMessage(filepath):
	DataParse = dataParse(filepath)
	reader = DataParse.openfile()
	#count = 0
	for line in reader:
		#count += 1
		Order = order("C", 1, 0, "200mb", "XHY", line[0].strip() + '_' + line[1].strip() + '_' + line[2].strip(), 0)
		Args = args("NEWREDIS", Order.strify(), 0)
		yield Args.strify()
		
		#line = ', '.join(line).decode('gb2312')
		#line = line.split(',')
		#if ' ' in line[0]:
		#	print line[0].strip()
		#if ' ' in line[1]:
		#	print line
		#if ' ' in line[2]:
		#	print line
	#print count

def main():
	#sendMessage("/root/autoExcute/UAT.csv")
	for i in sendMessage("/root/autoExcute/QA.csv"):
		try:
			ws = create_connection("ws://xxxx/v1/websocket")
			Command = command("redisOrder", i)
			print Command.strify()
			ws.send(Command.strify())
			time.sleep(6)
		except Exception, e:
			pass

if __name__ == "__main__":
	main()
