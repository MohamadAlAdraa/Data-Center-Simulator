import os
import collections
from argparse import ArgumentParser

class Analysis:

	def __init__(self, path_of_the_client_result_directory, path_of_the_server_result_directory):
		self.path_of_the_client_result_directory = path_of_the_client_result_directory
		self.path_of_the_server_result_directory = path_of_the_server_result_directory


	def averageThroughput(self):
		"""
		This function will find the average throughput of all packet rates and runs
		:return dict: keys of the dict is the packet rate and the value is av throughput
		"""
		dict_result = {}
		av_th = 0
		total_files = 0
		for f in os.listdir(self.path_of_the_server_result_directory):
			total_files += 1			
			th = self.calculateThroughput(self.path_of_the_server_result_directory + '/' + f)
			print th
			av_th += th
		return av_th/total_files

	def averageDelay(self, ):
		"""
		This function will find the average delay of all packet rates and runs
		:return dict: keys of the dict is the packet rate and the value is av delay
		"""
		dict_result = {}
		for f in os.listdir(self.path_of_the_server_result_directory):
			global_delay = 0
			for f1 in os.listdir(self.path_of_the_server_result_directory + '/' + f):
				av_dl = 0
				for f2 in os.listdir(self.path_of_the_server_result_directory + '/' + f + '/' + f1):
					dl = self.calculateDelay(self.path_of_the_server_result_directory + '/' + f + '/' + f1 + '/' + f2)
					av_dl += dl
				av_dl /= 16
				global_delay += av_dl
			global_delay /= 25
			dict_result[f] = format(global_delay, '.6f')
		return dict_result

	def averageLoss(self):
		"""
		This function will find the average Loss of all packet rates and runs
		:return dict: keys of the dict is the packet rate and the value is av loss
		"""
		dict_result = {}
		for f in os.listdir(self.path_of_the_client_result_directory):
			global_loss = 0
			for f1 in os.listdir(self.path_of_the_client_result_directory + '/' + f):
				av_loss = 0
				for f2 in os.listdir(self.path_of_the_client_result_directory + '/' + f + '/' + f1):
					c = self.path_of_the_client_result_directory + '/' + f + '/' + f1 + '/' + f2
					s = "Server" + c.split("ConnectedTo")[-1]
					s1 = self.path_of_the_server_result_directory + '/' + f + '/' + f1 + '/' + s
					loss = self.calculateLoss(c, s1)
					av_loss += loss
				av_loss /= 16
				global_loss += av_loss
			global_loss /= 25
			dict_result[f] = int(global_loss)
		return dict_result

	def calculateThroughput(self, filename):
		"""
		This function will sum the data received of each packet and divide it by the total time
		total time is the difference between rx time of the last packet and tx time of the first packet.
		:param filename: server file path
		:return throughput: in Mbits/s
		"""
		f = open(filename, 'r')
		lines = f.readlines()
		numberOfPacketsReceived = len(lines) - 3
		startTime = lines[2].split(" ")[7].split(">")[1]
		endTime = lines[-1].split(" ")[0]
		if len(lines[-1].split(" ")) < 8:
			numberOfPacketsReceived = numberOfPacketsReceived - 1
			endTime = lines[-2].split(" ")[0]
		packetSize = 1024
		totalReceivedData = numberOfPacketsReceived * packetSize
		totalTime = self.calculateTimeDifference(startTime, endTime)
		throughput_in_bytes_per_s = float(totalReceivedData) / float(totalTime)
		throughput_in_mbits_per_s = (throughput_in_bytes_per_s * 8) / 1000000
		#return throughput_in_bytes_per_s
		return throughput_in_mbits_per_s

	def calculateDelay(self, filename):
		"""
		This function will sum the delay of each packet by substituting rx from tx
		:param filename: server file path
		:return delay: in ms
		"""
		f = open(filename, 'r')
		lines = f.readlines()
		delay = 0
		for i in range(2, len(lines)-1):
			txtime = lines[i].split(" ")[7].split(">")[1]
			rxtime = lines[i].split(" ")[0]
			delay += self.calculateTimeDifference(txtime, rxtime)
		if len(lines[-1].split(" ")) > 8:
			txtime = lines[-1].split(" ")[7].split(">")[1]
			rxtime = lines[-1].split(" ")[0]
			delay += self.calculateTimeDifference(txtime, rxtime)

		delay_in_s = delay
		delay_in_ms = delay_in_s * 1000
		#return delay_in_s
		return delay_in_ms

	def calculateLoss(self, clientfilename, serverfilename):
		"""
		This function will find the loss by the substituting the number of packets sent from the number of packets received
		:param clientfilename: client file path
		:param serverfilename: server file path
		:return loss: in # of packets
		"""
		f = open(clientfilename, 'r')
		lines = f.readlines()
		numberOfSentPackets = len(lines) - 4
		f1 = open(serverfilename, 'r')
		lines1 = f1.readlines()
		numberOfReceivedPackets = len(lines1) - 2
		if len(lines1[-1].split(" ")) < 8:
			numberOfReceivedPackets = numberOfReceivedPackets - 1
		return numberOfSentPackets - numberOfReceivedPackets

	def calculateTimeDifference(self, startTime, endTime):
		"""
		:param startTime: transmission time
		:param endTime: reciption time
		:return time: difference between the given times
		"""
		s = startTime.split(":")
		e = endTime.split(":")
		time = (int(e[0])*3600 + int(e[1])*60 + int(float(e[2]))) - (int(s[0])*3600 + int(s[1])*60 + int(float(s[2])))
		return time

if __name__ == "__main__":
	parser = ArgumentParser(description="result file name")
	parser.add_argument('-f', '--filename', dest='topology_file', default='strat.txt', help='Topology input file')
	args = parser.parse_args()
	pr = 110
	ps = 1024
	an = Analysis("/home/mohamad/simulation/lib/results/mgen/clientfiles", "/home/mohamad/simulation/lib/results/mgen/serverfiles")
	throughput = an.averageThroughput()
	of = open("/home/mohamad/simulation/lib/results/mgen/result/"+args.topology_file+".txt", 'a')
	of.write(str(throughput))
	of.write(" ")
	exp_th = float(float(pr*ps) * 8) / float(1000000)
	throughput1 = float(throughput) / float(exp_th)
	of.write(str(throughput1))
	of.write("\n")
	cmd = "sudo rm -r /home/mohamad/simulation/lib/results/mgen/clientfiles/*"
	cmd1 = "sudo rm -r /home/mohamad/simulation/lib/results/mgen/serverfiles/*"
	cmd2 = "sudo rm -r /home/mohamad/simulation/lib/results/mgen/clientmgen/*"
	os.system(cmd)
	os.system(cmd1)
	os.system(cmd2)




