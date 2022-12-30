#!/usr/bin/python

import time
from threading import Thread
import math
import os
from datetime import datetime


class senderThread(Thread):

    def __init__(self, net, sender):
        self.sender = sender
        self.host = net.getNodeByName(self.sender)
        Thread.__init__(self)

    def run(self): 
        self.host.cmd("python -m ComplexHTTPServer 80 &")

class receiverThread(Thread):

    def __init__(
        self,
        net,
        receiver,
        sender,
        fileName = "1mb.txt"
        ):
        self.receiver = receiver
        self.sender = sender
        self.host = net.getNodeByName(self.receiver)
        self.host1 = net.getNodeByName(self.sender)
        self.fileName = fileName
        Thread.__init__(self)
    def run(self):
        r = "/home/mohamad/simulation/lib/results/http_files/"
        self.host.cmd("wget -o %s -O %s %s/%s" % (r+"/logs/"+self.receiver+self.sender+".log", r+"/data/"+self.receiver+self.sender+self.fileName, self.host1.IP(), self.fileName))

        print('Exiting %s' % (datetime.now().strftime("%H:%M:%S")))

class HTTP:

    Threads = []

    def __init__(
        self,
        senders,
        receivers,
        net, 
        bas = False
        ):
        self.senders = senders
        self.receivers = receivers
        self.net = net
        self.bas = bas
        self.startSimulation()

    def runSenders(self):
        set_sen = set(self.senders)
        list_sen = list(set_sen)
        for i in list_sen:
            sThread = senderThread(self.net, i)
            sThread.start()
            self.Threads.append(sThread)

    def runReceivers(self):
        temp_receivers = []
        for i in range(len(self.receivers)):
            if (self.bas == True) and (i%3 == 0):
                cThread = receiverThread(self.net, self.receivers[i], self.senders[i], fileName = "10mb.txt")
                cThread.start()
                if self.receivers[i] not in temp_receivers:
                    temp_receivers.append(self.receivers[i])
                    self.Threads.append(cThread)
            else:
                cThread = receiverThread(self.net, self.receivers[i], self.senders[i])
                cThread.start()
                if self.receivers[i] not in temp_receivers:
                    temp_receivers.append(self.receivers[i])
                    self.Threads.append(cThread)

    def startSimulation(self):
        self.runSenders()
        print '#################################\n'
        print 'Servers are running...'
        print '#################################\n'
        time.sleep(10)
        self.runReceivers()
        for th in self.Threads:
            th.join()
        os.system("sudo mn -c")
        time.sleep(2)
        



