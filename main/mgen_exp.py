import time
from threading import Thread
import math
import os
from datetime import datetime

class Mgen():

	Threads = []

	def __init__(self, net, senders, receivers, packetRate, clientMgenFiles, serverMgenFiles, resultPathForClients, resultPathForServers):
		self.net = net
		self.senders = senders
		self.receivers = receivers
		self.packetRate = packetRate
		self.clientMgenFiles = clientMgenFiles
		self.serverMgenFiles = serverMgenFiles
		self.resultPathForClients = resultPathForClients
		self.resultPathForServers = resultPathForServers
		
	def createClientsMgenFiles(self):
		for i in range(len(self.senders)):
		    sender_name = self.senders[i]
		    receiver_name = self.receivers[i]
		    sender_host = self.net.getNodeByName(sender_name)
		    receiver_host = self.net.getNodeByName(receiver_name)
		    f = open(self.clientMgenFiles + sender_name + "ConnectedTo" + receiver_name + ".mgn", "a")
		    f.write("0.0 ON 1 UDP SRC 5002 DST " + receiver_host.IP() + "/5001 PERIODIC [" + self.packetRate + " 1024]\n")
		    f.write("20.0 OFF 1\n")

	def runServers(self):
		for i in range(len(self.receivers)):
			sThread = MGENServerThread(self.net, self.receivers[i], self.serverMgenFiles, self.resultPathForServers)
			sThread.start()
			self.Threads.append(sThread)
			
	def runClients(self):
		for i in range(len(self.senders)):
			cThread = MGENClientThread(self.net, self.senders[i], self.receivers[i], self.clientMgenFiles, self.resultPathForClients)
			cThread.start()
			self.Threads.append(cThread)
			
	def startSimulation(self):
                print "Create MGEN sender files..."
		self.createClientsMgenFiles()
		time.sleep(5)
                print "Run receivers..."
		self.runServers()
		time.sleep(5)
		self.runClients()
                print "Run senders..."
		for th in self.Threads:
		        th.join()
                time.sleep(5)
			
class MGENServerThread(Thread):
	def __init__(self, net, server, serverMgenFiles, resultPathForServers):
		self.net = net
		self.server = server
		self.serverMgenFiles = serverMgenFiles
		self.resultPathForServers = resultPathForServers
		Thread.__init__(self)

	def run(self):
		f1 = self.serverMgenFiles + "receiver.mgn"
		f2 = self.resultPathForServers + "Server" + self.server + ".txt &"
		self.net.getNodeByName(self.server).cmd("mgen flush input " + f1 + " output " + f2)

class MGENClientThread(Thread):
	def __init__(self, net, sender, receiver, clientMgenFiles, resultPathForClients):
		self.net = net
		self.sender = sender
		self.receiver = receiver
		self.clientMgenFiles = clientMgenFiles
		self.resultPathForClients = resultPathForClients
		Thread.__init__(self)

	def run(self):
		f1 = self.clientMgenFiles + self.sender + "ConnectedTo" + self.receiver + ".mgn"
		f2 = self.resultPathForClients + self.sender + "ConnectedTo" + self.receiver + ".txt"
		self.net.getNodeByName(self.sender).cmd("mgen input " + f1 + " txlog > " + f2)
		print('Exiting', self.sender, datetime.now().strftime("%H:%M:%S"))
